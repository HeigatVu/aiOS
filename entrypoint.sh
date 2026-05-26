#!/bin/bash
set -e

# Migrate old agent-configs folder to persistent/ if it still exists
if [ -d "/workspace/agent-configs" ]; then
  echo "Found legacy agent-configs/ folder. Migrating to persistent/..."
  # Map of old subdirectories to new subdirectories under /workspace/persistent/
  declare -A MIGRATE_MAP=(
    [".agentmemory"]="agentmemory"
    [".claude"]="claude"
    [".hermes"]="hermes"
    [".gemini"]="gemini"
    [".antigravitycli"]="antigravitycli"
    [".agents"]="agents"
    [".fcc"]="fcc"
    [".iii"]="iii"
  )

  for old_dir in "${!MIGRATE_MAP[@]}"; do
    new_dir="${MIGRATE_MAP[$old_dir]}"
    if [ -d "/workspace/agent-configs/$old_dir" ]; then
      sudo mkdir -p "/workspace/persistent/$new_dir"
      # Move files using sudo to avoid permission issues
      sudo cp -aT "/workspace/agent-configs/$old_dir/" "/workspace/persistent/$new_dir/" 2>/dev/null || true
    fi
  done
  
  # Remove old agent-configs folder completely
  sudo rm -rf "/workspace/agent-configs"
  echo "Migration complete!"
fi

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
  "$HOME/.antigravitycli"
  "$HOME/.agents"
  "$HOME/.fcc"
  "$HOME/.iii"
)

for dir in "${DIRS[@]}"; do
  if [ -d "$dir" ] && [ ! -w "$dir" ]; then
    sudo chown -R "$(id -u):$(id -g)" "$dir"
  fi
done

exec "$@"
