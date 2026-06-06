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
    HERMES_AGENT_DIR="${WORKSPACE_DIR}/persistent/hermes/hermes-agent"
    HERMES_WEBUI_DIR="${WORKSPACE_DIR}/aiOS-ui/hermes-webui"
    echo "💻 Running on the HOST machine."
fi

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
    
    clear_lock "$agent_dir"
    cd "$agent_dir"
    echo "→ Fetching updates..."
    git fetch origin
    
    local has_changes=0
    if ! git diff --quiet || ! git diff --cached --quiet; then
        has_changes=1
        echo "⚠️ Hermes Agent has local changes. Stashing them..."
        git stash
    fi
    
    echo "→ Resetting to origin/main..."
    git reset --hard origin/main
    
    if [ "$has_changes" -eq 1 ]; then
        echo "→ Re-applying your local agent changes..."
        if git stash pop; then
            echo "✅ Local agent changes re-applied successfully."
        else
            echo "⚠️ Conflicts occurred while re-applying local changes."
        fi
    fi
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
            $cmd_prefix git -C "$HERMES_AGENT_DIR" fetch origin
            
            local has_changes=0
            if ! $cmd_prefix git -C "$HERMES_AGENT_DIR" diff --quiet || ! $cmd_prefix git -C "$HERMES_AGENT_DIR" diff --cached --quiet; then
                has_changes=1
                echo "⚠️ Hermes Agent has local changes. Stashing them..."
                $cmd_prefix git -C "$HERMES_AGENT_DIR" stash
            fi
            
            $cmd_prefix git -C "$HERMES_AGENT_DIR" reset --hard origin/main
            
            if [ "$has_changes" -eq 1 ]; then
                echo "→ Re-applying your local agent changes..."
                if $cmd_prefix git -C "$HERMES_AGENT_DIR" stash pop; then
                    echo "✅ Local agent changes re-applied successfully."
                else
                    echo "⚠️ Conflicts occurred while re-applying local changes."
                fi
            fi
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
    
    git fetch origin
    if git remote | grep -q "upstream"; then
        git fetch upstream
    fi

    # Check for local changes
    local has_changes=0
    if ! git diff --quiet || ! git diff --cached --quiet; then
        has_changes=1
        echo "⚠️ Hermes WebUI has local changes. Stashing them..."
        git stash
    fi

    # Determine local active branch
    local active_branch
    active_branch=$(git symbolic-ref --short HEAD 2>/dev/null || echo "master")

    # Determine upstream branch (main or master)
    local upstream_branch="master"
    if git show-ref --quiet refs/remotes/upstream/main || git show-ref --quiet refs/remotes/upstream/master; then
        if git show-ref --quiet refs/remotes/upstream/main; then
            upstream_branch="main"
        else
            upstream_branch="master"
        fi
    elif git show-ref --quiet refs/remotes/origin/main; then
        upstream_branch="main"
    fi

    if git remote | grep -q "upstream"; then
        echo "→ Resetting local branch '${active_branch}' to upstream/${upstream_branch}..."
        git reset --hard "upstream/${upstream_branch}"
        
        echo "→ Pushing updates to your fork (origin/${active_branch})..."
        git push origin "${active_branch}" || echo "⚠️ Could not push to fork automatically. You may need to push manually."
    else
        echo "→ Resetting Hermes WebUI to origin/${upstream_branch}..."
        git reset --hard "origin/${upstream_branch}"
    fi

    if [ "$has_changes" -eq 1 ]; then
        echo "→ Re-applying your local WebUI changes..."
        if git stash pop; then
            echo "✅ Local WebUI changes re-applied successfully."
        else
            echo "⚠️ Conflicts occurred while re-applying local changes. Please resolve them manually in $HERMES_WEBUI_DIR."
        fi
    fi
    echo "✅ Hermes WebUI update process completed."
}

# Run updates
update_agent
echo ""
update_webui
echo ""
echo "🎉 All updates complete!"
