#!/usr/bin/env bash
# Global AI & AGI News Intelligence Platform Launch Script
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PYTHON_BIN="$DIR/backend/.venv/bin/python"

if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

echo "======================================================================"
echo "       GLOBAL AI & AGI NEWS INTELLIGENCE PLATFORM                    "
echo "======================================================================"
echo "[+] Starting platform server on http://127.0.0.1:8000"
echo "[+] Interactive API Documentation: http://127.0.0.1:8000/docs"
echo "======================================================================"

exec $PYTHON_BIN -m uvicorn app.main:app --app-dir "$DIR/backend" --host 127.0.0.1 --port 8000 --reload
