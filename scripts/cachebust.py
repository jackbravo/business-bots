#!/usr/bin/env python3
"""Añade o reemplaza el cachebuster local de un plugin de Codex."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re


PLUGIN_NAME = re.compile(r"^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*$")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("plugin_path", type=pathlib.Path)
    parser.add_argument("--token", help="Token explícito; por defecto usa la hora UTC")
    args = parser.parse_args()

    manifest_path = args.plugin_path / ".codex-plugin" / "plugin.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))

    expected_name = args.plugin_path.resolve().name
    actual_name = data.get("name")
    if actual_name != expected_name or not PLUGIN_NAME.fullmatch(str(actual_name)):
        raise SystemExit(
            f"Nombre inválido: carpeta={expected_name!r}, manifiesto={actual_name!r}"
        )

    version = data.get("version")
    if not isinstance(version, str) or not version.strip():
        raise SystemExit("El manifiesto no contiene una versión válida")

    token = args.token or dt.datetime.now(dt.UTC).strftime("local-%Y%m%d-%H%M%S")
    if not re.fullmatch(r"[0-9A-Za-z.-]+", token):
        raise SystemExit("El token solo puede contener letras, números, puntos y guiones")

    base_version = version.split("+", 1)[0]
    data["version"] = f"{base_version}+codex.{token}"
    manifest_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(data["version"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
