"""Pruebas de instalación selectiva y de los recursos del paquete."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_npv_plugins_ship_only_their_own_skill(self):
        marketplace = json.loads(
            (ROOT / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        entries = {entry["name"]: entry for entry in marketplace["plugins"]}

        expected = (
            ("npv-marketing", "NPV Marketing", "Estrategia de Marketing"),
            ("npv-data", "NPV Datos", "Inteligencia de Mercado"),
        )
        for name, label, skill_label in expected:
            with self.subTest(plugin=name):
                entry = entries[name]
                self.assertEqual(entry["source"]["path"], f"./plugins/{name}")
                self.assertEqual(entry["policy"]["installation"], "AVAILABLE")
                package = ROOT / entry["source"]["path"]
                manifest = json.loads(
                    (package / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
                )
                self.assertEqual(manifest["interface"]["displayName"], label)
                skills = package / manifest["skills"]
                self.assertEqual(
                    {path.parent.name for path in skills.glob("*/SKILL.md")}, {name}
                )
                self.assertTrue((skills / name / "references/capa-npv.md").is_file())
                metadata = (skills / name / "agents/openai.yaml").read_text(encoding="utf-8")
                self.assertIn(f'  display_name: "{skill_label}"', metadata.splitlines())


@unittest.skipIf(os.name == "nt", "El instalador usa Bash; CI lo prueba en Linux")
class InstallerTests(unittest.TestCase):
    def run_installer(self, *args):
        with tempfile.TemporaryDirectory() as directory:
            stub = Path(directory) / "codex"
            log = Path(directory) / "codex.log"
            stub.write_text(
                '#!/bin/sh\nprintf "%s\\n" "$*" >> "$INSTALL_TEST_LOG"\n',
                encoding="utf-8",
            )
            stub.chmod(0o755)
            result = subprocess.run(
                ["bash", str(ROOT / "scripts/install.sh"), *args],
                cwd=directory,
                env=dict(os.environ, PATH=f"{directory}{os.pathsep}{os.environ['PATH']}",
                         INSTALL_TEST_LOG=str(log)),
                capture_output=True,
                text=True,
            )
            calls = log.read_text(encoding="utf-8").splitlines() if log.exists() else []
            return result, calls

    def test_fresh_install_of_either_plugin(self):
        for name in ("npv-marketing", "npv-data"):
            with self.subTest(plugin=name):
                result, calls = self.run_installer(name)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(calls, [
                    f"plugin marketplace add {ROOT}",
                    f"plugin add {name}@business-bots",
                ])

    def test_update_both_without_registering_marketplace_again(self):
        result, calls = self.run_installer("--update", "npv-marketing", "npv-data")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(calls, [
            "plugin add npv-marketing@business-bots",
            "plugin add npv-data@business-bots",
        ])

    def test_unknown_plugin_does_not_install_a_valid_first_argument(self):
        result, calls = self.run_installer("npv-marketing", "unknown")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown", result.stderr)
        self.assertEqual(calls, [])
