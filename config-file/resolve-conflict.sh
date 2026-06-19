#!/usr/bin/env bash
set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTAINER_NAME="ai_tui_sandbox"

# Detect if we are running inside the Docker container
if [ -f /.dockerenv ] || [ "${USER:-}" = "ai_user" ]; then
  IS_INSIDE_CONTAINER=true
  HERMES_WEBUI_DIR="/aiOS-ui/hermes-webui"
else
  IS_INSIDE_CONTAINER=false
  ROOT_DIR="$(dirname "$WORKSPACE_DIR")"
  HERMES_WEBUI_DIR="${ROOT_DIR}/aiOS-ui/hermes-webui"
fi

resolve_conflict_inside_container() {
  local webui_dir="/aiOS-ui/hermes-webui"
  cd "$webui_dir"

  echo "→ Resolving conflict in Dockerfile inside the container..."
  python3 -c '
import re
path = "Dockerfile"
with open(path, "r") as f:
    text = f.read()
pattern = r"<<<<<<< HEAD.*?>>>>>>> f1d16714.*?\n"
replacement = "HEALTHCHECK --interval=30s --timeout=8s --start-period=10s --retries=3 \\\n  CMD bash /apptoo/scripts/lib/health_probe.sh localhost 8788 /health 2 >/dev/null || exit 1\n"
new_text = re.sub(pattern, replacement, text, flags=re.DOTALL)
with open(path, "w") as f:
    f.write(new_text)
print("Resolved Dockerfile conflict.")
'

  echo "→ Staging resolved Dockerfile..."
  git add Dockerfile

  echo "→ Continuing git rebase..."
  GIT_EDITOR=true git rebase --continue || echo "⚠️ Rebase continue returned code $?"
}

if [ "$IS_INSIDE_CONTAINER" = true ]; then
  resolve_conflict_inside_container
else
  # Check if container is running
  if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${CONTAINER_NAME}$"; then
    echo "→ Container '${CONTAINER_NAME}' is running. Delegating conflict resolution to container..."
    docker exec -t "${CONTAINER_NAME}" bash -c "set -euo pipefail; $(declare -f resolve_conflict_inside_container); resolve_conflict_inside_container"
  else
    echo "⚠️ Container '${CONTAINER_NAME}' is NOT running."
    echo "Resolving conflict locally on host..."

    # Determine if we need sudo
    local cmd_prefix=""
    if [ ! -w "$HERMES_WEBUI_DIR/Dockerfile" ] 2>/dev/null; then
      cmd_prefix="sudo"
    fi

    echo "→ Resolving conflict in Dockerfile..."
    $cmd_prefix python3 -c '
import re
path = "'"$HERMES_WEBUI_DIR"'/Dockerfile"
with open(path, "r") as f:
    text = f.read()
pattern = r"<<<<<<< HEAD.*?>>>>>>> f1d16714.*?\n"
replacement = "HEALTHCHECK --interval=30s --timeout=8s --start-period=10s --retries=3 \\\n  CMD bash /apptoo/scripts/lib/health_probe.sh localhost 8788 /health 2 >/dev/null || exit 1\n"
new_text = re.sub(pattern, replacement, text, flags=re.DOTALL)
with open(path, "w") as f:
    f.write(new_text)
print("Resolved Dockerfile conflict.")
'

    echo "→ Staging resolved Dockerfile..."
    if [ -n "$cmd_prefix" ]; then
      sudo git -C "$HERMES_WEBUI_DIR" add Dockerfile
      echo "→ Continuing git rebase..."
      sudo env GIT_EDITOR=true git -C "$HERMES_WEBUI_DIR" rebase --continue || echo "⚠️ Rebase continue returned code $?"
    else
      git -C "$HERMES_WEBUI_DIR" add Dockerfile
      echo "→ Continuing git rebase..."
      GIT_EDITOR=true git -C "$HERMES_WEBUI_DIR" rebase --continue || echo "⚠️ Rebase continue returned code $?"
    fi
  fi
fi

echo "✅ Conflict resolution process completed. You can now rerun the update script."
