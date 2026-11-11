#!/usr/bin/env bash
# Creates a virtual environment, installs dependencies and starts the FastAPI server.
# Usage:  ./run.sh            (or: bash run.sh)
# Options (environment variables):  HOST=0.0.0.0 PORT=9000 RELOAD=0 ./run.sh

set -euo pipefail

# Always run from the project root, wherever the script is called from
cd "$(dirname "$0")"

VENV_DIR="venv"
HOST="${HOST:-127.0.0.1}"
PORT="${PORT:-8002}"
RELOAD="${RELOAD:-1}"   # 1 = auto-reload for development, 0 = off

# --- Checks ---------------------------------------------------------------
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is not installed." >&2
    exit 1
fi

if [ ! -f requirements.txt ]; then
    echo "Error: requirements.txt not found in $(pwd)." >&2
    exit 1
fi

if [ ! -f .env ]; then
    echo "Error: .env not found. Create it with at least:" >&2
    echo "  GROQ_API_KEY=your_key_here" >&2
    exit 1
fi

if ! grep -q '^GROQ_API_KEY=.\+' .env; then
    echo "Error: GROQ_API_KEY is missing or empty in .env." >&2
    exit 1
fi

# --- Virtual environment --------------------------------------------------
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in ./$VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# --- Dependencies (reinstall only when requirements.txt changed) ----------
STAMP="$VENV_DIR/.requirements.md5"
CURRENT_HASH="$(md5sum requirements.txt | cut -d' ' -f1)"

if [ ! -f "$STAMP" ] || [ "$(cat "$STAMP")" != "$CURRENT_HASH" ]; then
    echo "Installing dependencies ..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "$CURRENT_HASH" > "$STAMP"
else
    echo "Dependencies are up to date."
fi

# --- Run the API ----------------------------------------------------------
echo "Starting API at http://$HOST:$PORT  (docs: http://$HOST:$PORT/docs)"

if [ "$RELOAD" = "1" ]; then
    exec uvicorn api:app --host "$HOST" --port "$PORT" --reload
else
    exec uvicorn api:app --host "$HOST" --port "$PORT"
fi