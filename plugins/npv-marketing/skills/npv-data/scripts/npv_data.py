#!/usr/bin/env python3
"""CLI del prototipo NPV: datos trazables en DuckDB o MotherDuck."""
from __future__ import annotations

import argparse
import csv
from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import uuid

ASSETS = Path(__file__).resolve().parent.parent / "assets"
BANXICO_ROOT = "https://www.banxico.org.mx/SieAPIRest/service/v1"
BANXICO_SOURCE = ("banxico", "Banco de México", BANXICO_ROOT + "/", "macro")
MAX_BYTES = 8 * 1024 * 1024


class DataError(Exception):
    """Error público: no incluir credenciales, payloads ni errores del proveedor."""


def utc_now():
    return datetime.now(timezone.utc)


def timestamp(raw):
    try:
        value = datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except (ValueError, AttributeError) as exc:
        raise DataError("Usar fecha/hora ISO con zona horaria.") from exc
    if value.tzinfo is None or value > utc_now():
        raise DataError("La fecha de recuperación debe tener zona y no estar en el futuro.")
    return value.astimezone(timezone.utc)


def iso_date(raw):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw):
        raise DataError("Usar fecha YYYY-MM-DD.")
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise DataError("Fecha inválida.") from exc


def check_period(period, frequency):
    if frequency == "daily":
        iso_date(period)
    elif frequency == "monthly":
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", period):
            raise DataError("Periodo mensual inválido: usar YYYY-MM.")
        iso_date(period + "-01")
    elif frequency == "quarterly":
        if not re.fullmatch(r"\d{4}-Q[1-4]", period):
            raise DataError("Periodo trimestral inválido: usar YYYY-Q1 a YYYY-Q4.")
        iso_date(period[:4] + "-01-01")
    elif frequency == "annual":
        if not re.fullmatch(r"\d{4}", period):
            raise DataError("Periodo anual inválido: usar YYYY.")
        iso_date(period + "-01-01")
    else:
        raise DataError("Frecuencia no admitida.")


def number(raw, grouped=False):
    text = str(raw).strip()
    if text in ("", "N/E", "N/D", "ND", "N/A"):
        return None
    pattern = r"-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?" if grouped else r"-?\d+(?:\.\d+)?"
    if not re.fullmatch(pattern, text):
        raise DataError("Valor numérico inválido; usar punto decimal (CSV sin miles).")
    try:
        result = Decimal(text.replace(",", ""))
        if not result.is_finite() or abs(result) >= Decimal("1e18") or result != result.quantize(Decimal("1e-10")):
            raise DataError("Valor fuera de precisión DECIMAL(28,10).")
        return result
    except InvalidOperation as exc:
        raise DataError("Valor fuera de precisión DECIMAL(28,10).") from exc


def public_url(raw):
    parts = urlsplit(raw)
    if parts.scheme != "https" or not parts.netloc or parts.username or parts.password or parts.query or parts.fragment:
        raise DataError("Usar URL HTTPS sin credenciales, parámetros ni fragmentos.")
    return raw


def validate_source(source):
    source_id, name, url, category = source
    if not re.fullmatch(r"[a-z][a-z0-9_-]{0,63}", source_id) or not name.strip():
        raise DataError("Identificador o nombre de fuente inválido.")
    public_url(url)
    if category not in ("macro", "sector", "internal", "market", "reports", "demo"):
        raise DataError("Categoría de fuente no admitida.")


def connect_database(target, readonly=False):
    import duckdb
    if target.startswith("md:"):
        if not re.fullmatch(r"md:[A-Za-z][A-Za-z0-9_]*", target):
            raise DataError("Usar md:nombre_base sin tokens ni parámetros.")
        if not os.environ.get("motherduck_token"):
            raise DataError("Falta motherduck_token en los secretos del entorno.")
        # Permisos remotos dependen de la cuenta; las operaciones de lectura solo ejecutan SELECT.
        return duckdb.connect(target)
    if target == ":memory:":
        raise DataError("Usar un archivo persistente o md:nombre_base.")
    return duckdb.connect(target, read_only=readonly)


def check_schema(con, allow_empty=False):
    exists = con.execute("SELECT count(*) FROM information_schema.tables WHERE table_schema='npv' AND table_name='schema_versions'").fetchone()[0]
    if not exists:
        if allow_empty:
            occupied = con.execute("SELECT count(*) FROM information_schema.tables WHERE table_schema='npv'").fetchone()[0]
            if occupied:
                raise DataError("El namespace npv ya contiene tablas sin versión; revisar antes de inicializar.")
            return
        raise DataError("Falta esquema NPV; ejecutar init sobre el destino autorizado.")
    if con.execute("SELECT version FROM npv.schema_versions ORDER BY version").fetchall() != [(1,)]:
        raise DataError("Versión de esquema incompatible; no modificar automáticamente.")


