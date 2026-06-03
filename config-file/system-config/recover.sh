#!/bin/bash
# recover.sh — one-shot recovery for all services
# Run this when services are dead after laptop sleep/wake or container restart.
# Usage: bash /config-file/system-config/recover.sh
set +e

echo "=== $(date -Iseconds): Recovery started ==="

# ── iii engine ──
if ! iii --version >/dev/null 2>&1; then
  echo "[recover] iii missing, restoring..."
  cp ~/.agentmemory/bin/iii ~/.local/bin/iii 2>/dev/null && chmod +x ~/.local/bin/iii
fi

# ── agentmemory ──
if ! curl -s -o /dev/null -w '' http://localhost:3113/ 2>/dev/null; then
  echo "[recover] agentmemory down, starting..."
  sudo cp /config-file/agentmemory/iii-config.yaml \
    /usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml 2>/dev/null
  agentmemory start >> ~/.agentmemory/agentmemory.log 2>&1 || true
  sleep 4
fi

# ── viewer-proxy ──
if [ ! -f ~/.agentmemory/viewer-proxy.pid ] || ! kill -0 "$(cat ~/.agentmemory/viewer-proxy.pid 2>/dev/null)" 2>/dev/null; then
  echo "[recover] viewer-proxy down, starting..."
  kill $(cat ~/.agentmemory/viewer-proxy.pid 2>/dev/null) 2>/dev/null
  cp /config-file/agentmemory/viewer-proxy.mjs ~/.agentmemory/viewer-proxy.mjs
  nohup node ~/.agentmemory/viewer-proxy.mjs >> ~/.agentmemory/viewer-proxy.log 2>&1 &
  echo $! > ~/.agentmemory/viewer-proxy.pid
fi

# ── hermes dashboard ──
if [ ! -f /tmp/hermes-dashboard.pid ] || ! kill -0 "$(cat /tmp/hermes-dashboard.pid 2>/dev/null)" 2>/dev/null; then
  echo "[recover] dashboard down, starting..."
  mkdir -p ~/.hermes/logs
  hermes dashboard --no-open >> ~/.hermes/logs/dashboard.log 2>&1 &
  echo $! > /tmp/hermes-dashboard.pid
  sleep 3
fi

