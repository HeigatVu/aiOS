```python
markdown_content = """# Master AI & Signal Processing Workspace Blueprint (v2.0)

This document serves as the permanent memory and architectural guide for the isolated Docker workspace. It outlines the dual-terminal workflow, the Conda/UV machine learning integration, and the "Etch-A-Sketch" philosophy for maintaining the environment.

## 1. Core Architecture & Directory Structure
The master folder (`my-assistance/`) must maintain the following structure to ensure the environment remains perfectly portable and indestructible:


```

```text
File saved to /mnt/data/ai-workspace-blueprint-v2.md

```text
my-assistance/
│
├── Dockerfile               # Software Blueprint (Fedora, Conda, UV, FFmpeg, baked environment.yml)
├── docker-compose.yml       # Hardware/Network Wiring (GPU passthrough, Volume mounts)
├── environment.yml          # The heavy ML/Signal Processing Conda baseline (PyTorch, CUDA, etc.)
│
├── agent-configs/           # Hidden memory (API keys, tokens, settings)
│   ├── .claude              # Air-gapped from host machine
│   ├── .gemini              # Air-gapped from host machine
│   ├── .zshrc_docker        # Custom Zsh config with Conda auto-activate and Zinit plugins
│   └── ... [other agent config folders]
│
├── working-space/           # Python code, scripts, and local files (Maps to /workspace)
├── data/                    # Heavy audio files, .wav datasets
└── outputs/                 # AI agent generated results

```

## 2. The Dual-Terminal Workflow

This system relies on a strict separation between the physical Host (Fedora laptop) and the Sandbox (Docker).

| Action | Which Terminal? | Command / Usage |
| --- | --- | --- |
| **Turn engine on/off** | **Host (Fedora)** | `docker compose up -d` / `docker compose down` |
| **Enter the workspace** | **Host (Fedora)** | `docker compose exec -it sandbox /bin/zsh` |
| **Run code / Install ML tools** | **Docker Sandbox** | `uv pip install <pkg>`, `conda install <pkg>`, `python script.py` |
| **Manage system files** | **Host (Fedora)** | Regular OS management outside of the `my-assistance` folder |

## 3. Machine Learning Package Management (Conda + uv)

The architecture uses **Conda** to handle heavy C-libraries and **uv** for lightning-fast Python package installation.

* **The Baseline (`ai-baseline`):** The heavy ML environment (containing PyTorch, CUDA, OpenCV, and FFmpeg) is defined in `environment.yml` and is explicitly compiled into the Docker image during `docker compose build`. This prevents needing to re-download 5GB+ of packages if the container crashes.
* **Auto-Activation:** The mapped `.zshrc_docker` file contains the `conda activate ai-baseline` command, ensuring the Zsh terminal drops immediately into the ready-state ML environment upon entry.
* **Installing New Packages:**
* For **pure Python packages** (e.g., pandas, requests): Run `uv pip install <package>` inside the Docker terminal. `uv` automatically detects and injects it directly into the active Conda environment.
* For **C-bound packages** (e.g., new audio codecs): Run `conda install -c conda-forge <package>` inside the Docker terminal.



## 4. Expansion Guide: How to Add Features

Use this matrix to determine which file to modify when expanding the workspace:

| Goal | Target File | Next Command to Apply Changes |
| --- | --- | --- |
| **Install global system tools** (`htop`, `rust`) | `Dockerfile` | `docker compose build && docker compose up -d` |
| **Update heavy ML baseline** (PyTorch, etc.) | `environment.yml` | `docker compose build && docker compose up -d` |
| **Expose a new web app** (Streamlit, Jupyter) | `docker-compose.yml` (`ports:`) | `docker compose down && docker compose up -d` |
| **Persist a new AI Agent's memory** | `docker-compose.yml` (`volumes:`) | `docker compose down && docker compose up -d` |
| **Install daily Python libraries** (`librosa`) | **None** | Run `uv pip install <pkg>` inside the Docker terminal. |

## 5. Troubleshooting & Edge Cases

* **Permission Denied in Agent Folders:** Antigravity or Claude fails to save an OAuth token. Run `sudo chown -R ai_user:ai_user ~/.gemini ~/.claude ...` inside the Docker terminal. *(Host SELinux bypass: append `,z` to volume mounts in `docker-compose.yml`).*
* **GPU Passthrough Fails:** Docker refuses to start due to NVIDIA/device driver errors. Install `nvidia-container-toolkit` on the Host Fedora machine, configure the Docker runtime, and restart the Docker service.
* **"ResolvePackageNotFound" during Conda build:** Conda strict hashes don't match the OS. Open `environment.yml` and delete the strict hash suffixes (e.g., change `python=3.12.13=hd63d673_0` to simply `python=3.12.13`), then rebuild.
* **Ghost CLI commands on Host:** Zsh remembers uninstalled apps. Run `hash -r` in the Host terminal to clear cached execution paths.
"""

file_path = "/mnt/data/ai-workspace-blueprint-v2.md"
with open(file_path, "w") as f:
f.write(markdown_content)
print(f"File saved to {file_path}")

```
Your MD file is ready
[file-tag: code-generated-file-0-1779738968768438545]

I have created an updated `ai-workspace-blueprint-v2.md` file for you. 

This version includes everything from the previous file, plus:
* A complete mapping of your new `environment.yml` and `.zshrc_docker` files.
* The explicit "Dual-Terminal Workflow" guide so the AI knows exactly when to execute commands on the host versus inside the sandbox.
* The rules for using Conda vs. `uv` inside your auto-activated `ai-baseline` environment.
* The specific fix for Conda `ResolvePackageNotFound` hash errors in case you run into them during the build process.

If you ever need assistance expanding this workspace in the future, just drop this file into the chat. The AI will instantly understand your entire architecture, your strict air-gapped setup, and the exact commands needed to help you!

```

# Notes

* **[2026-05-25 21:41:46]** Installed package 'htop' via dnf using the Sidecar UI.
