Here is the vertical slice implementation plan for the AI Workspace Sidecar Controller. I mapped the dependency graph to ensure we build the infrastructure first, then the live execution engine, and finally the configuration savers.

### Dependency Graph & Implementation Plan

| Task | Description & Acceptance Criteria | Verification Steps | Dependencies | Files Touched | Size |
| --- | --- | --- | --- | --- | --- |
| **1. Scaffold Sidecar** | **AC:** `sidecar-ui` directory exists. `Dockerfile.sidecar` contains a lightweight Python image with Streamlit and Docker SDK. `docker-compose.yml` includes the new `sidecar` service mounting `/var/run/docker.sock` and the root folder. | Run `docker compose build sidecar`. It builds successfully without errors. | None | `sidecar-ui/Dockerfile.sidecar`, `sidecar-ui/requirements.txt`, `docker-compose.yml` | S |
| **2. UI Foundation** | **AC:** Streamlit app loads on port 8502. Sidebar displays a green/red connection status by querying the local Docker socket for the `ai_tui_sandbox` state. | Open `localhost:8502`. UI renders. Sidebar shows "Connected" for the sandbox container. | Task 1 | `sidecar-ui/app.py` | S |
| **Checkpoint 1** | **Review core infrastructure and UI shell.** |  |  |  |  |
| **3. Execution Bridge** | **AC:** Python module capable of taking a command string, running it inside `ai_tui_sandbox` via Docker SDK, capturing stdout/stderr, and returning the streams. | Unit test the function with a simple `echo "test"` command targeted at the sandbox. | Task 2 | `sidecar-ui/docker_bridge.py` | M |
| **4. Installer UI** | **AC:** Form accepts package name and ecosystem (`uv`, `conda`). UI displays the exact manual fallback command (e.g., `docker exec -it ai_tui_sandbox uv pip install...`). UI executes the background install and pipes output to a read-only terminal block. | Submit "htop" via `dnf`. Verify fallback command string is correct. Verify terminal block shows live installation logs. | Task 3 | `sidecar-ui/app.py` | M |
| **Checkpoint 2** | **Review live installation mechanism and fallback generator.** |  |  |  |  |
| **5. Text Editors** | **AC:** Functions to safely append text. Appends `RUN ...` under `# --- AI SIDECAR AUTO-INSTALLS ---` in `Dockerfile`. Appends notes under `# Notes` in `README.md`. | Install a test package. Verify `Dockerfile` updates correctly. Save a test note. Verify `README.md` updates. | Task 4 | `sidecar-ui/config_editors.py`, `sidecar-ui/app.py` | S |
| **6. YAML Editors** | **AC:** Functions using `PyYAML` to parse and edit YAML safely. Injects volume mappings into `services.sandbox.volumes` in `docker-compose.yml`. Appends dependencies to `environment.yml`. | Mount a dummy folder via UI. Verify `docker-compose.yml` updates and syntax remains valid. | Task 5 | `sidecar-ui/config_editors.py`, `sidecar-ui/app.py` | M |
| **Checkpoint 3** | **Review configuration persistence and end-to-end integration.** |  |  |  |  |
