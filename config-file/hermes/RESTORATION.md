# Hermes Dashboard Restoration Guide

Read this after a Docker container rebuild to restore external access to the
Hermes dashboard.

---

## Background — why this is needed

The Hermes dashboard binds to `127.0.0.1:9119` and enforces a Host-header
allowlist (only `localhost`, `127.0.0.1`, `::1`) to prevent DNS-rebinding
attacks (GHSA-ppp5-vxwm-4cf7). Requests arriving via Docker port mapping
carry `Host: <container-ip>:9119`, which the server rejects with 421.

Binding Hermes to `0.0.0.0` (`--host 0.0.0.0`) requires OAuth providers —
not available in this setup.

The fix: `dashboard-proxy.mjs` is an HTTP reverse proxy using
`http.createServer` → `http.request`. It forwards all requests to the
backend dashboard on `127.0.0.1:9119`, rewriting the `Host` header to
`localhost:9119` so the dashboard's allowlist check passes. The original
implementation used raw TCP (`net.createServer`) with regex-based Host
rewriting on the first chunk, which was fragile and returned `400 Bad Request`
from the container LAN IP. The current HTTP-based approach returns `200`
from both localhost and the container IP.

**Note:** Binding the proxy to `0.0.0.0:9119` does NOT work — Linux rejects
it as EADDRINUSE because Hermes already holds `127.0.0.1:9119` (loopback is
part of `0.0.0.0`). The proxy must bind to the container's LAN IP only.

---

## Files managed here

| File | Purpose |
|------|---------|
| `dashboard-proxy.mjs` | HTTP reverse proxy (`http.createServer`): exposes dashboard on container LAN IP with proper Host-header forwarding |

Hermes config (`~/.hermes/`) persists across rebuilds — no config files need
copying.

---

## Auto-start (configured 2026-05-31)

Both the Hermes gateway and the dashboard proxy auto-start via the container
entrypoint — **no manual steps needed for a normal restart.**

The entrypoint handles startup on every container boot. `~/.zshrc` contains
a **fallback-only** guard that only starts the proxy if the entrypoint's
instance has already exited and no other instance is running:

```zsh
# Recommended ~/.zshrc pattern (fallback only — entrypoint starts services first):

# 1. Dashboard proxy (fallback — check PID file before starting to avoid race with entrypoint)
if ! kill -0 "$(cat /tmp/hermes-proxy.pid 2>/dev/null)" 2>/dev/null && \
   ! pgrep -f "dashboard-proxy.mjs" > /dev/null 2>&1; then
  node /config-file/hermes/dashboard-proxy.mjs >> ~/.hermes/logs/dashboard-proxy.log 2>&1 &
  disown
fi

# 2. Service health status (runs on every new shell)
echo ""
python3 /config-file/system-config/service_health.py
```

**Important**: The old pattern (`if ! pgrep -f "dashboard-proxy.mjs"`) without
the PID-file check can race with the entrypoint and launch a second proxy that
blocks the watchdog from restarting the first. Always use the PID-file check.

Proxy logs: `~/.hermes/logs/dashboard-proxy.log`

Only follow the manual steps below if auto-start failed or after a full rebuild.

---

## Restoration steps (manual fallback)

### Step 1 — Start the Hermes dashboard

```bash
hermes dashboard --no-open >> ~/.hermes/logs/dashboard.log 2>&1 &
```

Wait ~3 s, then verify port 9119 is bound:

```bash
awk 'NR>1{split($2,a,":");p=strtonum("0x"a[2]);if(p==9119)print "bound"}' /proc/net/tcp
```

---

### Step 2 — Start the proxy

```bash
node /config-file/hermes/dashboard-proxy.mjs >> /tmp/hermes-proxy.log 2>&1 &
echo $! > /tmp/hermes-proxy.pid
sleep 1
tail -1 /tmp/hermes-proxy.log
# Expected: [dashboard-proxy] <container-LAN-IP>:9119 -> 127.0.0.1:9119 (host-rewrite enabled)
```

---

### Step 3 — Verify from inside the container

```bash
# loopback
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:9119/rgical: touch only what was asked; match existing style; remove orphans you created, not pre-existing dead code
# Expected: 200

# container LAN IP (what the host/port mapping forwards to)
curl -s -o /dev/null -w '%{http_code}\n' http://$(hostname -I | awk '{print $1}'):9119/
# Expected: 200
```

### Step 4 — Open in host browser

**With docker-compose port mapping (no `127.0.0.1:` prefix):**

