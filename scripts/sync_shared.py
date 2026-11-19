#!/usr/bin/env python3
"""Copia la guía común dentro de cada paquete instalable de NPV."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "shared" / "npv" / "capa-npv.md"
TARGETS = [
    ROOT / "plugins" / name / "skills" / name / "references" / SOURCE.name
    for name in ("npv-data", "npv-marketing")
]
HEADER = "<!-- Copia generada desde shared/npv/capa-npv.md. Editar la fuente y ejecutar python3 scripts/sync_shared.py. -->\n\n"


def shared_content() -> str:
    return HEADER + SOURCE.read_text(encoding="utf-8")


def validate_shared() -> list[str]:
    expected = shared_content()
    return [
        f"{path.relative_to(ROOT)}: ejecuta python3 scripts/sync_shared.py"
        for path in TARGETS
        if not path.is_file() or path.read_text(encoding="utf-8") != expected
    ]


if __name__ == "__main__":
    content = shared_content()
    for path in TARGETS:
        path.write_text(content, encoding="utf-8", newline="\n")
