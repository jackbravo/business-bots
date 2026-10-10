"""Pruebas con datos ficticios: persistencia, revisiones y límites del adaptador."""
from datetime import datetime, timezone
from decimal import Decimal
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

SCRIPT = Path(__file__).resolve().parents[1] / "plugins/npv-marketing/skills/npv-data/scripts/npv_data.py"
spec = importlib.util.spec_from_file_location("npv_data", SCRIPT)
data = importlib.util.module_from_spec(spec)
spec.loader.exec_module(data)
T1 = datetime(2026, 9, 1, tzinfo=timezone.utc)
T2 = datetime(2026, 9, 2, tzinfo=timezone.utc)
SOURCE = ("demo", "Datos ficticios", "https://example.com/", "demo")


def observation(value="2", period="2026-08", sid="ventas"):
    return dict(series_id=sid, series_name="Ventas netas", unit="unidades", frequency="monthly", geography="project:demo", period=period, value=data.number(value))


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.temp.name) / "demo.duckdb")
        self.con = data.connect_database(self.db)
        data.initialize(self.con)

    def tearDown(self):
        self.con.close()
        self.temp.cleanup()

    def ingest(self, rows, at=T1):
        return data.ingest(self.con, SOURCE, rows, at, "fixture-hash")

    def test_init_is_repeatable_and_rejects_future_schema(self):
        self.ingest([observation()])
        data.initialize(self.con)
        self.assertEqual(self.con.execute("SELECT count(*) FROM npv.observations").fetchone()[0], 1)
        self.con.execute("INSERT INTO npv.schema_versions(version) VALUES(2)")
        with self.assertRaises(data.DataError):
            data.initialize(self.con)

    def test_repeat_load_keeps_one_observation_and_refreshes_check(self):
        self.assertEqual(self.ingest([observation()])["new_revisions"], 1)
        self.assertEqual(self.ingest([observation()], T2)["new_revisions"], 0)
        self.assertEqual(self.con.execute("SELECT count(*) FROM npv.observations").fetchone()[0], 1)
        self.assertEqual(self.con.execute("SELECT first_retrieved_at,last_checked_at FROM npv.observations").fetchone(), (T1, T2))
        self.assertEqual(self.con.execute("SELECT count(*) FROM npv.ingestion_runs").fetchone()[0], 2)

    def test_correction_and_reversion_preserve_history(self):
        self.ingest([observation("2")])
        self.ingest([observation("3")], T2)
        self.ingest([observation("2")], T2)
        self.assertEqual(self.con.execute("SELECT revision,value FROM npv.observations ORDER BY revision").fetchall(), [(1, Decimal(2)), (2, Decimal(3)), (3, Decimal(2))])
        self.assertEqual(self.con.execute("SELECT revision,value FROM npv.current_observations").fetchone(), (3, Decimal(2)))

    def test_stale_retrieval_cannot_replace_latest(self):
        self.ingest([observation()], T2)
        with self.assertRaises(data.DataError):
            self.ingest([observation("5")], T1)
        self.assertEqual(self.con.execute("SELECT value FROM npv.current_observations").fetchone()[0], 2)
        self.assertEqual(self.con.execute("SELECT count(*) FROM npv.ingestion_runs").fetchone()[0], 1)

    def test_definition_change_rolls_back_entire_batch(self):
        self.ingest([observation()])
        conflicting = observation()
        conflicting["unit"] = "MXN"
        with self.assertRaises(data.DataError):
            self.ingest([observation(period="2026-07", sid="otra"), conflicting], T2)
        self.assertEqual(self.con.execute("SELECT count(*) FROM npv.indicators").fetchone()[0], 1)
        self.assertEqual(self.con.execute("SELECT count(*) FROM npv.ingestion_runs").fetchone()[0], 1)

    def test_zero_and_missing_remain_distinct(self):
        self.ingest([observation("0"), observation("N/E", "2026-07")])
        self.assertEqual(self.con.execute("SELECT value,status FROM npv.current_observations ORDER BY period DESC").fetchall(), [(Decimal(0), "available"), (None, "unavailable")])

    def test_duplicate_rows_and_invalid_period_fail_before_writes(self):
        for rows in ([observation(), observation()], [observation(period="2026-13")]):
            with self.assertRaises(data.DataError):
                self.ingest(rows)
        self.assertEqual(self.con.execute("SELECT count(*) FROM npv.sources").fetchone()[0], 0)

    def test_conflicting_source_is_rejected(self):
        data.ensure_source(self.con, SOURCE)
        with self.assertRaises(data.DataError):
            data.ensure_source(self.con, ("demo", "Otro nombre", SOURCE[2], "demo"))

    def test_document_deduplication_and_version_link(self):
        data.ensure_source(self.con, SOURCE)
        file = Path(self.temp.name) / "report.txt"
        file.write_text("Reporte ficticio v1")
        first = data.register_document(self.con, "demo", file, "Prueba", "https://example.com/report", "2026-08-31")
        again = data.register_document(self.con, "demo", file, "Prueba", "https://example.com/report", "2026-08-31")
        self.assertEqual(first["document_id"], again["document_id"])
        self.assertFalse(again["created"])
        self.assertFalse(first["original_uploaded"])
        file.write_text("Reporte ficticio v2")
        second = data.register_document(self.con, "demo", file, "Prueba", "https://example.com/report-v2", supersedes=first["document_id"])
        self.assertTrue(second["created"])
        self.assertEqual(self.con.execute("SELECT supersedes_document_id FROM npv.documents WHERE document_id=?", [second["document_id"]]).fetchone()[0], first["document_id"])


