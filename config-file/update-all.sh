#!/usr/bin/env bash
# Update script for Hermes Agent and Hermes WebUI
# This script can be run either on the HOST machine or INSIDE the Docker container.
set -euo pipefail

WORKSPACE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONTAINER_NAME="ai_tui_sandbox"

# Detect if we are running inside the Docker container
if [ -f /.dockerenv ] || [ "${USER:-}" = "ai_user" ]; then
  IS_INSIDE_CONTAINER=true
  HERMES_AGENT_DIR="/home/ai_user/.hermes/hermes-agent"
  HERMES_WEBUI_DIR="/aiOS-ui/hermes-webui"
  echo "🐳 Running INSIDE the Docker container."
else
  IS_INSIDE_CONTAINER=false
  # WORKSPACE_DIR is the config-file directory, so we need to go up one level
  ROOT_DIR="$(dirname "$WORKSPACE_DIR")"
  HERMES_AGENT_DIR="${ROOT_DIR}/persistent/hermes/hermes-agent"
  HERMES_WEBUI_DIR="${ROOT_DIR}/aiOS-ui/hermes-webui"
  echo "💻 Running on the HOST machine."
fi

# Fix git issues inside the container
git config --global --add safe.directory "$HERMES_AGENT_DIR" || true
git config --global --add safe.directory "$HERMES_WEBUI_DIR" || true
# Rewrite SSH URLs to HTTPS so we don't need SSH keys just to fetch
git config --global url."https://github.com/".insteadOf "git@github.com:" || true

# Helper to remove stale lock file
clear_lock() {
  local repo_path="$1"
  local lock_file="${repo_path}/.git/index.lock"
  if [ -f "$lock_file" ]; then
    echo "⚠️ Found stale Git lock file at: $lock_file"
    echo "Removing lock file..."
    rm -f "$lock_file"
  fi
}

safe_git_pull() {
  local repo_dir="$1"
  cd "$repo_dir"

  # Ensure git user is configured so git stash doesn't fail
  git config user.email "auto-updater@localhost" || true
  git config user.name "Auto Updater" || true

  # Reset conflicts if any
  if [ -n "$(git diff --name-only --diff-filter=U)" ]; then
    echo "⚠️ Unresolved merge conflicts detected in $(basename "$repo_dir"). Resetting to HEAD..."
    git reset --hard HEAD
  fi

  # Check if there are local changes to stash
  local has_changes=false
  if ! git diff --quiet || ! git diff --cached --quiet; then
    has_changes=true
  fi

  if [ "$has_changes" = true ]; then
    echo "→ Stashing local changes..."
    git stash
  fi

  echo "→ Pulling updates..."
  # Try to pull main, then master
  if git pull origin main 2>/dev/null || git pull origin master; then
    if [ "$has_changes" = true ]; then
      echo "→ Restoring stashed changes..."
      git stash pop || echo "⚠️ Could not pop stash (conflict occurred, please resolve manually)"
    fi
  else
    echo "❌ Pull failed for $(basename "$repo_dir")."
    if [ "$has_changes" = true ]; then
      git stash pop || true
    fi
    return 1
  fi
}

update_agent_inside_container() {
  local agent_dir="/home/ai_user/.hermes/hermes-agent"

  # Fix dubious ownership since this function is run via docker exec
  git config --global --add safe.directory "$agent_dir" || true
  git config --global url."https://github.com/".insteadOf "git@github.com:" || true

  clear_lock "$agent_dir"
  cd "$agent_dir"
  echo "→ Fetching updates..."
  git fetch origin

  safe_git_pull "$agent_dir"
}

update_webui_inside_container() {
  local webui_dir="/aiOS-ui/hermes-webui"

  # Fix dubious ownership since this function is run via docker exec
  git config --global --add safe.directory "$webui_dir" || true
  git config --global url."https://github.com/".insteadOf "git@github.com:" || true

  clear_lock "$webui_dir"
  cd "$webui_dir"
  echo "→ Fetching updates..."
  git fetch origin
  if git remote | grep -q "upstream"; then
    echo "→ Fetching updates from upstream..."
    git fetch upstream
  fi

  safe_git_pull "$webui_dir"
}