def initialize(con):
    check_schema(con, allow_empty=True)
    con.execute("BEGIN TRANSACTION")
    try:
        con.execute((ASSETS / "schema-v1.sql").read_text(encoding="utf-8"))
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise
    return {"schema_version": 1}


def ensure_source(con, source):
    validate_source(source)
    previous = con.execute("SELECT source_id,name,url,category FROM npv.sources WHERE source_id=?", [source[0]]).fetchone()
    if previous and tuple(source) != previous:
        raise DataError("La fuente ya existe con otros metadatos; usar otro identificador.")
    if not previous:
        con.execute("INSERT INTO npv.sources VALUES (?,?,?,?)", source)


def validate_rows(rows):
    if not rows:
        raise DataError("La fuente no devolvió observaciones; no se cargó nada.")
    seen, definitions = set(), {}
    for row in rows:
        sid = row["series_id"]
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,128}", sid):
            raise DataError("Identificador de serie inválido.")
        if any(not row[key].strip() for key in ("series_name", "unit", "geography")):
            raise DataError("Nombre, unidad y geografía son obligatorios.")
        check_period(row["period"], row["frequency"])
        definition = (row["series_name"], row["unit"], row["frequency"])
        if sid in definitions and definitions[sid] != definition:
            raise DataError("Definiciones contradictorias para una misma serie.")
        definitions[sid] = definition
        key = (sid, row["geography"], row["period"])
        if key in seen:
            raise DataError("Observaciones duplicadas dentro de la carga.")
        seen.add(key)


def ingest(con, source, rows, retrieved_at, content_hash, request_url=None):
    validate_rows(rows)
    check_schema(con)
    run_id, new_revisions = str(uuid.uuid4()), 0
    con.execute("BEGIN TRANSACTION")
    try:
        ensure_source(con, source)
        con.execute("INSERT INTO npv.ingestion_runs(run_id,source_id,retrieved_at,content_hash,request_url,row_count,new_revisions) VALUES (?,?,?,?,?,?,0)", [run_id, source[0], retrieved_at, content_hash, request_url, len(rows)])
        for row in rows:
            indicator_id = source[0] + ":" + row["series_id"]
            definition = (row["series_name"], row["unit"], row["frequency"])
            previous_definition = con.execute("SELECT name,unit,frequency FROM npv.indicators WHERE indicator_id=?", [indicator_id]).fetchone()
            if previous_definition and previous_definition != definition:
                raise DataError("Cambió la definición de la serie; revisar antes de combinarla.")
            if not previous_definition:
                con.execute("INSERT INTO npv.indicators VALUES (?,?,?,?,?,?)", [indicator_id, source[0], row["series_id"], *definition])
            key = [indicator_id, row["geography"], row["period"]]
            previous = con.execute("SELECT revision,value,status,last_checked_at FROM npv.observations WHERE indicator_id=? AND geography=? AND period=? ORDER BY revision DESC LIMIT 1", key).fetchone()
            value, status = row["value"], "unavailable" if row["value"] is None else "available"
            if previous and retrieved_at < previous[3]:
                raise DataError("Carga anterior al último control: no sustituir datos más recientes.")
            if previous and (value, status) == previous[1:3]:
                con.execute("UPDATE npv.observations SET last_checked_at=? WHERE indicator_id=? AND geography=? AND period=? AND revision=?", [retrieved_at, *key, previous[0]])
                continue
            revision = previous[0] + 1 if previous else 1
            con.execute("INSERT INTO npv.observations VALUES (?,?,?,?,?,?,?,?,?)", [*key, revision, value, status, run_id, retrieved_at, retrieved_at])
            new_revisions += 1
        con.execute("UPDATE npv.ingestion_runs SET new_revisions=? WHERE run_id=?", [new_revisions, run_id])
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise
    stored = con.execute("SELECT row_count,new_revisions FROM npv.ingestion_runs WHERE run_id=?", [run_id]).fetchone()
    return {"run_id": run_id, "rows": stored[0], "new_revisions": stored[1], "unchanged": stored[0] - stored[1], "retrieved_at": retrieved_at.isoformat()}


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise DataError("Redirección rechazada; no reenviar el token de Banxico.")


