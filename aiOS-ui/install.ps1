$ErrorActionPreference = "Stop"

param(
    [switch]$Migrate
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$RootDir = Split-Path -Parent $ScriptDir
$Python = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } elseif (Get-Command py -ErrorAction SilentlyContinue) { "py" } else { throw "Python 3 is required." }

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw "Docker Desktop is required." }
docker compose version | Out-Null
docker info | Out-Null

& $Python "$ScriptDir\scripts\aiosctl.py" --root $RootDir init
& $Python "$ScriptDir\scripts\aiosctl.py" --root $RootDir migrate
if ($Migrate) {
    & $Python "$ScriptDir\scripts\aiosctl.py" --root $RootDir migrate --apply
}

Push-Location $ScriptDir
try {
    docker compose build
    docker compose up -d --wait
} finally {
    Pop-Location
}

$Port = if ($env:AIOS_PORT) { $env:AIOS_PORT } else { "9119" }
Write-Host "aiOS is available at http://127.0.0.1:$Port"