```
http://<laptop-IP>:9119
```

See `/config-file/docker-compose.reference.yml` for the host-side
configuration (`restart: always` + published ports without `127.0.0.1:`
prefix).

---

## Troubleshooting

### Port 9119 not bound after starting dashboard

```bash
tail -20 ~/.hermes/logs/dashboard.log
```

Previous process still running — stop it first:

```bash
hermes dashboard --stop && sleep 2
hermes dashboard --no-open >> ~/.hermes/logs/dashboard.log 2>&1 &
```

### Proxy returning 400 Bad Request from LAN IP

The proxy is using the old raw-TCP implementation. The source files in
`/config-file/hermes/` have been updated to use HTTP — re-copy and restart:

```bash
kill $(cat /tmp/hermes-proxy.pid 2>/dev/null) 2>/dev/null
nohup node /config-file/hermes/dashboard-proxy.mjs >> /tmp/hermes-proxy.log 2>&1 &
echo $! > /tmp/hermes-proxy.pid
sleep 1
curl -s -o /dev/null -w '%{http_code}\n' http://$(hostname -I | awk '{print $1}'):9119/
# Expected: 200
```

### Proxy EADDRINUSE on LAN IP

A previous proxy instance is still running. `pkill` may miss it — kill by
scanning `/proc` instead:

```bash
for f in /proc/[0-9]*/cmdline; do
  pid=${f%/cmdline}; pid=${pid#/proc/}
  grep -q "dashboard-proxy" "$f" 2>/dev/null && echo "killing $pid" && kill $pid
done
sleep 1
node /config-file/hermes/dashboard-proxy.mjs >> /tmp/hermes-proxy.log 2>&1 &
sleep 1
tail -2 /tmp/hermes-proxy.log
```

### Do NOT bind the proxy to 0.0.0.0

`0.0.0.0:9119` conflicts with Hermes on `127.0.0.1:9119` — Linux treats
loopback as part of `0.0.0.0`. The proxy must bind to the container's LAN IP.

### LAN IP changed after rebuild

No action needed — the proxy auto-detects the LAN IP on startup.

---

## Security note

The Host-header rewrite bypasses DNS-rebinding protection intentionally.
This is safe because port 9119 on the Docker bridge IP is only reachable
from the host machine, not the public internet.

---

## MCP Server Fixes (agentmemory + codegraph)

### Background

After a rebuild, `~/.hermes/config.yaml` may revert to a broken state for
two MCP servers:

1. **agentmemory** — `mcp-agentmemory` was missing from `platform_toolsets.cli`.
   Hermes started the server but immediately closed the pipe (EPIPE crash)
   because it had no toolset to load tools into. Also: args were formatted
   as a JSON string instead of a YAML list, and `AGENTMEMORY_URL` was absent.

2. **codegraph** — already in `platform_toolsets.cli` as `mcp-codegraph` and
   the binary exists at `~/.local/bin/codegraph`. No config fix needed — it
   only works in directories where `codegraph init -i` has been run.

### Fix — edit `~/.hermes/config.yaml`

#### 1. Add `mcp-agentmemory` to `platform_toolsets.cli`

Find the `platform_toolsets:` section and add `mcp-agentmemory` as the
first entry under `cli:`:

```yaml
platform_toolsets:
  cli:
  - mcp-agentmemory
  - mcp-codegraph
  - browser
  # ... rest unchanged
```

#### 2. Fix `mcp_servers.agentmemory`

Find the `mcp_servers:` section and replace the agentmemory entry:

```yaml
mcp_servers:
  agentmemory:
    command: npx
    args:
      - "-y"
      - "@agentmemory/mcp"
    env:
      AGENTMEMORY_URL: "http://localhost:3111"
  codegraph:
    command: codegraph
    args:
      - serve
      - --mcp
    timeout: 120
    connect_timeout: 60
    enabled: true
```

### Verify

After editing, restart hermes:

```bash
hermes restart
```

Then check that agentmemory MCP starts without EPIPE:

```bash
tail -20 ~/.hermes/logs/mcp-stderr.log
```

Expected: `[@agentmemory/mcp] Standalone MCP server vX.Y.Z starting...`
with no EPIPE crash after it.

### npm cache corruption (bonus fix)

If `npx @agentmemory/mcp` fails with `ENOTEMPTY`, the npx cache is corrupt.
Clear it:

```bash
rm -rf ~/.npm/_npx/ba4b5775a0ab44e2
```

Then retry — npx will re-download the package cleanly.
