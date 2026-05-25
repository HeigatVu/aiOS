# File: docs/superpowers/specs/2026-05-26-sidecar-controller-design.md

## 1. Problem Statement & Objective
* **Project:** AI Workspace Sidecar Controller
* **Goal:** Build a lightweight Streamlit web application that serves as a secure, beginner-friendly control panel for the `ai_tui_sandbox`. It enables users to easily install new ML/system tools and manage configurations via a web UI. 
* **Constraint:** It must execute live updates in the sandbox while permanently saving those changes to infrastructure-as-code files (`Dockerfile`, `environment.yml`, `docker-compose.yml`), all while maintaining strict air-gapped security for the AI user.

## 2. High-Level Architecture
The system employs a "Sidecar" pattern to safely separate control-plane privileges from the AI execution environment.

* **The Controller (Streamlit Sidecar):** A new, lightweight Docker service added to `docker-compose.yml`.
    * *Privileges:* Mounts the host's `/var/run/docker.sock` and the `my-assistance/` directory.
    * *Interface:* Serves a web GUI on port `8502`.
* **The Target (AI Sandbox):** The existing `ai_tui_sandbox`.
    * *Privileges:* Strictly isolated; no socket access. Runs the `ai-baseline` as the restricted `ai_user`.
* **The Execution Bridge:** The Sidecar uses the Docker socket to dispatch `docker exec` commands into the Sandbox. 

## 3. UI Design & Core Workflows
The web interface features two primary panels:

* **Left Sidebar (Configuration):** Status indicators for Docker Socket connection and `ai_tui_sandbox` runtime status.
* **Main Panel (Action Center):** * A "Smart Form" for actions (Install Package, Mount Folder, Save Note).
    * **Live Output Terminal:** A read-only text block displaying stdout/stderr of background commands.
    * **Manual Fallback Guide:** A prominent, copyable text box generating the exact manual command (e.g., `docker exec -it ai_tui_sandbox uv pip install <pkg>`) in case the background installation fails and requires interactive debugging.

| Action | User Input | Backend Execution |
| :--- | :--- | :--- |
| **Install Package** | Package name, ecosystem (`uv`, `conda`, `dnf`) | 1. Generates fallback command.<br>2. Fires `docker exec`.<br>3. Pipes output to UI.<br>4. Appends to `Dockerfile` / `environment.yml`. |
| **Mount Folder** | Host Path, Container Path | 1. Loads `docker-compose.yml` via PyYAML.<br>2. Injects volume mapping.<br>3. Flashes UI restart warning. |
| **Save Note** | Text input | 1. Opens `README.md`.<br>2. Appends text under a designated section. |

## 4. File Structure
The controller app is isolated to prevent cluttering the root directory.

```text
my-assistance/
├── Dockerfile                   
├── docker-compose.yml           
├── environment.yml              
├── README.md                    
├── sidecar-ui/                  # NEW: Isolated Controller App
│   ├── Dockerfile.sidecar       # Lightweight Streamlit image
│   ├── requirements.txt         # pyyaml, docker, streamlit
│   └── app.py                   # Main UI logic
└── ... [existing folders]