def download_banxico(series, start=None, end=None, latest=False):
    catalog = json.loads((ASSETS / "banxico-series.json").read_text(encoding="utf-8"))
    if not series or len(series) != len(set(series)) or any(s not in catalog for s in series):
        raise DataError("Seleccionar series distintas del catálogo verificado: " + ", ".join(catalog))
    if latest:
        if start or end:
            raise DataError("No combinar --latest con un rango de fechas.")
        suffix = "oportuno"
    else:
        if not start or not end or iso_date(start) > iso_date(end):
            raise DataError("Indicar --start y --end en orden, o --latest.")
        suffix = start + "/" + end
    token = os.environ.get("BANXICO_TOKEN")
    if not token:
        raise DataError("Falta BANXICO_TOKEN en los secretos del entorno.")
    if not re.fullmatch(r"[A-Za-z0-9_-]{16,256}", token):
        raise DataError("BANXICO_TOKEN no tiene un formato válido.")
    url = BANXICO_ROOT + "/series/" + ",".join(series) + "/datos/" + suffix
    request = Request(url, headers={"Bmx-Token": token, "Accept": "application/json"})
    opener = build_opener(NoRedirect())
    for attempt in range(3):
        try:
            with opener.open(request, timeout=20) as response:
                raw = response.read(MAX_BYTES + 1)
            break
        except HTTPError as exc:
            if exc.code in (429, 500, 502, 503, 504) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise DataError(f"Banxico respondió HTTP {exc.code}; revisar acceso o disponibilidad.") from None
        except (URLError, TimeoutError):
            raise DataError("No se pudo acceder a Banxico; no se guardaron datos.") from None
    if len(raw) > MAX_BYTES:
        raise DataError("Respuesta demasiado grande; reducir el rango de fechas.")
    try:
        rows = normalize_banxico(json.loads(raw), series, catalog, start, end)
    except (KeyError, TypeError, ValueError, UnicodeError):
        raise DataError("Respuesta de Banxico no reconocida; no se guardaron datos.") from None
    return rows, hashlib.sha256(raw).hexdigest(), url, utc_now()


def normalize_banxico(payload, series, catalog, start=None, end=None):
    rows, returned = [], []
    for item in payload["bmx"]["series"]:
        sid = item["idSerie"]
        if sid not in series:
            raise DataError("Banxico devolvió una serie no solicitada.")
        returned.append(sid)
        for observation in item["datos"]:
            period = datetime.strptime(observation["fecha"], "%d/%m/%Y").date().isoformat()
            if (start and period < start) or (end and period > end):
                raise DataError("Banxico devolvió un periodo fuera del rango solicitado.")
            definition = catalog[sid]
            rows.append({"series_id": sid, "series_name": definition["name"], "unit": definition["unit"], "frequency": definition["frequency"], "geography": definition["geography"], "period": period, "value": number(observation["dato"], grouped=True)})
    if sorted(returned) != sorted(series):
        raise DataError("Banxico no devolvió todas las series solicitadas una sola vez.")
    validate_rows(rows)
    return rows


