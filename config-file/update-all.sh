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

update_agent_inside_container() {
    local agent_dir="/home/ai_user/.hermes/hermes-agent"
    
    # Fix dubious ownership since this function is run via docker exec
    git config --global --add safe.directory "$agent_dir" || true
    git config --global url."https://github.com/".insteadOf "git@github.com:" || true
    
    clear_lock "$agent_dir"
    cd "$agent_dir"
    echo "→ Fetching updates..."
    git fetch origin
    
    echo "→ Applying updates (stashing local changes first)..."
    git stash
    git pull origin main || git pull origin master || true
    git stash pop || echo "⚠️ Could not pop stash"
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
            # Execute the commands inside the container
            docker exec -t "${CONTAINER_NAME}" bash -c "$(declare -f clear_lock update_agent_inside_container); update_agent_inside_container"
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
            
            echo "→ Applying updates (stashing local changes first)..."
            $cmd_prefix git -C "$HERMES_AGENT_DIR" stash || true
            $cmd_prefix git -C "$HERMES_AGENT_DIR" pull origin main || $cmd_prefix git -C "$HERMES_AGENT_DIR" pull origin master || true
            $cmd_prefix git -C "$HERMES_AGENT_DIR" stash pop || echo "⚠️ Could not pop stash"
        fi
    fi
    echo "✅ Hermes Agent update process completed."
}

update_webui() {
    echo "⚕ Updating Hermes WebUI..."
    if [ ! -d "$HERMES_WEBUI_DIR" ]; then
        echo "❌ Hermes WebUI directory not found at $HERMES_WEBUI_DIR"
        return 1
    fi

    clear_lock "$HERMES_WEBUI_DIR"

    echo "→ Fetching Hermes WebUI updates..."
    cd "$HERMES_WEBUI_DIR"
    
    # Fix potential permission issues caused by docker volume mapping (e.g. objects owned by 'nobody')
    if [ "$IS_INSIDE_CONTAINER" = false ]; then
        if find .git/objects -type d ! -user "$(whoami)" 2>/dev/null | grep -q .; then
            echo "⚠️ Found git objects with incorrect ownership. Attempting to fix by moving them aside..."
            find .git/objects -maxdepth 2 -type d ! -user "$(whoami)" ! -name "*.bak" -exec mv {} {}.bak \; 2>/dev/null || true
        fi
    fi
    
    # Ensure git user is configured so git stash doesn't fail
    git config user.email "auto-updater@localhost" || true
    git config user.name "Auto Updater" || true
    
    git fetch origin
    if git remote | grep -q "upstream"; then
        echo "→ Fetching updates from upstream..."
        git fetch upstream
    fi
    
    echo "→ Applying updates (stashing local changes first)..."
    git stash
    git pull origin master || true
    git stash pop || echo "⚠️ Could not pop stash (maybe nothing was stashed, or there's a merge conflict)"
    
    echo "✅ Hermes WebUI update process completed."
}

# Run updates
update_agent
echo ""
update_webui
echo ""
echo "🎉 All updates complete!"
