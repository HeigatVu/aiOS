# aiOS: Agent Intelligence Operating System for Workspace (v2.0)

<div align="center">
  <img src="./aiOS-ui/assets/dashboard.png" alt="aiOS Main Dashboard" width="800"/>
</div>

This repository houses a secure, GPU-accelerated workspace for AI agents.

By leveraging the **Sidecar Pattern**, it isolates the heavy AI sandbox from your host machine while providing a web control panel in the background to manage installations, file permissions, and shared directories.

## 🖼️ Features & Screenshots

### Multi-pane Workspace Terminals

### Secure File Browser

Browse, manage files, and configure AI read/write boundaries visually.

<img src="./aiOS-ui/assets/file-browser.png" alt="File Browser" width="800"/>

### File & Folder Context Menu Actions

Right-click any file or directory in the workspace browser to run quick terminal operations. Includes natural-language actions like **Open Directory**, **Edit File**, and **View File**, which automatically determine the target terminal pane and run the corresponding commands. Features viewport collision detection to flip submenus to the left if opened near the screen's right edge.

<img src="./aiOS-ui/assets/file-folder-terminal-feature.png" alt="File & Folder Context Menu" width="800"/>

## Step to do

Navigate to `aiOS-ui` and run:

```bash
cd aiOS-ui && make down && make build && make up
```

- Then attach to the container and verify:

```bash
cd aiOS-ui && make shell
```

- If all three pass, everything works. If anything fails, run the automated recovery script inside the container:

```bash
bash /config-file/system-config/recover.sh
```

Or paste into a new Codex session:

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
├── .gitignore                   # Anti-leak protections & heavy file ignores
├── README.md                    # Root workspace documentation
│
├── sandbox-data/                # Docker bind-mounts for persistent working files
│   ├── working-space/           # Mapped to /workspace (code & scripts)
│   ├── my-data/                 # Mapped to /my-data (heavy datasets — read-only, gitignored)
│   └── outputs/                 # Mapped to /outputs (generated results — gitignored)
│
└── aiOS-ui/                     # Main Web control panel & Docker project root
    ├── Dockerfile               # Software blueprint for the AI sandbox & tools
    ├── docker-compose.yml       # Core wiring (ports, GPU passthrough, volume mounts)
    ├── Makefile                 # Build/run shortcuts — auto-detects your UID/GID
    ├── environment.yml          # Deep ML & signal processing conda baseline
    │
    ├── config-file/             # Persistent configs bind-mounted into the container
    │   ├── aiOS-ui/             # Configurations for the UI services
    │   ├── hermes/              # hermes dashboard-proxy.mjs
    │   ├── system-config/       # Shell configs, nvim config, entrypoint, & recovery tools
    │   └── update-all.sh        # Hermes Agent & WebUI update utility
    │
    ├── persistent/              # Persistent runtime storage & user settings
    │
    └── features/                # Application feature services
        ├── dashboard/           # FastAPI BFF Dashboard (runs on host/container port 8788)
        └── hermes-webui/        # Hermes WebUI application (server.py on port 8501)
```
