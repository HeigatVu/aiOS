# aiOS: Agent Intelligence Operating System for Workspace (v2.0)

This repository houses a secure, GPU-accelerated workspace for AI agents.

By leveraging the **Sidecar Pattern**, it isolates the heavy AI sandbox from your host machine while providing a web control panel in the background to manage installations, file permissions, and shared directories.

## Step to do

```bash
make down && make build && make up
```

- Then attach to the container and verify:

```bash
make shell
```

- Once inside, check:

```bash
  iii --version          # expect 0.11.2 (set by AGENTMEMORY_III_VERSION)
  agentmemory status     # expect Health: ✓ healthy
  claude auth status     # expect "loggedIn": true
```

- If all three pass, everything works. If anything fails, run the automated recovery script inside the container:

```bash
bash /config-file/system-config/recover.sh
```

Or paste into a new Claude Code session:

```text
Read /config-file/step-to-reconfig.md and execute every step in order.
```

---

## 📖 Table of Contents

1. [What is Contained in the Project](#1-what-is-contained-in-the-project)
2. [How to Run and Use](#2-how-to-run-and-use)
3. [The Dual-Terminal Workflow](#3-the-dual-terminal-workflow)
4. [How to Configure in the Dockerfile](#4-how-to-configure-in-the-dockerfile)
5. [Git Security & Push Safety](#5-git-security--push-safety)
6. [Troubleshooting & Edge Cases](#6-troubleshooting--edge-cases)
7. [Secure AI Permissions Boundary](#7-secure-ai-permissions-boundary)
8. [Automated Diagnostics & Recovery](#8-automated-diagnostics--recovery)

---

## 1. What is Contained in the Project

```text
my-assistance/
├── Dockerfile                   # Software blueprint for the AI sandbox & tools
├── docker-compose.yml           # Core wiring (ports, GPU passthrough, volume mounts)
├── Makefile                     # Build/run shortcuts — auto-detects your UID/GID
├── environment.yml              # Deep ML & signal processing conda baseline
├── .gitignore                   # Anti-leak protections & heavy file ignores
├── .dockerignore                # Excludes heavy folders from the builder
│
├── sandbox-data/                # Docker bind-mounts for persistent working files
│   ├── working-space/           # Mapped to /workspace (code & scripts)
│   ├── my-data/                 # Mapped to /my-data (heavy datasets — read-only, gitignored)
│   └── outputs/                 # Mapped to /outputs (generated results — gitignored)
│
├── config-file/                 # Persistent configs bind-mounted into the container
│   ├── aiOS-ui/agentmemory/     # agentmemory iii-config.yaml, viewer-proxy.mjs
│   ├── hermes/                  # hermes dashboard-proxy.mjs
│   ├── system-config/           # Shell configs (.zshrc, .p10k.zsh), nvim config, entrypoint, & recovery tools
│   │   ├── entrypoint.sh        # Runs on every container start: fixes permissions, starts background services
│   │   ├── recover.sh           # One-shot recovery script for all services
│   │   ├── service_health.py    # Async health checks for all 7 services (runs on terminal login)
│   │   └── RESTORATION.md       # Deep troubleshooting and system restoration log
│   └── step-to-reconfig.md      # Manual step-by-step reconfiguration instructions
│
├── aiOS-ui/                     # Web control panel (port 8501) — FastAPI + Vue 3 Hermes wrapper
│   ├── main.py                  # FastAPI BFF app — all API routes + custom File Browser endpoints
│   ├── server.py                # Hermes Web UI main server entry point
│   ├── api/                     # Backend implementation modules (auth, workspace, session lifecycle, etc.)
│   └── static/                  # Vue 3 SPA frontend files (chat, settings, terminal, etc.)
│       └── file-browser/        # Custom file browser SPA (accessible at /files)
│
└── persistent/                  # Heavy caches & credentials (gitignored, bind-mounted)
    ├── ml-env/                  # Conda environment cache
    ├── uv-cache/                # Astral uv package installer cache
    ├── conda-pkgs/              # Conda package download cache
    └── [agent directories]/     # Persistent settings for Claude, Gemini, Hermes, AgentMemory, etc.
```

### The AI Sandbox (`ai_tui_sandbox`)

- **Purpose:** Where AI agents (Gemini, Claude, Hermes, agentmemory, etc.) run in a secure, isolated workspace.
- **Privileges:** Strictly isolated — no Docker socket access.
- **User:** Runs as your host UID/GID (auto-detected by Makefile) so bind-mount files are always owned by you.
- **Environments:** Pre-activated Conda `ai-baseline` env, plus `uv` for fast Python installs.
- **GPU Passthrough:** Wires your host NVIDIA GPU for local model inference.

### The Sidecar Web Control Panel

- **Purpose:** Web control panel at `http://localhost:8501` — FastAPI backend + Vue 3 Hermes SPA running as a background service inside the sandbox container.
- **Views:**
  - **Dashboard** — live CPU / RAM / GPU cards + 5-minute Chart.js history charts, container logs stream, rebuild button
  - **Terminal** — package installer (uv / conda / dnf / npm), raw command executor with history, custom snippet bank
  - **PTY Shell** — full interactive xterm.js shell session directly into the sandbox
  - **File Browser** — browse, upload/download, chmod, rw/ro toggle, volume detach, and configure AI permissions
  - **Processes & Ports** — live `ps aux` with CPU/MEM bars + kill, listening ports
  - **Git** — branch status, diff viewer, stage-all / commit / push inside the sandbox
  - **Config** — Dockerfile / README / environment.yml editors, volume mapper, `.env` Manager (multi-file CRUD)

---

## 2. How to Run and Use

All commands are run from the project root on the **host machine**.

### Start the Engine

```bash
make up
```

Builds the image (if needed) with your current UID/GID, then starts the sandbox container in the background.

> If you see DNS/network timeouts during build:
>
> ```bash
> docker compose build --no-cache && make up
> ```

### Access the Web Control Panel

Open `http://localhost:8501` in your browser.

### Enter the Sandbox Terminal

```bash
make shell
```

### Other useful commands

```bash
make build     # Rebuild the image without starting
make down      # Stop and remove containers
make restart   # Restart just the sandbox
make logs      # Tail sandbox logs
```

### Stop the Engine

```bash
make down
```

---

## 3. The Dual-Terminal Workflow

| Goal | Done on Host | Done inside Sandbox (`make shell`) |
| :--- | :--- | :--- |
| **Start/Stop containers** | `make up` / `make down` | ❌ Never |
| **Run scripts / execute code** | ❌ Never | `python script.py` |
| **Install Python packages** | ❌ (use Sidecar UI) | `uv pip install <pkg>` |
| **Install system tools** | ❌ (use Sidecar UI) | `sudo dnf install <pkg>` |
| **Edit configs (.zshrc, nvim)** | Edit files in `config-file/system-config/` | Changes reflect immediately |
| **Restore agentmemory/hermes** | ❌ | Run `bash /config-file/system-config/recover.sh` or follow `/config-file/step-to-reconfig.md` |

---

## 4. How to Configure in the Dockerfile

The root `Dockerfile` defines the base OS (Fedora 44), global npm tools, conda baselines, and AI agents.

### The Auto-Install Section

To permanently add system packages, edit the marker section in `Dockerfile`:

```dockerfile
# --- AI SIDECAR AUTO-INSTALLS ---
RUN dnf install -y htop && dnf clean all
```

When you trigger an install via the **Sidecar Web UI**, the controller injects a new `RUN` layer under this marker. You can also add lines manually — they are baked into the image on the next `make build`.

### UID/GID Matching

The Makefile automatically passes your current user's `UID` and `GID` as build args, so `ai_user` inside the container shares your host identity. Files written in any bind-mounted directory are always owned by you on the host.

---

## 5. Git Security & Push Safety

The `.gitignore` protects sensitive and heavy content:

- **Gitignored:** `data/`, `outputs/`, `persistent/` (agent credentials, Conda env, caches), `.env`
- **Tracked:** Empty directory stubs via `.gitkeep`, all config files in `config-file/`

### Clear Git Cache Before First Push

If you previously committed files that are now ignored:

```bash
git rm -r --cached .
git add .
git commit -m "chore: secure all private directories and workspaces"
```

---

## 6. Troubleshooting & Edge Cases

- **SELinux Permission Denied:** Volume mounts use the `:z` flag in `docker-compose.yml` to relabel SELinux contexts. If an agent can't write credentials, verify the mount entry ends with `:rw,z`.
- **File ownership issues on host:** Always run Docker via `make up` — it exports the correct UID/GID. If you ran `docker compose up` directly without exporting `UID`/`GID`, files may be owned by the wrong user; fix with `sudo chown -R $(id -u):$(id -g) persistent/ config-file/`.
- **GPU Connection Failure:** Ensure `nvidia-container-toolkit` is installed on the host and the Docker daemon is restarted after toolkit setup.
- **ResolvePackageNotFound (Conda):** Open `environment.yml`, remove strict version build strings (e.g., change `python=3.12.13=hd63d673_0` to `python=3.12.13`), then `make build`.
- **agentmemory or hermes not healthy after rebuild:** Open a sandbox shell (`make shell`) and run the automated recovery script: `bash /config-file/system-config/recover.sh`. If that fails, follow the manual steps in `/config-file/step-to-reconfig.md`.

---

## 7. Secure AI Permissions Boundary

The Sidecar Web UI includes an **AI Permissions** system designed to restrict what AI agents running inside the Docker sandbox are allowed to see or edit.

- **Storage**: Mappings are saved in a JSON file at `/tmp/aios-permissions.json` (configured via `FILE_BROWSER_PERMISSIONS_CONFIG` in FastAPI).
- **Permission Levels**:
  - `rw` (Read-Write): Normal access to files and directories.
  - `ro` (Read-Only): Forces files/directories to read-only filesystem modes (`444` for files, `555` for directories).
  - `none` (No Access): Restricts the AI from viewing or accessing the directory/file entirely by setting strict mode permissions (`600` for files, `700` for directories) and filtering these items out of the `/api/files/list` API responses.
- **Longest-Prefix Matching**: If no exact mapping is found for a path, the permissions system resolves the level using a longest-prefix match on parent directories, falling back to `rw` if no rule matches.

---

## 8. Automated Diagnostics & Recovery

Two critical maintenance utilities are provided inside the container at `/config-file/system-config/`:

### A. Async Health Checker (`service_health.py`)

This tool runs concurrently via Python's `asyncio` (stdlib only, zero external dependencies) with a 2-second timeout per probe.

- **Status Table**: It verifies the health of **7 services**: `iii engine`, `agentmemory`, `viewer-proxy`, `hermes dashboard`, `dashboard-proxy`, `fcc-server`, and `hermes gateway`.
- **Interactive Shell Feedback**: Runs automatically on every new terminal login via `~/.zshrc` to show a clean color-coded status table, ensuring any degradation is noticed immediately.

### B. One-Shot recovery (`recover.sh`)

When services go down (e.g., after the host computer wakes from sleep or Docker restarts), this script restores everything automatically.

- **Conflict Resolution**: Scans `/proc` to kill any stale or conflicting background processes holding ports (`3113`, `9119`, `8082`).
- **State Restorer**: Restores correct binaries (e.g., pinned `iii` engine), boots all services, registers a fresh watchdog loop, and outputs the final service health table.
