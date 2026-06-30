#!/bin/bash
# recover.sh — one-shot recovery for all services
# Run this when services are dead after laptop sleep/wake or container restart.
# Usage: bash /config-file/system-config/recover.sh
set +e

# Resolve python interpreter with fastapi/uvicorn
PYTHON_EXE="python"
for py in "/home/ai_user/.hermes/hermes-agent/venv/bin/python" "/aiOS-ui/hermes-webui/.venv/bin/python" "/home/ai_user/miniconda3/envs/ai-baseline/bin/python" "python"; do
  if [ -x "$py" ]; then
    PYTHON_EXE="$py"
    break
  fi
done

echo "=== $(date -Iseconds): Recovery started ==="

# Helper: write PID to file, silently ignoring permission errors (root-owned files)
write_pid() { { printf '%s\n' "$1" >"$2"; } 2>/dev/null || true; }

# ── iii engine ──
if ! iii --version >/dev/null 2>&1; then
  echo "[recover] iii missing, restoring..."
  cp ~/.agentmemory/bin/iii ~/.local/bin/iii 2>/dev/null && chmod +x ~/.local/bin/iii
fi

# ── agentmemory ──
if ! curl -s -o /dev/null -w '' http://localhost:3113/ 2>/dev/null; then
  echo "[recover] agentmemory down, starting..."
  if [ "$(id -u)" -eq 0 ]; then
    cp /config-file/aiOS-ui/agentmemory/iii-config.yaml \
      /usr/local/lib/node_modules/@agentmemory/agentmemory/dist/iii-config.yaml 2>/dev/null
  fi
  # Comment out AGENTMEMORY_VIEWER_HOST=0.0.0.0 in .env if present (causes port 3113 EADDRINUSE conflict with viewer-proxy)
  if [ -f ~/.agentmemory/.env ]; then
    sed -i 's/^AGENTMEMORY_VIEWER_HOST=0.0.0.0/# AGENTMEMORY_VIEWER_HOST=0.0.0.0/g' ~/.agentmemory/.env
    sed -i 's/^VIEWER_ALLOWED_HOSTS=/# VIEWER_ALLOWED_HOSTS=/g' ~/.agentmemory/.env
  fi
  agentmemory start >>~/.agentmemory/agentmemory.log 2>&1 &
  for i in {1..20}; do
    if curl -s -o /dev/null -w '' http://localhost:3113/ 2>/dev/null; then
      break
    fi
    sleep 0.2
  done
fi

