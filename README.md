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
│   ├── aiOS-ui/                 # Configurations for the UI services
│   │   └── agentmemory/         # agentmemory iii-config.yaml, viewer-proxy.mjs, .env, RESTORATION.md
│   ├── hermes/                  # hermes dashboard-proxy.mjs
│   ├── claude/                  # Claude agent configurations (settings.json, CLAUDE.md, SKILLS_ROUTER.md)
│   ├── gemini/                  # Gemini agent configurations (settings.json, mcp_config.json)
│   ├── fcc/                     # Free Claude Code config template
│   ├── system-config/           # Shell configs (.zshrc, .p10k.zsh), nvim config, entrypoint, & recovery tools
│   │   ├── entrypoint.sh        # Runs on every container start: fixes permissions, starts background services
│   │   ├── recover.sh           # One-shot recovery script for all services
│   │   ├── service_health.py    # Async health checks for all 7 services (runs on terminal login)
│   │   └── RESTORATION.md       # Deep troubleshooting and system restoration log
│   ├── step-to-reconfig.md      # Manual step-by-step reconfiguration instructions
│   └── update-all.sh            # Hermes Agent & WebUI update utility
│
├── aiOS-ui/                     # Web control panel directory
│   ├── dashboard/               # BFF Dashboard (runs on host)
│   │   ├── main.py              # FastAPI BFF backend (port 8787) — routes, permissions & file browser SPA
│   │   ├── start-host.sh        # Host bootstrap script to run the BFF
│   │   └── static/
│   │       └── file-browser/    # Custom File Browser SPA
│   └── hermes-webui/            # Upstream Hermes Web UI submodule (runs on port 8501 inside container)
│       └── server.py            # Hermes Web UI main server entry point
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

### The Sidecar Web Control Panel (BFF Dashboard)

- **Purpose:** Web dashboard running at `http://localhost:8787` on the host, launched via `aiOS-ui/dashboard/start-host.sh`. It proxies to the Vue 3 Hermes Web UI running as a background service inside the sandbox container (port `8501`), and serves the custom File Browser SPA (at `/files`).
- **Views & Capabilities (via Hermes subserver & BFF):**
  - **BFF Dashboard** — Central entry point with quick access to Hermes, AgentMemory, and File Browser.
  - **Hermes SPA** — Multi-agent chat workspace.
  - **Dashboard** — Live CPU / RAM / GPU cards + 5-minute Chart.js history charts, container logs stream, rebuild button.
  - **Terminal** — Package installer (uv / conda / dnf / npm), raw command executor with history, custom snippet bank.
  - **PTY Shell** — Full interactive xterm.js shell session directly into the sandbox.
  - **File Browser** — Browse, upload/download, chmod, rename/move, and configure AI permissions.
  - **Processes & Ports** — Live `ps aux` with CPU/MEM bars + kill, listening ports.
  - **Git** — Branch status, diff viewer, stage-all / commit / push inside the sandbox.
  - **Config** — Dockerfile / README / environment.yml editors, volume mapper, `.env` Manager (multi-file CRUD).

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

1. Start the FastAPI BFF Dashboard on your **host machine**:

   ```bash
   bash aiOS-ui/dashboard/start-host.sh
   ```

2. Open `http://localhost:8787` in your browser.

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

- **Storage**: Mappings are saved in a JSON file at `/config-file/aios-permissions.json` (configured via `FILE_BROWSER_PERMISSIONS_CONFIG` in FastAPI).
- **Permission Levels**:
  - `rw` (Read-Write): Normal access to files and directories.
  - `ro` (Read-Only): Forces files/directories to read-only filesystem modes (`444` for files, `555` for directories).
  - `none` (No Access): Restricts the AI from viewing or accessing the directory/file entirely by setting strict mode permissions (`600` for files, `700` for directories) and filtering these items out of the `/api/files/list` API responses.
- **Longest-Prefix Matching**: If no exact mapping is found for a path, the permissions system resolves the level using a longest-prefix match on parent directories, falling back to `rw` if no rule matches.

---

## 8. Automated Diagnostics, Recovery & Updates

Three critical maintenance utilities are provided inside the container and workspace:

### A. Async Health Checker (`service_health.py`)

Located inside the container at `/config-file/system-config/`, this tool runs concurrently via Python's `asyncio` (stdlib only, zero external dependencies) with a 2-second timeout per probe.

- **Status Table**: It verifies the health of **7 services**: `iii engine`, `agentmemory`, `viewer-proxy`, `hermes dashboard`, `dashboard-proxy`, `fcc-server`, and `hermes gateway`.
- **Interactive Shell Feedback**: Runs automatically on every new terminal login via `~/.zshrc` to show a clean color-coded status table, ensuring any degradation is noticed immediately.

### B. One-Shot Recovery (`recover.sh`)

Located inside the container at `/config-file/system-config/`, when services go down (e.g., after the host computer wakes from sleep or Docker restarts), this script restores everything automatically.

- **Conflict Resolution**: Scans `/proc` to kill any stale or conflicting background processes holding ports (`3113`, `9119`, `8082`).
- **State Restorer**: Restores correct binaries (e.g., pinned `iii` engine), boots all services, registers a fresh watchdog loop, and outputs the final service health table.

### C. Hermes Agent & WebUI Updater (`update-all.sh`)

Located at `/config-file/update-all.sh` (or `config-file/update-all.sh` on the host), this script provides a unified update utility for the Hermes Agent and WebUI submodules.

- **Context-Aware Execution**: Can be safely run either from the **host machine** or **inside the Docker container**. It automatically detects the environment and performs the appropriate actions (e.g., executing commands inside the container using `docker exec` if run from the host when the container is running).
- **Safe Git Management**:
  - Automatically checks for and clears stale Git index locks.
  - Detects local uncommitted changes, stashes them, performs `git reset --hard` to synchronize with `origin/main` (for the Agent) or `upstream/master` (for the WebUI), and then pops/re-applies the stashed changes.
  - Automatically pushes WebUI updates to the user's fork (`origin/master`).
