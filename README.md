# aiOS: AI OS for Workspace (v2.0)

This repository houses a secure, GPU-accelerated multi-container workspace for AI agents and advanced signal processing.

By leveraging the **Sidecar Pattern**, it isolates the heavy AI sandbox from your host machine while providing a web control panel to manage installations and shared directories.

---

## 📖 Table of Contents

1. [What is Contained in the Project](#1-what-is-contained-in-the-project)
2. [How to Run and Use](#2-how-to-run-and-use)
3. [The Dual-Terminal Workflow](#3-the-dual-terminal-workflow)
4. [How to Configure in the Dockerfile](#4-how-to-configure-in-the-dockerfile)
5. [Git Security & Push Safety](#5-git-security--push-safety)
6. [Troubleshooting & Edge Cases](#6-troubleshooting--edge-cases)

---

## 1. What is Contained in the Project

```text
my-assistance/
├── Dockerfile                   # Software blueprint for the AI sandbox
├── docker-compose.yml           # Core wiring (ports, GPU passthrough, volume mounts)
├── Makefile                     # Build/run shortcuts — auto-detects your UID/GID
├── .env                         # UID/GID override (gitignored; Makefile fills this automatically)
├── entrypoint.sh                # Runs on every container start: fixes permissions, starts services
├── environment.yml              # Deep ML & signal processing conda baseline
├── .gitignore                   # Anti-leak protections & heavy file ignores
├── .dockerignore                # Excludes heavy folders from the builder
│
├── config-file/                 # Persistent configs bind-mounted into the container
│   ├── agentmemory/             # agentmemory .env, iii-config.yaml, viewer-proxy.mjs
│   ├── hermes/                  # hermes dashboard-proxy.mjs
│   ├── system-config/           # .zshrc, .p10k.zsh, nvim config
│   └── prompt-to-fix.md        # Paste-in prompt for Claude after a container rebuild
│
├── sidecar-ui/                  # Streamlit control panel (port 8502)
│   ├── Dockerfile.sidecar
│   ├── app.py
│   ├── docker_bridge.py
│   └── config_editors.py
│
├── working-space/               # Mapped to /workspace (code & scripts)
├── data/                        # Mapped to /data (heavy datasets — gitignored)
└── outputs/                     # Mapped to /outputs (generated results — gitignored)
```

### Container 1: The AI Sandbox (`ai_tui_sandbox`)

* **Purpose:** Where AI agents (Gemini, Claude, Hermes, agentmemory, etc.) run.
* **Privileges:** Strictly isolated — no Docker socket access.
* **User:** Runs as your host UID/GID (auto-detected by Makefile) so bind-mount files are always owned by you.
* **Environments:** Pre-activated Conda `ai-baseline` env, plus `uv` for fast Python installs.
* **GPU Passthrough:** Wires your host NVIDIA GPU for local model inference.

### Container 2: The Sidecar Controller (`ai_sidecar_controller`)

* **Purpose:** Web control panel at `http://localhost:8502`.
* **Privileges:** Mounts `/var/run/docker.sock` to execute commands inside the sandbox.
* **Features:** Live package installer terminal, dynamic volume folder mapper, persistent markdown notebook.

---

## 2. How to Run and Use

All commands are run from the project root on the **host machine**.

### Start the Engine

```bash
make up
```

Builds the image (if needed) with your current UID/GID, then starts both containers in the background.

> If you see DNS/network timeouts during build:
>
> ```bash
> docker compose build --no-cache && make up
> ```

### Access the Web Control Panel

Open `http://localhost:8502` in your browser.

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
| **Restore agentmemory/hermes** | ❌ | Paste prompt from `config-file/prompt-to-fix.md` into Claude Code |

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

* **Gitignored:** `data/`, `outputs/`, `persistent/` (agent credentials, Conda env, caches), `.env`
* **Tracked:** Empty directory stubs via `.gitkeep`, all config files in `config-file/`

### Clear Git Cache Before First Push

If you previously committed files that are now ignored:

```bash
git rm -r --cached .
git add .
git commit -m "chore: secure all private directories and workspaces"
```

---

## 6. Troubleshooting & Edge Cases

* **SELinux Permission Denied:** Volume mounts use the `:z` flag in `docker-compose.yml` to relabel SELinux contexts. If an agent can't write credentials, verify the mount entry ends with `:rw,z`.
* **File ownership issues on host:** Always run Docker via `make up` — it exports the correct UID/GID. If you ran `docker compose up` directly without exporting `UID`/`GID`, files may be owned by the wrong user; fix with `sudo chown -R $(id -u):$(id -g) persistent/ config-file/`.
* **GPU Connection Failure:** Ensure `nvidia-container-toolkit` is installed on the host and the Docker daemon is restarted after toolkit setup.
* **ResolvePackageNotFound (Conda):** Open `environment.yml`, remove strict version build strings (e.g., change `python=3.12.13=hd63d673_0` to `python=3.12.13`), then `make build`.
* **agentmemory or hermes not healthy after rebuild:** Open a sandbox shell (`make shell`) and paste the prompt from `config-file/prompt-to-fix.md` into Claude Code.
