#!/bin/bash
set -e

# Fix ownership of bind-mounted directories.
DIRS=(
  "$HOME/.cache/uv"
  "$HOME/miniconda3/envs/ai-baseline"
  "$HOME/miniconda3/pkgs"
  "$HOME/.agentmemory"
  "$HOME/.claude"
  "$HOME/.hermes"
  "$HOME/.gemini"
  "$HOME/.agents"
  "$HOME/.fcc"
  "$HOME/.iii"
  "$HOME/.feynman"
)
for dir in "${DIRS[@]}"; do
  if [ -d "$dir" ] && [ ! -w "$dir" ]; then
    sudo chown -R "$(id -u):$(id -g)" "$dir"
  fi
done

# Build the Conda ai-baseline env on first launch if the bind-mount is empty.
ENV_DIR="$HOME/miniconda3/envs/ai-baseline"
if [ ! -f "$ENV_DIR/conda-meta/history" ]; then
  echo "[entrypoint] Building Conda env 'ai-baseline' (first launch — slow)..."
  "$HOME/miniconda3/bin/conda" env create -f "$HOME/environment.yml" -p "$ENV_DIR" ||
    echo "[entrypoint] WARNING: conda env create failed — continuing without it."
fi

# ── agentmemory ───────────────────────────────────────────────────────────────

# Copy saved config so agentmemory starts with the right flags and data path.
if [ -f /config-file/agentmemory/.env ]; then
  cp /config-file/agentmemory/.env "$HOME/.agentmemory/.env"
  echo "[entrypoint] agentmemory .env copied"
fi
if [ -f /config-file/agentmemory/iii-config.yaml ]; then
  sudo cp /config-file/agentmemory/iii-config.yaml \
    /usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml
  echo "[entrypoint] iii-config.yaml copied"
fi
mkdir -p "$HOME/.agentmemory/data"

# Install the patched viewer-proxy (rewrites Host header for LAN access).
if [ -f /config-file/agentmemory/viewer-proxy.mjs ]; then
  cp /config-file/agentmemory/viewer-proxy.mjs "$HOME/.agentmemory/viewer-proxy.mjs"
  echo "[entrypoint] viewer-proxy.mjs (patched) installed"
fi

# Start agentmemory if not already running.
if [ ! -f "$HOME/.agentmemory/iii.pid" ] || ! kill -0 "$(cat "$HOME/.agentmemory/iii.pid" 2>/dev/null)" 2>/dev/null; then
  agentmemory start >>"$HOME/.agentmemory/agentmemory.log" 2>&1
  echo "[entrypoint] agentmemory started"
  sleep 4
fi

# Start viewer proxy if not already running.
PROXY="$HOME/.agentmemory/viewer-proxy.mjs"
PROXY_PID_FILE="$HOME/.agentmemory/viewer-proxy.pid"
if [ -f "$PROXY" ]; then
  if [ ! -f "$PROXY_PID_FILE" ] || ! kill -0 "$(cat "$PROXY_PID_FILE" 2>/dev/null)" 2>/dev/null; then
    nohup node "$PROXY" >>"$HOME/.agentmemory/viewer-proxy.log" 2>&1 &
    echo $! >"$PROXY_PID_FILE"
    echo "[entrypoint] viewer-proxy started (PID $!)"
  fi
fi

# ── hermes dashboard ──────────────────────────────────────────────────────────

HERMES_DASH_PID=/tmp/hermes-dashboard.pid
if [ ! -f "$HERMES_DASH_PID" ] || ! kill -0 "$(cat "$HERMES_DASH_PID" 2>/dev/null)" 2>/dev/null; then
  hermes dashboard --no-open >>"$HOME/.hermes/logs/dashboard.log" 2>&1 &
  echo $! >"$HERMES_DASH_PID"
  echo "[entrypoint] hermes dashboard started (PID $!)"
  sleep 4
fi

HERMES_PROXY=/config-file/hermes/dashboard-proxy.mjs
HERMES_PROXY_PID=/tmp/hermes-proxy.pid
if [ -f "$HERMES_PROXY" ]; then
  if [ ! -f "$HERMES_PROXY_PID" ] || ! kill -0 "$(cat "$HERMES_PROXY_PID" 2>/dev/null)" 2>/dev/null; then
    nohup node "$HERMES_PROXY" >>/tmp/hermes-proxy.log 2>&1 &
    echo $! >"$HERMES_PROXY_PID"
    echo "[entrypoint] hermes dashboard-proxy started (PID $!)"
  fi
fi

# ─────────────────────────────────────────────────────────────────────────────

exec "$@"
