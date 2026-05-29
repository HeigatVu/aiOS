# Hermes Dashboard Restoration Guide

Read this after a Docker container rebuild to restore external access to the
Hermes dashboard at `http://<container-ip>:9119`.

---

## Background — why this is needed

The Hermes dashboard binds to `127.0.0.1:9119` and enforces a Host-header
allowlist (only `localhost`, `127.0.0.1`, `::1`) to prevent DNS-rebinding
attacks (GHSA-ppp5-vxwm-4cf7). Requests from the host browser carry
`Host: 172.17.0.3:9119`, which the server rejects with 421.

Binding to `0.0.0.0` (`--host 0.0.0.0`) requires OAuth providers — not
available in this setup.

The fix: `dashboard-proxy.mjs` rewrites `Host: <LAN-IP>:9119` →
`Host: localhost:9119` on the first HTTP chunk before forwarding.
The LAN IP is auto-detected at startup via `os.networkInterfaces()`.

---

## Files managed here

| File | Purpose |
|------|---------|
| `dashboard-proxy.mjs` | HTTP-aware proxy — exposes dashboard on LAN IP with Host-header rewrite |

Hermes config (`~/.hermes/`) persists across rebuilds — no config files need
copying.

---

## Restoration steps

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
sleep 1
cat /tmp/hermes-proxy.log
# Expected: [dashboard-proxy] 172.17.0.3:9119 -> 127.0.0.1:9119 (host-rewrite enabled)
```

---

### Step 3 — Verify

```bash
node -e "
const net=require('net'), LAN='172.17.0.3';
const c=net.connect(9119,LAN,()=>c.write('GET / HTTP/1.0\r\nHost: '+LAN+':9119\r\n\r\n'));
c.once('data',d=>{console.log(d.toString().slice(0,80));c.destroy();});
c.on('error',e=>console.error('FAIL:',e.message));
setTimeout(()=>process.exit(0),2000);
"
```

Expected first line: `HTTP/1.1 200 OK`

Then open `http://172.17.0.3:9119` in the host browser.

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

### Proxy EADDRINUSE on LAN IP

A previous proxy instance is still running. Find and kill it:

```bash
for pid in /proc/[0-9]*/fd; do
  ls -la "$pid" 2>/dev/null | grep -q socket &&
    grep -q 'dashboard-proxy' /proc/${pid%/fd}/cmdline 2>/dev/null &&
    echo "PID: ${pid%/fd}" && kill ${pid%/fd}
done
node /config-file/hermes/dashboard-proxy.mjs >> /tmp/hermes-proxy.log 2>&1 &
```

### LAN IP changed after rebuild

No action needed — the proxy auto-detects the LAN IP on startup.

---

## Security note

The Host-header rewrite bypasses DNS-rebinding protection intentionally.
This is safe because port 9119 on the Docker bridge IP is only reachable
from the host machine, not the public internet.