# ── viewer-proxy ──
# Kill any stale viewer-proxy process holding port 3113.
for f in /proc/[0-9]*/cmdline; do
  pid=${f%/cmdline}
  pid=${pid#/proc/}
  grep -q "viewer-proxy" "$f" 2>/dev/null && kill -9 "$pid" 2>/dev/null || true
done
# Wait until port 3113 is released (up to 3 seconds).
for i in 1 2 3; do
  if ! awk 'NR>1{split($2,a,":");p=strtonum("0x"a[2]);if(p==3113)print}' /proc/net/tcp 2>/dev/null | grep -q .; then
    break
  fi
  sleep 1
done

if [ ! -f ~/.agentmemory/viewer-proxy.pid ] || ! kill -0 "$(cat ~/.agentmemory/viewer-proxy.pid 2>/dev/null)" 2>/dev/null; then
  echo "[recover] viewer-proxy down, starting..."
  cp /config-file/aiOS-ui/agentmemory/viewer-proxy.mjs ~/.agentmemory/viewer-proxy.mjs
  nohup node ~/.agentmemory/viewer-proxy.mjs >>~/.agentmemory/viewer-proxy.log 2>&1 &
  write_pid "$!" ~/.agentmemory/viewer-proxy.pid
fi

# ── hermes dashboard ──
# Kill any stale/hung dashboard processes first to guarantee a clean recovery.
for f in /proc/[0-9]*/cmdline; do
  p=${f%/cmdline}
  p=${p#/proc/}
  args=$(cat "$f" 2>/dev/null | tr '\0' '\n')
  echo "$args" | grep -q "^dashboard$" && echo "$args" | grep -q "hermes" && kill -9 "$p" 2>/dev/null || true
done

echo "[recover] dashboard restarting..."
mkdir -p ~/.hermes/logs
HERMES_WEBUI_TRUST_FORWARDED_HOST=1 hermes dashboard --no-open >>/config-file/dashboard.log 2>&1 &
write_pid "$!" /tmp/hermes-dashboard.pid
for i in {1..20}; do
  if curl -s -o /dev/null -w '' http://localhost:9119/ 2>/dev/null; then
    break
  fi
  sleep 0.2
done

# Resolve actual DASH_PID
DASH_PID=""
for f in /proc/[0-9]*/cmdline; do
  p=${f%/cmdline}
  p=${p#/proc/}
  args=$(cat "$f" 2>/dev/null | tr '\0' '\n')
  echo "$args" | grep -q "^dashboard$" && echo "$args" | grep -q "hermes" && {
    DASH_PID=$p
    write_pid "$p" /tmp/hermes-dashboard.pid
    break
  }
done

# ── hermes dashboard-proxy ──
# Kill any stale/hung dashboard-proxy processes first to guarantee a clean recovery.
for f in /proc/[0-9]*/cmdline; do
  p=${f%/cmdline}
  p=${p#/proc/}
  cat "$f" 2>/dev/null | grep -q "dashboard-proxy" && kill -9 "$p" 2>/dev/null || true
done
# Wait until port 9119 is released (up to 3 seconds).
for i in 1 2 3; do
  if ! awk 'NR>1{split($2,a,":");p=strtonum("0x"a[2]);if(p==9119)print}' /proc/net/tcp 2>/dev/null | grep -q .; then
    break
  fi
  sleep 1
done

echo "[recover] dashboard-proxy restarting..."
nohup node /config-file/hermes/dashboard-proxy.mjs >>/config-file/hermes-proxy.log 2>&1 &
PROXY_PID=$!
write_pid "$PROXY_PID" /tmp/hermes-proxy.pid
sleep 1

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
  hermes gateway run >>/config-file/gateway.log 2>&1 &
  for i in {1..15}; do
    if hermes gateway status 2>&1 | grep -q "running"; then
      break
    fi
    sleep 0.2
  done
fi

# ── hermes-webui (server.py on port 8501) ──
WEBUI_PID=""
for f in /proc/[0-9]*/cmdline; do
  p=${f%/cmdline}
  p=${p#/proc/}
  cat "$f" 2>/dev/null | grep -q "server.py" && {
    WEBUI_PID=$p
    break
  }
done
if [ -z "$WEBUI_PID" ]; then
  echo "[recover] hermes-webui down, starting..."
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}
    pid=${pid#/proc/}
    cat "$f" 2>/dev/null | grep -q "server.py" && kill -9 "$pid" 2>/dev/null || true
  done
  if [ "$(id -u)" -eq 0 ]; then
    runuser -u ai_user -- env HOME=/home/ai_user HERMES_WEBUI_HOST=0.0.0.0 HERMES_WEBUI_PORT=8501 HERMES_WEBUI_TRUST_FORWARDED_HOST=1 "$PYTHON_EXE" /aiOS-ui/hermes-webui/server.py >>/config-file/aiOS-ui.log 2>&1 &
  else
    env HOME=/home/ai_user HERMES_WEBUI_HOST=0.0.0.0 HERMES_WEBUI_PORT=8501 HERMES_WEBUI_TRUST_FORWARDED_HOST=1 "$PYTHON_EXE" /aiOS-ui/hermes-webui/server.py >>/config-file/aiOS-ui.log 2>&1 &
  fi
  WEBUI_PID=$!
  write_pid "$WEBUI_PID" /tmp/hermes-subserver.pid
  for i in {1..10}; do
    if curl -s -o /dev/null -w '' http://localhost:8501/ 2>/dev/null; then
      break
    fi
    sleep 0.2
  done
fi

# ── headroom proxy ──
HEADROOM_PID=""
for f in /proc/[0-9]*/cmdline; do
  p=${f%/cmdline}
  p=${p#/proc/}
  cat "$f" 2>/dev/null | tr '\0' ' ' | grep -q "headroom proxy" && {
    HEADROOM_PID=$p
    break
  }
done
if [ -n "$HEADROOM_PID" ]; then
  write_pid "$HEADROOM_PID" /tmp/headroom.pid
else
  echo "[recover] headroom proxy down, starting..."
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}
    pid=${pid#/proc/}
    cat "$f" 2>/dev/null | tr '\0' ' ' | grep -q "headroom proxy" && kill -9 "$pid" 2>/dev/null || true
  done
  if [ "$(id -u)" -eq 0 ]; then
    runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'nohup /home/ai_user/miniconda3/bin/headroom proxy >> /config-file/headroom.log 2>&1' &
  else
    nohup /home/ai_user/miniconda3/bin/headroom proxy >>/config-file/headroom.log 2>&1 &
  fi
  HEADROOM_PID=$!
  write_pid "$HEADROOM_PID" /tmp/headroom.pid
  for i in {1..5}; do
    if curl -s -o /dev/null -w '' http://localhost:8787/health 2>/dev/null; then
      break
    fi
    sleep 0.2
  done
fi

# ── watchdog ──
if [ "$(id -u)" -eq 0 ]; then
  echo "[recover] ensuring watchdog is running..."
  for f in /proc/[0-9]*/cmdline; do
    pid=${f%/cmdline}
    pid=${pid#/proc/}
    cat "$f" 2>/dev/null | grep -q "while true.*hermes-dashboard" && kill "$pid" 2>/dev/null || true
  done
  (
    set +e
    while true; do
      sleep 60
      # Dashboard
      if [ -f /tmp/hermes-dashboard.pid ] && ! kill -0 "$(cat /tmp/hermes-dashboard.pid 2>/dev/null)" 2>/dev/null; then
        mkdir -p "$HOME/.hermes/logs"
        HERMES_WEBUI_TRUST_FORWARDED_HOST=1 hermes dashboard --no-open >>/config-file/dashboard.log 2>&1 &
        echo $! >/tmp/hermes-dashboard.pid
        chown ai_user:ai_user /tmp/hermes-dashboard.pid
        echo "[watchdog] $(date -Iseconds): dashboard restarted" >>/config-file/hermes-watchdog.log
      fi
      # Dashboard-proxy
      if [ -f /tmp/hermes-proxy.pid ] && ! kill -0 "$(cat /tmp/hermes-proxy.pid 2>/dev/null)" 2>/dev/null; then
        nohup node /config-file/hermes/dashboard-proxy.mjs >>/config-file/hermes-proxy.log 2>&1 &
        echo $! >/tmp/hermes-proxy.pid
        chown ai_user:ai_user /tmp/hermes-proxy.pid
        echo "[watchdog] $(date -Iseconds): dashboard-proxy restarted" >>/config-file/hermes-watchdog.log
      fi
      # viewer-proxy
      if [ -f "$HOME/.agentmemory/viewer-proxy.pid" ] && ! kill -0 "$(cat "$HOME/.agentmemory/viewer-proxy.pid" 2>/dev/null)" 2>/dev/null; then
        cp /config-file/aiOS-ui/agentmemory/viewer-proxy.mjs "$HOME/.agentmemory/viewer-proxy.mjs" 2>/dev/null || true
        nohup node "$HOME/.agentmemory/viewer-proxy.mjs" >>"$HOME/.agentmemory/viewer-proxy.log" 2>&1 &
        write_pid "$!" "$HOME/.agentmemory/viewer-proxy.pid"
        echo "[watchdog] $(date -Iseconds): viewer-proxy restarted" >>/config-file/hermes-watchdog.log
      fi
      # hermes-webui
      if [ -f /tmp/hermes-subserver.pid ] && ! kill -0 "$(cat /tmp/hermes-subserver.pid 2>/dev/null)" 2>/dev/null; then
        if [ "$(id -u)" -eq 0 ]; then
          runuser -u ai_user -- env HOME=/home/ai_user HERMES_WEBUI_HOST=0.0.0.0 HERMES_WEBUI_PORT=8501 HERMES_WEBUI_TRUST_FORWARDED_HOST=1 "$PYTHON_EXE" /aiOS-ui/hermes-webui/server.py >>/config-file/aiOS-ui.log 2>&1 &
        else
          env HOME=/home/ai_user HERMES_WEBUI_HOST=0.0.0.0 HERMES_WEBUI_PORT=8501 HERMES_WEBUI_TRUST_FORWARDED_HOST=1 "$PYTHON_EXE" /aiOS-ui/hermes-webui/server.py >>/config-file/aiOS-ui.log 2>&1 &
        fi
        echo $! >/tmp/hermes-subserver.pid
        chown ai_user:ai_user /tmp/hermes-subserver.pid
        echo "[watchdog] $(date -Iseconds): hermes-webui restarted" >>/config-file/hermes-watchdog.log
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
          hermes gateway restart >>/config-file/gateway.log 2>&1 || true
          echo "[watchdog] $(date -Iseconds): gateway restarted (state: $TG_STATE)" >>/config-file/hermes-watchdog.log
        fi
      fi
      # Headroom proxy
      if [ -f /tmp/headroom.pid ] && ! kill -0 "$(cat /tmp/headroom.pid 2>/dev/null)" 2>/dev/null; then
        if [ "$(id -u)" -eq 0 ]; then
          runuser -u ai_user -- env HOME=/home/ai_user zsh -c 'nohup /home/ai_user/miniconda3/bin/headroom proxy >> /config-file/headroom.log 2>&1' &
        else
          nohup /home/ai_user/miniconda3/bin/headroom proxy >>/config-file/headroom.log 2>&1 &
        fi
        echo $! >/tmp/headroom.pid
        chown ai_user:ai_user /tmp/headroom.pid
        echo "[watchdog] $(date -Iseconds): headroom proxy restarted" >>/config-file/hermes-watchdog.log
      fi
    done
  ) >>/config-file/hermes-watchdog.log 2>&1 &
  echo "[recover] watchdog PID=$!"
else
  echo "[recover] watchdog is managed by root. Skipping."
fi

# ── status report ──
echo ""
echo "=== Recovery complete. Status: ==="
echo -n "iii: " && iii --version 2>&1 | head -1
echo -n "agentmemory: " && curl -s -o /dev/null -w '%{http_code}' http://localhost:3113/ && echo " (port 3113)"
echo -n "dashboard: "
_dp=""
for f in /proc/[0-9]*/cmdline; do
  p=${f%/cmdline}
  p=${p#/proc/}
  _a=$(cat "$f" 2>/dev/null | tr '\0' '\n')
  echo "$_a" | grep -q "^dashboard$" && echo "$_a" | grep -q "hermes" && {
    _dp=$p
    break
  }
done
[ -n "$_dp" ] && echo "PID $_dp OK" || echo "FAIL"
echo -n "proxy: "
_pp=""
for f in /proc/[0-9]*/cmdline; do
  p=${f%/cmdline}
  p=${p#/proc/}
  cat "$f" 2>/dev/null | grep -q "dashboard-proxy" && {
    _pp=$p
    break
  }
done
[ -n "$_pp" ] && echo "PID $_pp OK" || echo "FAIL"
echo -n "gateway: " && hermes gateway status 2>&1 | head -1
echo -n "hermes-webui: "
_wp=""
for f in /proc/[0-9]*/cmdline; do
  p=${f%/cmdline}
  p=${p#/proc/}
  cat "$f" 2>/dev/null | grep -q "server.py" && {
    _wp=$p
    break
  }
done
[ -n "$_wp" ] && echo "PID $_wp OK (port 8501)" || echo "FAIL"
echo -n "headroom: "
_hp=""
for f in /proc/[0-9]*/cmdline; do
  p=${f%/cmdline}
  p=${p#/proc/}
  cat "$f" 2>/dev/null | tr '\0' ' ' | grep -q "headroom proxy" && {
    _hp=$p
    break
  }
done
[ -n "$_hp" ] && echo "PID $_hp OK (port 8787)" || echo "FAIL"
echo -n "watchdog: " && ls -la /config-file/hermes-watchdog.log 2>/dev/null | awk '{print "log size:", $5, "bytes"}'
CONTAINER_IP=$(hostname -I 2>/dev/null | awk '{print $1}')
[ -z "$CONTAINER_IP" ] && CONTAINER_IP="127.0.0.1"
echo -n "ports: "
curl -s -o /dev/null -w "9119_local:%{http_code} " http://127.0.0.1:9119/ || echo -n "9119_local:down "
curl -s -o /dev/null -w "9119_proxy:%{http_code} " http://"$CONTAINER_IP":9119/ || echo -n "9119_proxy:down "
curl -s -o /dev/null -w "3113_local:%{http_code} " http://127.0.0.1:3113/ || echo -n "3113_local:down "
curl -s -o /dev/null -w "3113_proxy:%{http_code} " http://"$CONTAINER_IP":3113/ || echo -n "3113_proxy:down "
curl -s -o /dev/null -w "8787:%{http_code}" http://127.0.0.1:8787/health || echo -n "8787:down"
echo
