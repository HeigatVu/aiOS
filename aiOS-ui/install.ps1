# ==============================================================================
# aiOS-ui Cross-Platform Auto-Installer (Windows PowerShell)
# ==============================================================================
$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir

Write-Host "🚀 Starting aiOS-ui Setup & Auto-Installer for Windows..." -ForegroundColor Cyan
Write-Host "📂 Project Directory: $ScriptDir" -ForegroundColor Gray

# 1. Check Prerequisite Tools
Write-Host "🔍 Checking Prerequisites..." -ForegroundColor Yellow
if (-not (Get-Command "docker" -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Error: Docker Desktop is not installed or not in PATH." -ForegroundColor Red
    Write-Host "Please install Docker Desktop for Windows: https://docs.docker.com/desktop/install/windows-install/" -ForegroundColor Red
    exit 1
}

try {
    docker info *> $null
} catch {
    Write-Host "❌ Error: Docker daemon is not running." -ForegroundColor Red
    Write-Host "Please start Docker Desktop on your machine and rerun this script." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker Desktop runtime detected." -ForegroundColor Green

# 2. Create Required Host Bind-Mount Directories
Write-Host "📁 Initializing Workspace & Persistence Directories..." -ForegroundColor Yellow
$Directories = @(
    "$RootDir\sandbox-data\working-space",
    "$RootDir\sandbox-data\my-data",
    "$RootDir\sandbox-data\outputs",
    "$RootDir\sandbox-data\home_ai_user",
    "$ScriptDir\persistent\ml-env",
    "$ScriptDir\persistent\uv-cache",
    "$ScriptDir\persistent\conda-pkgs",
    "$ScriptDir\persistent\agentmemory",
    "$ScriptDir\persistent\hermes",
    "$ScriptDir\persistent\mimocode",
    "$ScriptDir\persistent\agents",
    "$ScriptDir\persistent\iii",
    "$ScriptDir\persistent\reasonix",
    "$ScriptDir\config-file\system-config\nvim"
)

foreach ($dir in $Directories) {
    if (-not (Test-Path -Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
    }
}
Write-Host "✅ Directories initialized." -ForegroundColor Green

# 3. Environment File Setup
$EnvFile = Join-Path $ScriptDir ".env"
$EnvExample = Join-Path $ScriptDir ".env.example"
if (-not (Test-Path $EnvFile)) {
    if (Test-Path $EnvExample) {
        Copy-Item -Path $EnvExample -Destination $EnvFile
        Write-Host "📄 Created .env from .env.example" -ForegroundColor Green
    } else {
        Set-Content -Path $EnvFile -Value "USER_ID=1000`nGROUP_ID=1000"
        Write-Host "📄 Generated default .env file." -ForegroundColor Green
    }
}

# 4. Build and Launch Containers
Set-Location -Path $ScriptDir
Write-Host "🐳 Building and starting Docker containers..." -ForegroundColor Cyan
docker compose build
docker compose up -d

Write-Host ""
Write-Host "==========================================================================" -ForegroundColor Green
Write-Host "🎉 aiOS-ui Installation Complete!" -ForegroundColor Green
Write-Host "==========================================================================" -ForegroundColor Green
Write-Host "🌐 Dashboard Web UI:  http://localhost:9119  (or http://localhost:8788)" -ForegroundColor Cyan
Write-Host "💬 Hermes Web UI:     http://localhost:8501" -ForegroundColor Cyan
Write-Host "🧠 AgentMemory:       http://localhost:3113" -ForegroundColor Cyan
Write-Host ""
Write-Host "Attach interactive terminal:  docker compose exec sandbox zsh" -ForegroundColor Yellow
Write-Host "==========================================================================" -ForegroundColor Green
