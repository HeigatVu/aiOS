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

exec "$@"
