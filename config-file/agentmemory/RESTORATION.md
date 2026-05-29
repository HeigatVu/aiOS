# agentmemory Restoration Guide

Read this file at the start of any session after a Docker container rebuild.
Follow the steps in order; each step has a verification check.

---

## Background — why this is needed

On every container start, agentmemory launches a bare boot daemon (low PID, ~90)
with **no environment variables**. This daemon:
- Binds ports 3111 (REST), 3112 (streams), 3113 (viewer) on 127.0.0.1
- Reads nothing from `~/.agentmemory/.env` — all feature flags are absent
- Spawns `~/.agentmemory/viewer-proxy.mjs` to expose the viewer on the LAN IP

The viewer enforces a Host-header allowlist using `process.env.VIEWER_ALLOWED_HOSTS`,
which is evaluated at module load time — **not** from the `.env` file. So even after
writing the correct env, the boot daemon's viewer rejects browser requests with
`403 forbidden host`.

The fix lives in `viewer-proxy.mjs`: it rewrites `Host: <LAN-IP>:3113` →
`Host: localhost:3113` on the first HTTP chunk before forwarding, bypassing
the allowlist check entirely.

---

## Files managed here

| File | Destination | Purpose |
|------|-------------|---------|
| `.env` | `~/.agentmemory/.env` | Feature flags, LLM key, all runtime config |
| `iii-config.yaml` | `/usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml` | Service config — binds REST/stream to 127.0.0.1, sets CORS origins |
| `viewer-proxy.mjs` | `~/.agentmemory/viewer-proxy.mjs` | HTTP-aware proxy: exposes viewer on LAN IP with Host-header rewrite |

---

## Restoration steps

### Step 1 — Copy config files

```bash
cp /config-file/agentmemory/.env ~/.agentmemory/.env

cp /config-file/agentmemory/iii-config.yaml \
  /usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml
```

Do NOT copy viewer-proxy.mjs yet — agentmemory may overwrite it on start.

---

### Step 2 — Kill the boot daemon and restart cleanly

The boot daemon holds port 3113 on localhost. Find and kill it, then restart:

```bash
# Kill everything agentmemory-related by their PID files
kill $(cat ~/.agentmemory/worker.pid ~/.agentmemory/iii.pid ~/.agentmemory/viewer-proxy.pid 2>/dev/null) 2>/dev/null

# Wait for ports to clear, then start fresh
sleep 2
agentmemory start
```

Verify the start output says `Viewer: http://localhost:3113` (not 3114).
If it says 3114, something still holds 3113 — see Troubleshooting below.

```bash
agentmemory status
```

Expected output includes:
- `Health: ✓ healthy`
- `Provider: ✓ llm`
- `Embeddings: ✓ embeddings`
- All five flags ticked: GRAPH_EXTRACTION, CONSOLIDATION, AUTO_COMPRESS, INJECT_CONTEXT, REFLECT

---

### Step 3 — Install the patched viewer-proxy

agentmemory may have spawned a fresh (unpatched) viewer-proxy.mjs. Replace it:

```bash
# Check if the running proxy has the host-rewrite patch
tail -1 ~/.agentmemory/viewer-proxy.log
```

If the last line does NOT contain `host-rewrite enabled`:

```bash
# Kill the unpatched proxy, install the patch, restart
kill $(cat ~/.agentmemory/viewer-proxy.pid 2>/dev/null) 2>/dev/null
cp /config-file/agentmemory/viewer-proxy.mjs ~/.agentmemory/viewer-proxy.mjs
sleep 1
node ~/.agentmemory/viewer-proxy.mjs >> ~/.agentmemory/viewer-proxy.log 2>&1 &
echo $! > ~/.agentmemory/viewer-proxy.pid
sleep 1
tail -1 ~/.agentmemory/viewer-proxy.log   # should now say "host-rewrite enabled"
```

If the last line already says `host-rewrite enabled`, skip this step.

---

### Step 4 — Verify viewer is reachable from the host

```bash
# Get the container's LAN IP
node -e "
const os = require('os');
for (const [n,a] of Object.entries(os.networkInterfaces()))
  if (n !== 'lo') for (const i of a)
    if (i.family==='IPv4' && !i.internal) console.log(i.address);
"
```

Then run a raw HTTP test against that IP:

```bash
node -e "
const net = require('net');
const LAN = '172.17.0.3'; // replace if your container IP differs
const c = net.connect(3113, LAN, () =>
  c.write('GET / HTTP/1.0\r\nHost: ' + LAN + ':3113\r\n\r\n'));
c.once('data', d => { console.log(d.toString().slice(0,80)); c.destroy(); });
c.on('error', e => console.error('FAIL:', e.message));
setTimeout(() => { console.error('TIMEOUT'); process.exit(1); }, 3000);
"
```

Expected: first line is `HTTP/1.1 200 OK`.
Open `http://<container-ip>:3113` in the host browser.

---

## Troubleshooting

### Viewer falls back to port 3114

Something still holds localhost:3113. Find it:

```bash
# Get the inode for port 3113
awk 'NR>1 { split($2,a,":"); p=strtonum("0x"a[2]); if(p==3113) print $10 }' /proc/net/tcp
# Replace INODE below with the number from the above command
for pid in /proc/[0-9]*/fd; do
  ls -la "$pid" 2>/dev/null | grep -q "socket:\[INODE\]" &&
    echo "PID: ${pid%/fd}" &&
    cat "${pid%/fd}/cmdline" 2>/dev/null | tr '\0' ' '
done
```

Kill that PID, wait 1 s, then `agentmemory start` again.

### Viewer returns `403 forbidden host`

The viewer-proxy is running the unpatched (raw TCP) version. Redo Step 3.

### Flags not showing in `agentmemory status`

`.env` was not copied before start, or the daemon started before the copy.
Verify:

```bash
grep 'AGENTMEMORY_AUTO_COMPRESS\|CONSOLIDATION_ENABLED' ~/.agentmemory/.env
```

If missing, re-copy and restart:

```bash
agentmemory stop && sleep 2 && agentmemory start
```

### LAN IP changed after rebuild

The LAN IP is auto-detected by viewer-proxy.mjs at startup — no action needed.
The `.env` line `VIEWER_ALLOWED_HOSTS=172.17.0.3:3113` is a non-functional
remnant (the bug means it is never read by the boot daemon); ignore it.

---

## Known bug in agentmemory v0.9.22

`VIEWER_ALLOWED_HOSTS` in `.env` is silently ignored. The viewer reads
`process.env.VIEWER_ALLOWED_HOSTS` at module-load time; `loadEnvFile()` only
populates `getMergedEnv()`, not `process.env`. The viewer-proxy Host-rewrite
is the correct workaround until this is fixed upstream.