# ── hermes dashboard-proxy ──
if [ ! -f /tmp/hermes-proxy.pid ] || ! kill -0 "$(cat /tmp/hermes-proxy.pid 2>/dev/null)" 2>/dev/null; then
  echo "[recover] dashboard-proxy down, starting..."
  # Kill stale processes
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}; pid=${pid#/proc/}
    grep -q "dashboard-proxy" "$f" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
  done
  nohup node /config-file/hermes/dashboard-proxy.mjs >> /tmp/hermes-proxy.log 2>&1 &
  echo $! > /tmp/hermes-proxy.pid
  sleep 1
fi

# ── fcc-server ──
if [ ! -f /tmp/fcc-server.pid ] || ! kill -0 "$(cat /tmp/fcc-server.pid 2>/dev/null)" 2>/dev/null; then
  echo "[recover] fcc-server down, starting..."
  mkdir -p ~/.fcc/logs
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}; pid=${pid#/proc/}
    grep -q "fcc-server" "$f" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
  done
  nohup fcc-server >> ~/.fcc/logs/fcc-server.log 2>&1 &
  echo $! > /tmp/fcc-server.pid
  sleep 2
fi

# ── hermes gateway ──
GATEWAY_STATE_FILE="$HOME/.hermes/gateway_state.json"
GATEWAY_RUNNING=false
if [ -f "$GATEWAY_STATE_FILE" ]; then
  GATEWAY_PID=$(python3 -c "import json; print(json.load(open('$GATEWAY_STATE_FILE')).get('pid',''))" 2>/dev/null)
  if [ -n "$GATEWAY_PID" ] && kill -0 "$GATEWAY_PID" 2>/dev/null; then
    GATEWAY_RUNNING=true
  fi
fi
if [ "$GATEWAY_RUNNING" = false ]; then
  echo "[recover] gateway down, starting..."
  hermes gateway run >> ~/.hermes/logs/gateway.log 2>&1 &
  sleep 3
fi

# ── aiOS-ui (FastAPI on port 8501) ──
if [ ! -f /tmp/aiOS-ui.pid ] || ! kill -0 "$(cat /tmp/aiOS-ui.pid 2>/dev/null)" 2>/dev/null; then
  echo "[recover] aiOS-ui down, starting..."
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}; pid=${pid#/proc/}
    grep -q "aiOS-ui\|main.py" "$f" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
  done
  (cd /aiOS-ui && exec python main.py) >>/tmp/aiOS-ui.log 2>&1 &
  echo $! > /tmp/aiOS-ui.pid
  sleep 2
fi

# ── watchdog (always restart it) ──
echo "[recover] ensuring watchdog is running..."
# Kill any existing watchdog
for f in /proc/[0-9]*/cmdline; do
  pid=${f%/cmdline}; pid=${pid#/proc/}
  grep -q "while true.*hermes-dashboard" "$f" 2>/dev/null && kill "$pid" 2>/dev/null || true
done
# Start fresh
(
  set +e
  while true; do
    sleep 60
    # Dashboard
    if [ -f /tmp/hermes-dashboard.pid ] && ! kill -0 "$(cat /tmp/hermes-dashboard.pid 2>/dev/null)" 2>/dev/null; then
      mkdir -p "$HOME/.hermes/logs"
      hermes dashboard --no-open >>"$HOME/.hermes/logs/dashboard.log" 2>&1 &
      echo $! >/tmp/hermes-dashboard.pid
      echo "[watchdog] $(date -Iseconds): dashboard restarted" >>/tmp/hermes-watchdog.log
    fi
    # Dashboard-proxy
    if [ -f /tmp/hermes-proxy.pid ] && ! kill -0 "$(cat /tmp/hermes-proxy.pid 2>/dev/null)" 2>/dev/null; then
      nohup node /config-file/hermes/dashboard-proxy.mjs >>/tmp/hermes-proxy.log 2>&1 &
      echo $! >/tmp/hermes-proxy.pid
      echo "[watchdog] $(date -Iseconds): dashboard-proxy restarted" >>/tmp/hermes-watchdog.log
    fi
    # viewer-proxy
    if [ -f "$HOME/.agentmemory/viewer-proxy.pid" ] && ! kill -0 "$(cat "$HOME/.agentmemory/viewer-proxy.pid" 2>/dev/null)" 2>/dev/null; then
      cp /config-file/agentmemory/viewer-proxy.mjs "$HOME/.agentmemory/viewer-proxy.mjs" 2>/dev/null || true
      nohup node "$HOME/.agentmemory/viewer-proxy.mjs" >>"$HOME/.agentmemory/viewer-proxy.log" 2>&1 &
      echo $! >"$HOME/.agentmemory/viewer-proxy.pid"
      echo "[watchdog] $(date -Iseconds): viewer-proxy restarted" >>/tmp/hermes-watchdog.log
    fi
    # fcc-server
    if [ -f /tmp/fcc-server.pid ] && ! kill -0 "$(cat /tmp/fcc-server.pid 2>/dev/null)" 2>/dev/null; then
      nohup fcc-server >>"$HOME/.fcc/logs/fcc-server.log" 2>&1 &
      echo $! >/tmp/fcc-server.pid
      echo "[watchdog] $(date -Iseconds): fcc-server restarted" >>/tmp/hermes-watchdog.log
    fi
    # aiOS-ui
    if [ -f /tmp/aiOS-ui.pid ] && ! kill -0 "$(cat /tmp/aiOS-ui.pid 2>/dev/null)" 2>/dev/null; then
      (cd /aiOS-ui && exec python main.py) >>/tmp/aiOS-ui.log 2>&1 &
      echo $! > /tmp/aiOS-ui.pid
      echo "[watchdog] $(date -Iseconds): aiOS-ui restarted" >>/tmp/hermes-watchdog.log
    fi
    # Gateway
    if [ -f "$HOME/.hermes/gateway_state.json" ]; then
      TG_STATE=$(python3 -c "
import json
try:
    d = json.load(open('$HOME/.hermes/gateway_state.json'))
    gw = d.get('gateway_state', '')
    tg = d.get('platforms', {}).get('telegram', {}).get('state', 'unknown')
    print(gw, tg)
except Exception:
    print('error')
" 2>/dev/null)
      if ! echo "$TG_STATE" | grep -q "running connected"; then
        hermes gateway restart >>"$HOME/.hermes/logs/gateway.log" 2>&1 || true
        echo "[watchdog] $(date -Iseconds): gateway restarted (state: $TG_STATE)" >>/tmp/hermes-watchdog.log
      fi
    fi
  done
) >>/tmp/hermes-watchdog.log 2>&1 &
echo "[recover] watchdog PID=$!"

# ── status report ──
echo ""
echo "=== Recovery complete. Status: ==="
echo -n "iii: " && iii --version 2>&1 | head -1
echo -n "agentmemory: " && curl -s -o /dev/null -w '%{http_code}' http://localhost:3113/ && echo " (port 3113)"
echo -n "dashboard: " && kill -0 $(cat /tmp/hermes-dashboard.pid 2>/dev/null) 2>/dev/null && echo "PID $(cat /tmp/hermes-dashboard.pid) OK" || echo "FAIL"
echo -n "proxy: " && kill -0 $(cat /tmp/hermes-proxy.pid 2>/dev/null) 2>/dev/null && echo "PID $(cat /tmp/hermes-proxy.pid) OK" || echo "FAIL"
echo -n "fcc-server: " && kill -0 $(cat /tmp/fcc-server.pid 2>/dev/null) 2>/dev/null && echo "PID $(cat /tmp/fcc-server.pid) OK" || echo "FAIL"
echo -n "gateway: " && hermes gateway status 2>&1 | head -1
echo -n "aiOS-ui: " && kill -0 $(cat /tmp/aiOS-ui.pid 2>/dev/null) 2>/dev/null && echo "PID $(cat /tmp/aiOS-ui.pid) OK (port 8501)" || echo "FAIL"
echo -n "watchdog: " && ls -la /tmp/hermes-watchdog.log 2>/dev/null | awk '{print "log size:", $5, "bytes"}'
echo -n "ports: " && curl -s -o /dev/null -w '9119:%{http_code} ' http://localhost:9119/ && curl -s -o /dev/null -w '3113:%{http_code} ' http://localhost:3113/ && curl -s -o /dev/null -w '8082:%{http_code}' http://localhost:8082/health && echo