def read_csv(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise DataError("CSV demasiado grande para el prototipo.")
    required = {"series_id", "series_name", "unit", "frequency", "geography", "period", "value"}
    with io.StringIO(raw.decode("utf-8-sig"), newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or set(reader.fieldnames) != required or len(reader.fieldnames) != len(required):
            raise DataError("CSV debe contener exactamente: " + ", ".join(sorted(required)))
        rows = []
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise DataError("Fila CSV incompleta o con columnas sobrantes.")
            row = {k: v.strip() for k, v in row.items()}
            row["value"] = number(row["value"])
            rows.append(row)
    validate_rows(rows)
    return rows, hashlib.sha256(raw).hexdigest()


def register_document(con, source_id, file, title, locator, published=None, supersedes=None):
    check_schema(con)
    if not con.execute("SELECT 1 FROM npv.sources WHERE source_id=?", [source_id]).fetchone():
        raise DataError("Registrar primero la fuente del documento.")
    if not title.strip() or not locator.strip():
        raise DataError("Título y ubicación del original son obligatorios.")
    if locator.startswith("https:"):
        public_url(locator)
    published_on = iso_date(published) if published else None
    if published_on and published_on > date.today():
        raise DataError("La publicación no puede estar en el futuro.")
    digest, byte_count = hashlib.sha256(), 0
    with Path(file).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
            byte_count += len(block)
    if not byte_count:
        raise DataError("Documento vacío.")
    content_hash = digest.hexdigest()
    previous = con.execute("SELECT document_id FROM npv.documents WHERE source_id=? AND content_hash=?", [source_id, content_hash]).fetchone()
    if previous:
        return {"document_id": previous[0], "created": False, "original_uploaded": False}
    if supersedes and not con.execute("SELECT 1 FROM npv.documents WHERE document_id=? AND source_id=?", [supersedes, source_id]).fetchone():
        raise DataError("La versión anterior debe existir y pertenecer a la misma fuente.")
    document_id = str(uuid.uuid4())
    con.execute("INSERT INTO npv.documents(document_id,source_id,title,published_on,original_locator,content_hash,byte_count,supersedes_document_id) VALUES (?,?,?,?,?,?,?,?)", [document_id, source_id, title, published_on, locator, content_hash, byte_count, supersedes])
    verified = con.execute("SELECT document_id FROM npv.documents WHERE document_id=?", [document_id]).fetchone()
    return {"document_id": verified[0], "created": True, "original_uploaded": False}


def query_rows(con, sql, parameters=()):
    cursor = con.execute(sql, parameters)
    names = [column[0] for column in cursor.description]
    return [dict(zip(names, row)) for row in cursor.fetchall()]


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, help="Archivo DuckDB o md:base_existente; nunca incluir tokens")
    subs = parser.add_subparsers(dest="command", required=True)
    subs.add_parser("init")
    source = subs.add_parser("register-source")
    source.add_argument("--id", required=True)
    source.add_argument("--name", required=True)
    source.add_argument("--url", required=True)
    source.add_argument("--category", required=True, choices=["macro", "sector", "internal", "market", "reports", "demo"])
    fetch = subs.add_parser("fetch-banxico")
    fetch.add_argument("--series", nargs="+", required=True)
    fetch.add_argument("--start")
    fetch.add_argument("--end")
    fetch.add_argument("--latest", action="store_true")
    upload = subs.add_parser("import-csv")
    upload.add_argument("--file", required=True)
    upload.add_argument("--source-id", required=True)
    upload.add_argument("--retrieved-at", required=True)
    doc = subs.add_parser("register-document")
    doc.add_argument("--file", required=True)
    doc.add_argument("--source-id", required=True)
    doc.add_argument("--title", required=True)
    doc.add_argument("--original-locator", required=True, help="Ubicación durable del original; este comando no lo sube")
    doc.add_argument("--published-on")
    doc.add_argument("--supersedes")
    subs.add_parser("list-documents")
    subs.add_parser("list-indicators")
    show = subs.add_parser("show-series")
    show.add_argument("--indicator", required=True)
    show.add_argument("--geography", required=True)
    show.add_argument("--history", action="store_true")
    show.add_argument("--limit", type=int, default=100)
    return parser


def execute(args):
    readonly = args.command in ("show-series", "list-indicators", "list-documents")
    con = connect_database(args.database, readonly=readonly)
    try:
        if args.command == "init":
            return initialize(con)
        check_schema(con)
        if args.command == "register-source":
            source = (args.id, args.name, args.url, args.category)
            if args.id == "banxico":
                raise DataError("La fuente banxico se registra mediante fetch-banxico.")
            ensure_source(con, source)
            return {"source_id": args.id}
        if args.command == "fetch-banxico":
            rows, digest, url, fetched_at = download_banxico(args.series, args.start, args.end, args.latest)
            return ingest(con, BANXICO_SOURCE, rows, fetched_at, digest, url)
        if args.command == "import-csv":
            source = con.execute("SELECT source_id,name,url,category FROM npv.sources WHERE source_id=?", [args.source_id]).fetchone()
            if not source or source[0] == "banxico":
                raise DataError("Registrar una fuente de carga manual distinta de banxico.")
            rows, digest = read_csv(args.file)
            return ingest(con, source, rows, timestamp(args.retrieved_at), digest)
        if args.command == "register-document":
            return register_document(con, args.source_id, args.file, args.title, args.original_locator, args.published_on, args.supersedes)
        if args.command == "list-documents":
            return query_rows(con, "SELECT d.*,s.name AS source_name,s.url AS source_url FROM npv.documents d JOIN npv.sources s USING(source_id) ORDER BY registered_at DESC LIMIT 100")
        if args.command == "list-indicators":
            return query_rows(con, "SELECT i.*,s.name AS source_name,s.url AS source_url FROM npv.indicators i JOIN npv.sources s USING(source_id) ORDER BY indicator_id")
        if not 1 <= args.limit <= 10000:
            raise DataError("Usar --limit entre 1 y 10000.")
        table = "npv.observations" if args.history else "npv.current_observations"
        return query_rows(con, f"SELECT o.*,i.name,i.unit,i.frequency,s.name AS source_name,s.url AS source_url,r.request_url,r.retrieved_at,r.loaded_at FROM {table} o JOIN npv.indicators i USING(indicator_id) JOIN npv.sources s USING(source_id) JOIN npv.ingestion_runs r USING(run_id) WHERE indicator_id=? AND geography=? ORDER BY period DESC,revision DESC LIMIT ?", [args.indicator, args.geography, args.limit])
    finally:
        con.close()


def main():
    args = build_parser().parse_args()
    try:
        print(json.dumps(execute(args), default=str, ensure_ascii=False, indent=2))
        return 0
    except DataError as exc:
        print("ERROR: " + str(exc), file=sys.stderr)
    except ImportError:
        print("ERROR: Instalar scripts/requirements.txt en el entorno.", file=sys.stderr)
    except Exception:
        # No imprimir mensajes del driver: pueden contener credenciales o contenido privado.
        print("ERROR: No se pudo completar la operación; revisar archivo, conexión, permisos y esquema. No se confirma guardado.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
