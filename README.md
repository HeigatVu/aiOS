# Outrider AI: Master AI & Signal Processing Workspace (v2.0)

This repository houses a secure, indestructible, and highly accelerated multi-container workspace designed for AI agents and advanced signal processing. 

By leveraging the **Sidecar Pattern**, it safely isolates the heavy, GPU-accelerated AI sandbox from your host laptop, while providing a stunning, secure web control panel to manage installations and shared directories.

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

The workspace runs two harmoniously connected Docker containers:

```text
my-assistance/
├── Dockerfile                   # Software Blueprint for the AI Sandbox
├── docker-compose.yml           # Core wiring (ports, GPU passthrough, volume mounts)
├── environment.yml              # Deep ML & Signal Processing conda baseline
├── .gitignore                   # Anti-leak key protections & heavy file ignores
├── .dockerignore                 # Excludes heavy folders from the builder
│
├── sidecar-ui/                  # Streamlit Control Panel App (Port 8502)
│   ├── Dockerfile.sidecar       # High-speed uv-based container setup
│   ├── app.py                   # Custom UI dashboard and interactive terminal
│   ├── docker_bridge.py         # Broker for live-streaming docker execution
│   └── config_editors.py        # Surgical code & YAML writers
│
├── working-space/               # Mapped to /workspace (Python code & scripts)
├── data/                        # Mapped to /data (Heavy WAV audio datasets)
└── outputs/                     # Mapped to /outputs (Generated AI results)
```

### Container 1: The AI Sandbox (`ai_tui_sandbox`)
* **Purpose:** The safe-house where AI agents (Gemini, Claude, Hermes, etc.) execute.
* **Privileges:** Strictly isolated; **no** Docker socket access (incapable of escaping to your host machine).
* **Environments:** Pre-activated Conda `ai-baseline` environment, utilizing **`Conda`** for heavy C-libraries and **`uv`** for lightning-fast Python installations.
* **GPU Passthrough:** Safely wires your host RTX graphics card for local model inference.

### Container 2: The Sidecar Controller (`ai_sidecar_controller`)
* **Purpose:** A secure control panel served at `http://localhost:8502` to manage your sandbox.
* **Privileges:** Mounts `/var/run/docker.sock` to securely execute commands inside the sandbox.
* **Features:** Live package installer terminal (for `uv`, `conda`, and `dnf`), dynamic volume folder mapper, and a persistent markdown notebook.

---

## 2. How to Run and Use

### Start the Engine (Power On)
To spin up both containers in the background, run this command from the root folder of your project:
```bash
docker compose up -d
```
*Note: If you run into local DNS/network timeouts, you can bypass BuildKit using `DOCKER_BUILDKIT=0 docker compose up -d --build`.*

### Access the Web Control Panel
Open your browser and navigate to:
👉 **`http://localhost:8502`**

### Enter the Sandbox Terminal
To get a CLI prompt directly inside your active AI sandbox, run:
```bash
docker compose exec -it sandbox /bin/zsh
```

### Stop the Engine (Power Off)
To release all RAM, CPU, and GPU resources at the end of the day, run:
```bash
docker compose down
```

---

## 3. The Dual-Terminal Workflow

This setup establishes a clean separation between your physical Host (Fedora laptop) and the Sandbox (Docker):

| Goal | Done on Host (laptop) | Done inside Sandbox (`docker compose exec`) |
| :--- | :--- | :--- |
| **Start/Stop containers** | Run `docker compose up -d` or `down` | ❌ Never |
| **Run model scripts / execute code** | ❌ Never | Run `python script.py` |
| **Interactive Zsh shell** | Regular OS terminal | Run `zsh` plugin actions |
| **Install pure Python dependencies** | ❌ Never (Do via Sidecar UI) | Run `uv pip install <package>` |
| **Install global system tools** | ❌ Never (Do via Sidecar UI) | Run `sudo dnf install <package>` |

---

## 4. How to Configure in the Dockerfile

The root `Dockerfile` defines the base operating system (Fedora 44), npm tools, conda baselines, and active agents. 

### The Auto-Install Section
To prevent manual configurations from being wiped out when rebuilding containers, the root `Dockerfile` contains a designated marker section:

```dockerfile
# --- AI SIDECAR AUTO-INSTALLS ---
RUN dnf install -y htop && dnf clean all
```

* **How it works:** When you trigger an installation via the **Sidecar Web UI**, the controller surgically injects a new `RUN` layer directly under this marker.
* **Manual edits:** You can safely add custom global operations here by editing the `Dockerfile` in your text editor. Every package listed here will be permanently baked into your image during the next `docker compose build`.

---

## 5. Git Security & Push Safety

To ensure you can safely push your code to **GitHub** without leaking secure API keys or bloating your repository with heavy data files, a custom `.gitignore` has been pre-configured:

* **Protected Folders:** `agent-configs/` (containing secret agent tokens), `data/` (large audio files), and `outputs/` (generated results) are completely ignored.
* **Directory Tracking:** Empty structures of these folders are maintained via `.gitkeep` files, allowing you to share the project setup cleanly.

### Important: Clear Git Cache Before First Push
If you had previously committed files from ignored folders, run this on your Host terminal to clear the index:
```bash
git rm -r --cached .
git add .
git commit -m "chore: secure all private directories and workspaces"
```

---

## 6. Troubleshooting & Edge Cases

* **SELinux Permission Denied:** If an AI agent cannot save credentials inside the mapped folders, make sure the volume mounts in `docker-compose.yml` append the `, z` flag (e.g., `- ./agent-configs/.gemini:/home/ai_user/.gemini:rw, z`), which bypasses host SELinux security rules safely.
* **GPU Connection Failure:** If Docker refuses to start due to CUDA/NVIDIA errors, ensure that `nvidia-container-toolkit` is correctly installed on your host system and the docker daemon is restarted.
* **ResolvePackageNotFound:** If Conda throws package conflicts during a build, open `environment.yml` and delete the strict version suffixes (e.g., change `python=3.12.13=hd63d673_0` to `python=3.12.13`), then rebuild.

---

# Notes

* **[2026-05-26 16:59:49]** Mounted folder mapping '/home/HeigatWorkspace/Downloads:/workspace/Downloads' in docker-compose.yml.


* **[2026-05-25 21:41:46]** Installed package 'htop' via dnf using the Sidecar UI.
