# aiOS-UI Restoration Guide

Read this after a Docker rebuild to verify aiOS-ui is running correctly.

---

## What aiOS-ui is

FastAPI control panel running on **port 8501** inside the `ai_tui_sandbox` container.
Source: `/aiOS-ui/` (bind-mounted from host `./aiOS-ui`).
It starts hermes-webui as a subprocess on internal port 8787 and proxies `/api/*` to it.
Also exposes Claude / Gemini / Hermes CLI chat endpoints.

Access: `http://localhost:8501` (or `http://<laptop-IP>:8501` from LAN)

---

## Auto-start on laptop boot

The full startup chain is:

1. **Host boot** → systemd starts Docker daemon (`sudo systemctl enable docker` on host)
2. **Docker daemon** → starts `ai_tui_sandbox` container (`restart: always` in `docker-compose.yml`)
3. **Container** → runs `/usr/local/bin/entrypoint.sh`
4. **Entrypoint** → starts aiOS-ui background process, writes PID to `/tmp/aiOS-ui.pid`
5. **Watchdog** (60s loop) → restarts aiOS-ui if it dies

### One-time host setup (run on host, not inside container)

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Then bring up the container from the directory containing `docker-compose.yml`:

```bash
docker compose up -d
```

After that, every laptop boot automatically starts the container and all services.

---

## Verify after rebuild

```bash
# Inside the container:
kill -0 $(cat /tmp/aiOS-ui.pid 2>/dev/null) 2>/dev/null && echo "aiOS-ui OK" || echo "aiOS-ui FAIL"
curl -s http://localhost:8501/health | python3 -m json.tool
```

Expected health response:
```json
{
  "status": "ok",
  "hermes_subserver": {
    "healthy": true,
    "port": 8787,
    "host": "127.0.0.1",
    "pid": <number>
  }
}
```

---

## Manual start (if not running)

```bash
# Inside container:
(cd /aiOS-ui && exec python main.py) >>/tmp/aiOS-ui.log 2>&1 &
echo $! > /tmp/aiOS-ui.pid
echo "Started PID $(cat /tmp/aiOS-ui.pid)"
```

Or use the full recovery script:

```bash
bash /config-file/system-config/recover.sh
```

---

## Log file

```bash
tail -f /tmp/aiOS-ui.log
```

---

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `SIDECAR_HOST` | `0.0.0.0` | Bind address for FastAPI |
| `SIDECAR_PORT` | `8501` | Public port |
| `HERMES_SUB_HOST` | `127.0.0.1` | Internal hermes-webui bind |
| `HERMES_SUB_PORT` | `8787` | Internal hermes-webui port |
| `HERMES_HOME` | `~/.hermes` | Hermes data directory |

---

## Where it's wired in

| File | What was added |
|---|---|
| `/usr/local/bin/entrypoint.sh` | Startup section + watchdog coverage |
| `/config-file/system-config/recover.sh` | Startup + watchdog + status check |
| `/config-file/docker-compose.yml` (host) | Port 8501 exposed, `restart: always` |

---

## Rebuild flow

```bash
# On host:
docker compose build && docker compose up -d

# Inside container — verify:
bash /config-file/system-config/recover.sh
curl -s http://localhost:8501/health
```
