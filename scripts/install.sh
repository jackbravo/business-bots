#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Uso: bash scripts/install.sh [--update] <plugin>" >&2
}

update_only=false
if [[ "${1:-}" == "--update" ]]; then
  update_only=true
  shift
fi

plugin_name="${1:-}"
if [[ -z "$plugin_name" || $# -ne 1 ]]; then
  usage
  exit 2
fi

for command_name in codex python3; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Falta el comando requerido: $command_name" >&2
    exit 1
  fi
done

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
marketplace_file="$repo_root/.agents/plugins/marketplace.json"

python3 "$repo_root/scripts/validate.py"

marketplace_name="$(python3 - "$marketplace_file" "$plugin_name" <<'PY'
import json
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
plugin = sys.argv[2]
data = json.loads(path.read_text(encoding="utf-8"))
names = {entry.get("name") for entry in data.get("plugins", [])}
if plugin not in names:
    raise SystemExit(f"El plugin {plugin!r} no está registrado en {path}")
print(data["name"])
PY
)"

if [[ "$update_only" == false ]]; then
  codex plugin marketplace add "$repo_root"
fi

codex plugin add "$plugin_name@$marketplace_name"

echo "Instalado $plugin_name@$marketplace_name. Abre un hilo nuevo para probar los cambios."
