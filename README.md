# aiOS

aiOS is a local Docker workspace for AI tools. The control dashboard and Hermes WebUI run as Compose services. AgentMemory and CodeGraph run inside the shared `agent-runtime` container alongside Codex, MiMo, Reasonix, and other agent CLIs. Only the control dashboard is exposed to the host by default.

## Install

Prerequisites: Docker Engine or Docker Desktop with Compose v2, plus Python 3 on the host.

```bash
cd aiOS-ui
make install
```

The installer initializes the data directories, previews legacy state it found, builds images, starts the stack, waits for health checks, and prints the local URL:

```text
http://127.0.0.1:9119
```

To copy data from the former `aiOS-ui/persistent` layout after reviewing the preview:

```bash
cd aiOS-ui
bash install.sh --migrate
```

On Windows PowerShell:

```powershell
cd aiOS-ui
.\install.ps1
.\install.ps1 -Migrate
```

## Daily Commands

```bash
cd aiOS-ui
make up       # Start and wait for healthy services
make down     # Stop the stack
make logs     # Follow all service logs
make shell    # Open a shell in agent-runtime
make up-gpu   # Start with the NVIDIA override
```

## Data Layout

```text
aiOS-ui/       Versioned application code, Compose files, images, and installers
working-space/ Read/write workspace for agent work
outputs/       Generated AI results
sandbox-data/
  my-data/     Read-only data mount for agents
  state/       Agent state, job history, tool lockfile, and file policy
  private-notes/ Notes mounted only into the control service
  exports/     Generated migration bundles
  imports/     Bundles staged for restore
```

All mutable data is gitignored. The dashboard runs only on `127.0.0.1:9119`; Hermes and AgentMemory are reachable through its internal proxy instead of direct host ports. CodeGraph keeps its shared index in `working-space/.codegraph`, so every agent that works in `/workspace` can query the same current code knowledge. CodeGraph's MCP adapter is installed for supported hosts such as Codex and Hermes; MiMo and Reasonix can use the same `codegraph` CLI directly in the runtime.

## Agent and Tool Management

The **Agents & Tools** screen manages Hermes, Codex, MiMo, Reasonix, AgentMemory, and CodeGraph. Updates are confirmed, queued one at a time, and logged in `sandbox-data/state/jobs.json`.

Additional tools can be installed only as exact NPM or PyPI/uv package versions. Their definitions are saved to `sandbox-data/state/extensions.lock.json`. On a restored or fresh installation the runtime replays those pinned tools automatically; the maintained Dockerfiles are not rewritten by terminal activity.

## Export and Restore

Use the dashboard migration API or the host CLI:

```bash
python3 aiOS-ui/scripts/aiosctl.py export
python3 aiOS-ui/scripts/aiosctl.py restore /path/to/aios-YYYYMMDD-HHMMSS.tar.gz
python3 aiOS-ui/scripts/aiosctl.py doctor
```

Bundles include selected state and notes with checksums. Credentials under `sandbox-data/state/credentials` and `sandbox-data/state/secrets` are excluded by default.
