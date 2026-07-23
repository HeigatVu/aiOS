#!/usr/bin/env bash
# ==============================================================================
# aiOS-ui Cross-Platform Auto-Installer (Linux / macOS / WSL2)
# ==============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting aiOS-ui Setup & Auto-Installer..."
echo "📂 Project Directory: ${SCRIPT_DIR}"

# 1. Check Prerequisite Tools
echo "🔍 Checking Prerequisites..."
if ! command -v docker >/dev/null 2>&1; then
    echo "❌ Error: Docker is not installed or not in PATH."
    echo "Please install Docker Desktop (macOS/Windows) or Docker Engine (Linux): https://docs.docker.com/get-docker/"
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "❌ Error: Docker daemon is not running."
    echo "Please start Docker Desktop or the Docker service and rerun this script."
    exit 1
fi

DOCKER_COMPOSE_CMD=""
if docker compose version >/dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker compose"
elif command -v docker-compose >/dev/null 2>&1; then
    DOCKER_COMPOSE_CMD="docker-compose"
else
    echo "❌ Error: Docker Compose is not installed."
    exit 1
fi

echo "✅ Docker runtime and ${DOCKER_COMPOSE_CMD} detected."

# 2. Create Required Host Bind-Mount Directories
echo "📁 Initializing Workspace & Persistence Directories..."
mkdir -p "${ROOT_DIR}/sandbox-data/working-space"
mkdir -p "${ROOT_DIR}/sandbox-data/my-data"
mkdir -p "${ROOT_DIR}/sandbox-data/outputs"
mkdir -p "${ROOT_DIR}/sandbox-data/home_ai_user"

mkdir -p "${SCRIPT_DIR}/persistent/ml-env"
mkdir -p "${SCRIPT_DIR}/persistent/uv-cache"
mkdir -p "${SCRIPT_DIR}/persistent/conda-pkgs"
mkdir -p "${SCRIPT_DIR}/persistent/agentmemory"
mkdir -p "${SCRIPT_DIR}/persistent/hermes"
mkdir -p "${SCRIPT_DIR}/persistent/mimocode"
mkdir -p "${SCRIPT_DIR}/persistent/agents"
mkdir -p "${SCRIPT_DIR}/persistent/iii"
mkdir -p "${SCRIPT_DIR}/persistent/reasonix"
mkdir -p "${SCRIPT_DIR}/config-file/system-config/nvim"

echo "✅ Directories initialized."

# 3. Environment File Setup
if [ ! -f "${SCRIPT_DIR}/.env" ]; then
    if [ -f "${SCRIPT_DIR}/.env.example" ]; then
        cp "${SCRIPT_DIR}/.env.example" "${SCRIPT_DIR}/.env"
        echo "📄 Created .env from .env.example"
    else
        USER_ID=$(id -u 2>/dev/null || echo 1000)
        GROUP_ID=$(id -g 2>/dev/null || echo 1000)
        cat <<EOF > "${SCRIPT_DIR}/.env"
USER_ID=${USER_ID}
GROUP_ID=${GROUP_ID}
EOF
        echo "📄 Generated default .env file."
    fi
fi

# 4. Build and Launch Containers
cd "${SCRIPT_DIR}"
echo "🐳 Building and starting Docker container..."
${DOCKER_COMPOSE_CMD} build
${DOCKER_COMPOSE_CMD} up -d

echo ""
echo "=========================================================================="
echo "🎉 aiOS-ui Installation Complete!"
echo "=========================================================================="
echo "🌐 Dashboard Web UI:  http://localhost:9119  (or http://localhost:8788)"
echo "💬 Hermes Web UI:     http://localhost:8501"
echo "🧠 AgentMemory:       http://localhost:3113"
echo ""
echo "Attach interactive terminal:  make shell  (or ${DOCKER_COMPOSE_CMD} exec sandbox zsh)"
echo "=========================================================================="
