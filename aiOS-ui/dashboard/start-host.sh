#!/bin/bash
# Setup Python environment on the host and run BFF
cd "$(dirname "$0")"

if [ ! -d ".venv-host" ]; then
  echo "Setting up Python virtual environment (.venv-host) on the host..."
  python3 -m venv .venv-host
  .venv-host/bin/pip install --upgrade pip
fi

.venv-host/bin/pip install fastapi uvicorn httpx websockets

echo "Starting FastAPI BFF Dashboard on host (port 8787)..."
export HERMES_SUB_HOST=127.0.0.1
export HERMES_SUB_PORT=8501

exec .venv-host/bin/python main.py