class AdapterTests(unittest.TestCase):
    def test_successful_download_retries_then_normalizes(self):
        payload = {"bmx": {"series": [{"idSerie": "SF43718", "datos": [{"fecha": "01/09/2026", "dato": "18.5000"}]}]}}
        raw = json.dumps(payload).encode()
        class Response:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def read(self, limit):
                return raw
        class Opener:
            calls = 0
            def open(self, request, timeout):
                self.calls += 1
                if self.calls < 3:
                    raise HTTPError(request.full_url, 429, "throttled", {}, None)
                return Response()
        opener = Opener()
        with patch.dict(os.environ, {"BANXICO_TOKEN": "SYNTHETIC_TOKEN_FOR_TEST_ONLY"}), patch.object(data, "build_opener", return_value=opener), patch.object(data.time, "sleep") as sleep:
            rows, digest, url, retrieved = data.download_banxico(["SF43718"], latest=True)
        self.assertEqual(opener.calls, 3)
        self.assertEqual(sleep.call_count, 2)
        self.assertEqual(rows[0]["value"], Decimal("18.5"))
        self.assertEqual(len(digest), 64)
        self.assertTrue(url.endswith("/series/SF43718/datos/oportuno"))
        self.assertIsNotNone(retrieved.tzinfo)

    def test_existing_unversioned_namespace_is_not_adopted(self):
        import duckdb
        with duckdb.connect() as con:
            con.execute("CREATE SCHEMA npv; CREATE TABLE npv.legacy(value INTEGER)")
            with self.assertRaises(data.DataError):
                data.initialize(con)
            self.assertEqual(con.execute("SELECT count(*) FROM information_schema.tables WHERE table_schema='npv'").fetchone()[0], 1)

    def test_banxico_parsing_and_response_scope(self):
        catalog = json.loads((data.ASSETS / "banxico-series.json").read_text())
        payload = {"bmx": {"series": [{"idSerie": "SF43718", "datos": [{"fecha": "01/09/2026", "dato": "1,234.50000"}]}]}}
        rows = data.normalize_banxico(payload, ["SF43718"], catalog)
        self.assertEqual(rows[0]["value"], Decimal("1234.5"))
        self.assertEqual(rows[0]["period"], "2026-09-01")
        with self.assertRaises(data.DataError):
            data.normalize_banxico(payload, ["SF61745"], catalog)
        with self.assertRaises(data.DataError):
            data.normalize_banxico(payload, ["SF43718"], catalog, "2026-09-02", "2026-09-03")

    def test_token_only_in_header_and_errors_do_not_echo_it(self):
        token = "SYNTHETIC_TOKEN_FOR_TEST_ONLY"
        captured = []
        class Opener:
            def open(self, request, timeout):
                captured.append(request)
                raise HTTPError(request.full_url, 401, token, {}, None)
        with patch.dict(os.environ, {"BANXICO_TOKEN": token}), patch.object(data, "build_opener", return_value=Opener()):
            with self.assertRaises(data.DataError) as result:
                data.download_banxico(["SF43718"], latest=True)
        self.assertNotIn(token, str(result.exception))
        self.assertNotIn(token, captured[0].full_url)
        self.assertEqual(captured[0].get_header("Bmx-token"), token)

    def test_missing_credentials_and_redirects(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(data.DataError, "BANXICO_TOKEN"):
                data.download_banxico(["SF43718"], latest=True)
            with self.assertRaisesRegex(data.DataError, "motherduck_token"):
                data.connect_database("md:npv_pilot")
        with self.assertRaises(data.DataError):
            data.NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.com")

    def test_numeric_precision_and_periods(self):
        for invalid in ("NaN", "Infinity", "1,2", "1000000000000000000", "0.00000000001"):
            with self.assertRaises(data.DataError):
                data.number(invalid)
        for period, frequency in (("2026-02-30", "daily"), ("2026-Q5", "quarterly"), ("0", "annual")):
            with self.assertRaises(data.DataError):
                data.check_period(period, frequency)
        self.assertEqual(data.number("12.50000000000"), Decimal("12.5"))


class ProcessTests(unittest.TestCase):
    def test_csv_persists_across_processes_and_queries_are_readonly(self):
        with tempfile.TemporaryDirectory() as temp:
            db, csv_file = Path(temp) / "demo.duckdb", Path(temp) / "demo.csv"
            csv_file.write_text("series_id,series_name,unit,frequency,geography,period,value\nventas,Ventas netas,unidades,monthly,project:demo,2026-08,2\n")
            def run(*args):
                result = subprocess.run([sys.executable, str(SCRIPT), "--database", str(db), *args], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                return json.loads(result.stdout)
            run("init")
            run("register-source", "--id", "demo", "--name", "Datos ficticios", "--url", "https://example.com/", "--category", "demo")
            args = ("import-csv", "--source-id", "demo", "--file", str(csv_file), "--retrieved-at", T1.isoformat())
            self.assertEqual(run(*args)["new_revisions"], 1)
            self.assertEqual(run(*args)["new_revisions"], 0)
            before = db.read_bytes()
            rows = run("show-series", "--indicator", "demo:ventas", "--geography", "project:demo")
            self.assertEqual(rows[0]["value"], "2.0000000000")
            self.assertEqual(rows[0]["source_name"], "Datos ficticios")
            self.assertEqual(before, db.read_bytes())
            csv_file.write_text("series_id,series_name,unit,frequency,geography,period,value\nventas,Ventas netas,unidades,monthly,project:demo,2026-08,2\nventas,Ventas netas,unidades,monthly,project:demo,2026-08,3\n")
            result = subprocess.run([sys.executable, str(SCRIPT), "--database", str(db), *args], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("duplicadas", result.stderr)


if __name__ == "__main__":
    unittest.main()
