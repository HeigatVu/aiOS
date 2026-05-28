#!/bin/bash
set -e

# Fix ownership of bind-mounted directories.
# Docker creates host dirs as root when they don't exist,
# so mounted paths may not be writable by ai_user.
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
  echo "[entrypoint] Building Conda env 'ai-baseline' from environment.yml (first launch — slow)..."
  "$HOME/miniconda3/bin/conda" env create -f "$HOME/environment.yml" -p "$ENV_DIR" ||
    echo "[entrypoint] WARNING: conda env create failed — continuing without it."
fi

# Auto-start agentmemory if not already running.
if [ ! -f "$HOME/.agentmemory/iii.pid" ] || ! kill -0 "$(cat "$HOME/.agentmemory/iii.pid" 2>/dev/null)" 2>/dev/null; then
  nohup agentmemory >>"$HOME/.agentmemory/agentmemory.log" 2>&1 &
  echo "[entrypoint] agentmemory started (bg)"
fi

# Auto-start TCP proxy so viewer is reachable outside Docker.
# Binds to container eth0 IP:3113 -> 127.0.0.1:3113 (viewer allowlist accepts Host: localhost:3113).
PROXY="$HOME/.agentmemory/viewer-proxy.mjs"
PROXY_PID_FILE="$HOME/.agentmemory/viewer-proxy.pid"
if [ -f "$PROXY" ]; then
  if [ ! -f "$PROXY_PID_FILE" ] || ! kill -0 "$(cat "$PROXY_PID_FILE" 2>/dev/null)" 2>/dev/null; then
    nohup node "$PROXY" >>"$HOME/.agentmemory/viewer-proxy.log" 2>&1 &
    echo $! >"$PROXY_PID_FILE"
    echo "[entrypoint] viewer-proxy started (bg, PID $!)"
  fi
fi

exec "$@"
