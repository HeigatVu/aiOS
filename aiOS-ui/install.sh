#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
PYTHON_BIN="${PYTHON_BIN:-python3}"
MIGRATE=0

for argument in "$@"; do
  case "$argument" in
    --migrate) MIGRATE=1 ;;
    --no-migrate) MIGRATE=0 ;;
    *) echo "Unknown option: $argument" >&2; exit 2 ;;
  esac
done

command -v "$PYTHON_BIN" >/dev/null 2>&1 || { echo "Python 3 is required." >&2; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "Docker is required." >&2; exit 1; }
docker compose version >/dev/null 2>&1 || { echo "Docker Compose v2 is required." >&2; exit 1; }
docker info >/dev/null 2>&1 || { echo "Docker daemon is not running." >&2; exit 1; }

"$PYTHON_BIN" "$SCRIPT_DIR/scripts/aiosctl.py" --root "$ROOT_DIR" init
"$PYTHON_BIN" "$SCRIPT_DIR/scripts/aiosctl.py" --root "$ROOT_DIR" migrate
if [[ "$MIGRATE" -eq 1 ]]; then
  "$PYTHON_BIN" "$SCRIPT_DIR/scripts/aiosctl.py" --root "$ROOT_DIR" migrate --apply
fi

cd "$SCRIPT_DIR"
docker compose build
docker compose up -d --wait
printf 'aiOS is available at http://127.0.0.1:%s\n' "${AIOS_PORT:-9119}"