update_agent() {
  echo "⚕ Updating Hermes Agent..."

  if [ "$IS_INSIDE_CONTAINER" = true ]; then
    if [ ! -d "$HERMES_AGENT_DIR" ]; then
      echo "❌ Hermes Agent directory not found at $HERMES_AGENT_DIR"
      return 1
    fi
    update_agent_inside_container
  else
    # Running on the host
    # Check if the Docker container is running
    if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${CONTAINER_NAME}$"; then
      echo "→ Container '${CONTAINER_NAME}' is running. Updating Hermes Agent inside the container..."
      # Execute the commands inside the container with set -e
      if docker exec -t "${CONTAINER_NAME}" bash -c "set -euo pipefail; $(declare -f clear_lock safe_git_pull update_agent_inside_container); update_agent_inside_container"; then
        echo "✅ Hermes Agent update process completed."
      else
        echo "❌ Hermes Agent update process failed."
        return 1
      fi
    else
      echo "⚠️ Container '${CONTAINER_NAME}' is NOT running."
      echo "Updating Hermes Agent locally on host (may require sudo due to permission settings)..."

      # Determine if we need sudo to access or traverse the directory
      local cmd_prefix=""
      if [ ! -x "$(dirname "$HERMES_AGENT_DIR")" ] || [ ! -w "$HERMES_AGENT_DIR" ] 2>/dev/null; then
        echo "🔒 Traversal/write access denied to $HERMES_AGENT_DIR. Using sudo..."
        cmd_prefix="sudo"
      fi

      if ! $cmd_prefix test -d "$HERMES_AGENT_DIR"; then
        echo "❌ Hermes Agent directory not found at $HERMES_AGENT_DIR"
        return 1
      fi

      $cmd_prefix rm -f "${HERMES_AGENT_DIR}/.git/index.lock"
      echo "→ Fetching updates..."
      $cmd_prefix git -C "$HERMES_AGENT_DIR" fetch origin

      if [ -n "$cmd_prefix" ]; then
        if sudo bash -c "set -euo pipefail; $(declare -f safe_git_pull); safe_git_pull \"$HERMES_AGENT_DIR\""; then
          echo "✅ Hermes Agent update process completed."
        else
          echo "❌ Hermes Agent update process failed."
          return 1
        fi
      else
        if safe_git_pull "$HERMES_AGENT_DIR"; then
          echo "✅ Hermes Agent update process completed."
        else
          echo "❌ Hermes Agent update process failed."
          return 1
        fi
      fi
    fi
  fi
}

update_webui() {
  echo "⚕ Updating Hermes WebUI..."

  if [ "$IS_INSIDE_CONTAINER" = true ]; then
    if [ ! -d "$HERMES_WEBUI_DIR" ]; then
      echo "❌ Hermes WebUI directory not found at $HERMES_WEBUI_DIR"
      return 1
    fi
    update_webui_inside_container
  else
    # Running on the host
    # Check if the Docker container is running
    if docker ps --format '{{.Names}}' 2>/dev/null | grep -q "^${CONTAINER_NAME}$"; then
      echo "→ Container '${CONTAINER_NAME}' is running. Updating Hermes WebUI inside the container..."
      # Execute the commands inside the container with set -e
      if docker exec -t "${CONTAINER_NAME}" bash -c "set -euo pipefail; $(declare -f clear_lock safe_git_pull update_webui_inside_container); update_webui_inside_container"; then
        echo "✅ Hermes WebUI update process completed."
      else
        echo "❌ Hermes WebUI update process failed."
        return 1
      fi
    else
      echo "⚠️ Container '${CONTAINER_NAME}' is NOT running."
      echo "Updating Hermes WebUI locally on host (may require sudo due to permission settings)..."

      # Determine if we need sudo to access or traverse the directory
      local cmd_prefix=""
      if [ ! -x "$(dirname "$HERMES_WEBUI_DIR")" ] || [ ! -w "$HERMES_WEBUI_DIR" ] 2>/dev/null; then
        echo "🔒 Traversal/write access denied to $HERMES_WEBUI_DIR. Using sudo..."
        cmd_prefix="sudo"
      fi

      if [ -z "$cmd_prefix" ]; then
        if [ -d "$HERMES_WEBUI_DIR/.git" ] && find "$HERMES_WEBUI_DIR/.git" ! -writable -print -quit 2>/dev/null | grep -q .; then
          echo "🔒 Found files/directories in $HERMES_WEBUI_DIR with restricted write access. Using sudo..."
          cmd_prefix="sudo"
        fi
      fi

      if ! $cmd_prefix test -d "$HERMES_WEBUI_DIR"; then
        echo "❌ Hermes WebUI directory not found at $HERMES_WEBUI_DIR"
        return 1
      fi

      $cmd_prefix rm -f "${HERMES_WEBUI_DIR}/.git/index.lock"
      echo "→ Fetching updates..."
      $cmd_prefix git -C "$HERMES_WEBUI_DIR" fetch origin
      if $cmd_prefix git -C "$HERMES_WEBUI_DIR" remote | grep -q "upstream"; then
        echo "→ Fetching updates from upstream..."
        $cmd_prefix git -C "$HERMES_WEBUI_DIR" fetch upstream
      fi

      if [ -n "$cmd_prefix" ]; then
        if sudo bash -c "set -euo pipefail; $(declare -f safe_git_pull); safe_git_pull \"$HERMES_WEBUI_DIR\""; then
          echo "✅ Hermes WebUI update process completed."
        else
          echo "❌ Hermes WebUI update process failed."
          return 1
        fi
      else
        if safe_git_pull "$HERMES_WEBUI_DIR"; then
          echo "✅ Hermes WebUI update process completed."
        else
          echo "❌ Hermes WebUI update process failed."
          return 1
        fi
      fi
    fi
  fi
}

# Run updates
update_agent
echo ""
update_webui
echo ""
echo "🎉 All updates complete!"
