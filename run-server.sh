#!/usr/bin/env bash
# Run the Boxes.py self-host web server.
# Usage: ./run-server.sh [--host HOST] [--port PORT] [extra boxesserver args...]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="${VENV_DIR:-$SCRIPT_DIR/.venv}"
PYTHON_BIN="${PYTHON_BIN:-python3}"

if [[ ! -d "$VENV_DIR" ]]; then
    echo "Creating virtualenv in $VENV_DIR..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

if ! python -c "import affine, markdown, numpy, yaml, qrcode, rectpack, shapely, svgpathtools" >/dev/null 2>&1; then
    echo "Installing Python dependencies..."
    pip install --upgrade pip >/dev/null
    pip install -r requirements.txt
fi

HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8000}"

# Allow overriding host/port via CLI flags; pass everything else through.
ARGS=()
while [[ $# -gt 0 ]]; do
    case "$1" in
        --host) HOST="$2"; shift 2 ;;
        --port) PORT="$2"; shift 2 ;;
        *) ARGS+=("$1"); shift ;;
    esac
done

export PYTHONPATH="$SCRIPT_DIR${PYTHONPATH:+:$PYTHONPATH}"

echo "Starting BoxesServer on http://${HOST}:${PORT}/ ..."
exec python scripts/boxesserver \
    --host "$HOST" \
    --port "$PORT" \
    --static_path "$SCRIPT_DIR/static/" \
    "${ARGS[@]}"
