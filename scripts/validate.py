#!/usr/bin/env python3
"""Validación estructural, sin dependencias externas, del marketplace y sus plugins."""

from __future__ import annotations

import json
import pathlib
import re
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / ".agents" / "plugins" / "marketplace.json"
NAME = re.compile(r"^[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*$")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
ALLOWED_INSTALLATION = {"NOT_AVAILABLE", "AVAILABLE", "INSTALLED_BY_DEFAULT"}
ALLOWED_AUTHENTICATION = {"ON_INSTALL", "ON_USE"}


class ValidationError(Exception):
    pass


def load_json(path: pathlib.Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValidationError(f"{path.relative_to(ROOT)}: JSON inválido: {exc}") from exc
    if not isinstance(value, dict):
        raise ValidationError(f"{path.relative_to(ROOT)}: se esperaba un objeto JSON")
    return value


def frontmatter(path: pathlib.Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValidationError(f"{path.relative_to(ROOT)}: falta frontmatter")
    try:
        raw, _body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValidationError(f"{path.relative_to(ROOT)}: frontmatter sin cierre") from exc

    result: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValidationError(f"{path.relative_to(ROOT)}: línea inválida: {line!r}")
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def validate_links(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    for target in MARKDOWN_LINK.findall(text):
        clean = target.split("#", 1)[0].strip()
        if not clean or "://" in clean or clean.startswith(("mailto:", "#")):
            continue
        if not (path.parent / clean).resolve().exists():
            errors.append(f"{path.relative_to(ROOT)}: enlace inexistente: {target}")
    return errors


def validate_plugin(entry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    plugin_name = entry.get("name")
    if not isinstance(plugin_name, str) or not NAME.fullmatch(plugin_name):
        return [f"marketplace: nombre de plugin inválido: {plugin_name!r}"]

    source = entry.get("source")
    expected_source = f"./plugins/{plugin_name}"
    if source != {"source": "local", "path": expected_source}:
        errors.append(f"{plugin_name}: source debe apuntar a {expected_source}")

    policy = entry.get("policy")
    if not isinstance(policy, dict):
        errors.append(f"{plugin_name}: falta policy")
    else:
        if policy.get("installation") not in ALLOWED_INSTALLATION:
            errors.append(f"{plugin_name}: policy.installation inválida")
        if policy.get("authentication") not in ALLOWED_AUTHENTICATION:
            errors.append(f"{plugin_name}: policy.authentication inválida")
    if not entry.get("category"):
        errors.append(f"{plugin_name}: falta category")

    plugin_path = ROOT / "plugins" / plugin_name
    manifest_path = plugin_path / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        return errors + [f"{plugin_name}: falta .codex-plugin/plugin.json"]

    manifest = load_json(manifest_path)
    if manifest.get("name") != plugin_name:
        errors.append(f"{plugin_name}: el nombre del manifiesto no coincide con la carpeta")
    if not isinstance(manifest.get("version"), str) or not manifest["version"].strip():
        errors.append(f"{plugin_name}: falta version")
    if not manifest.get("description"):
        errors.append(f"{plugin_name}: falta description")
    if "hooks" in manifest:
        errors.append(f"{plugin_name}: plugin.json no admite hooks")
    if "[TODO:" in manifest_path.read_text(encoding="utf-8"):
        errors.append(f"{plugin_name}: el manifiesto contiene un TODO pendiente")

    skills_value = manifest.get("skills")
    skills_path = plugin_path / "skills"
    if skills_value != "./skills/":
        errors.append(f"{plugin_name}: skills debe ser ./skills/")
    if not skills_path.is_dir():
        errors.append(f"{plugin_name}: falta la carpeta skills")
        return errors

    skill_files = sorted(skills_path.glob("*/SKILL.md"))
    if not skill_files:
        errors.append(f"{plugin_name}: no contiene ninguna skill")
    for skill_file in skill_files:
        try:
            metadata = frontmatter(skill_file)
        except (OSError, ValidationError) as exc:
            errors.append(str(exc))
            continue
        folder_name = skill_file.parent.name
        if metadata.get("name") != folder_name:
            errors.append(f"{skill_file.relative_to(ROOT)}: name no coincide con la carpeta")
        if not metadata.get("description"):
            errors.append(f"{skill_file.relative_to(ROOT)}: falta description")
        if "[TODO:" in skill_file.read_text(encoding="utf-8"):
            errors.append(f"{skill_file.relative_to(ROOT)}: contiene un TODO pendiente")
        errors.extend(validate_links(skill_file))

    return errors


def main() -> int:
    errors: list[str] = []
    marketplace = load_json(MARKETPLACE)
    marketplace_name = marketplace.get("name")
    if not isinstance(marketplace_name, str) or not NAME.fullmatch(marketplace_name):
        errors.append("marketplace: name inválido")
    interface = marketplace.get("interface")
    if not isinstance(interface, dict) or not interface.get("displayName"):
        errors.append("marketplace: falta interface.displayName")

    entries = marketplace.get("plugins")
    if not isinstance(entries, list) or not entries:
        errors.append("marketplace: plugins debe ser una lista no vacía")
        entries = []

    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("marketplace: cada plugin debe ser un objeto")
            continue
        name = entry.get("name")
        if isinstance(name, str) and name in seen:
            errors.append(f"marketplace: plugin duplicado: {name}")
        if isinstance(name, str):
            seen.add(name)
        try:
            errors.extend(validate_plugin(entry))
        except ValidationError as exc:
            errors.append(str(exc))

    unlisted = {
        path.name
        for path in (ROOT / "plugins").iterdir()
        if path.is_dir() and (path / ".codex-plugin" / "plugin.json").is_file()
    } - seen
    for name in sorted(unlisted):
        errors.append(f"{name}: existe en plugins/ pero no en el marketplace")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: marketplace {marketplace_name!r}; {len(entries)} plugin(s) válido(s)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
