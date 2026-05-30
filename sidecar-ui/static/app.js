'use strict';

const { createApp, ref, reactive, computed, watch, onMounted, onUnmounted, nextTick, inject, provide } = Vue;
const { createRouter, createWebHashHistory } = VueRouter;

// ---------------------------------------------------------------------------
// API helpers
// ---------------------------------------------------------------------------

async function apiFetch(path, opts = {}) {
    const res = await fetch(path, {
        headers: { 'Content-Type': 'application/json' },
        ...opts,
    });
    if (!res.ok) {
        const text = await res.text().catch(() => res.statusText);
        throw new Error(text || `HTTP ${res.status}`);
    }
    return res.json();
}

const api = {
    get:    (path)       => apiFetch(path),
    post:   (path, body) => apiFetch(path, { method: 'POST',   body: JSON.stringify(body) }),
    delete: (path)       => apiFetch(path, { method: 'DELETE' }),
};

// ---------------------------------------------------------------------------
// WebSocket helpers
// ---------------------------------------------------------------------------

function streamWs(url, { onOpen, onChunk, onDone, onError } = {}) {
    const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${proto}//${location.host}${url}`);
    ws.onopen    = () => onOpen?.(ws);
    ws.onmessage = (e) => onChunk?.(e.data);
    ws.onerror   = () => onError?.('WebSocket error');
    ws.onclose   = () => onDone?.();
    return () => ws.close();
}

function streamExec(cmd, { onChunk, onDone, onError }) {
    return streamWs('/ws/exec', {
        onOpen: (ws) => ws.send(cmd),
        onChunk, onDone, onError,
    });
}

// ---------------------------------------------------------------------------
// Utility
// ---------------------------------------------------------------------------

// Global Toasts State
const toasts = ref([]);
function addToast(message, type = 'info') {
    const id = Date.now();
    toasts.value.push({ id, message, type });
    setTimeout(() => {
        toasts.value = toasts.value.filter(t => t.id !== id);
    }, 4000);
}

function octalToSymbolic(octal) {
    const map = ['---', '--x', '-w-', '-wx', 'r--', 'r-x', 'rw-', 'rwx'];
    const digits = String(octal).padStart(3, '0').slice(-3);
    let result = '';
    for (const ch of digits) {
        const n = parseInt(ch, 10);
        result += (n >= 0 && n <= 7) ? map[n] : '???';
    }
    return result;
}

function basename(path) {
    return path.split('/').filter(Boolean).pop() || path;
}

// Terminal history (localStorage)
const HISTORY_KEY = 'aios_terminal_history';
const MAX_HISTORY = 20;

function loadHistory() {
    try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]'); }
    catch { return []; }
}

function pushHistory(cmd, current) {
    const next = [cmd, ...current.filter(c => c !== cmd)].slice(0, MAX_HISTORY);
    localStorage.setItem(HISTORY_KEY, JSON.stringify(next));
    return next;
}

// ---------------------------------------------------------------------------
// StatusBar component
// ---------------------------------------------------------------------------

const StatusBar = {
    setup() {
        const status = inject('status');
        return { status };
    },
    template: `
        <div class="status-bar">
            <span class="logo">🤖 aiOS</span>
            <span class="indicator" v-if="status">
                <span class="dot" :class="status.docker_connected ? 'ok' : 'err'">●</span>
                Docker {{ status.docker_connected ? 'connected' : 'disconnected' }}
            </span>
            <span class="indicator" v-if="status">
                <span class="dot" :class="status.sandbox_running ? 'ok' : 'err'">●</span>
                Sandbox: {{ status.sandbox_status }}
            </span>
            <span v-if="status && status.is_mock" class="indicator">
                <span class="dot warn">●</span> mock mode
            </span>
            <span class="status-text" v-if="!status">Loading...</span>
        </div>
    `,
};

// ---------------------------------------------------------------------------
// MetricsCharts component — Chart.js history charts for Dashboard
// ---------------------------------------------------------------------------

const MetricsCharts = {
    props: ['history'],
    setup(props) {
        let cpuChart = null, ramChart = null, gpuChart = null;

        const hasGpu = computed(() => props.history && props.history.some(s => s.gpu));

        function makeChart(id, label, color) {
            const canvas = document.getElementById(id);
            if (!canvas || !window.Chart) return null;
            return new window.Chart(canvas, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{ label, data: [], borderColor: color, backgroundColor: color + '22',
                        fill: true, tension: 0.3, pointRadius: 2, borderWidth: 1.5 }]
                },
                options: {
                    animation: false, responsive: true, maintainAspectRatio: false,
                    scales: {
                        y: { min: 0, max: 100, grid: { color: '#3a3a3a' }, ticks: { color: '#858585', font: { size: 10 } } },
                        x: { grid: { color: '#3a3a3a' }, ticks: { color: '#858585', font: { size: 9 }, maxTicksLimit: 8, maxRotation: 0 } },
                    },
                    plugins: { legend: { display: false } },
                },
            });
        }

        function updateCharts() {
            if (!props.history || !props.history.length) return;
            const now = Date.now() / 1000;
            const labels = props.history.map(s => {
                const ago = Math.round(now - s.ts);
                return ago < 60 ? `${ago}s` : `${Math.round(ago / 60)}m`;
            });
            if (cpuChart) { cpuChart.data.labels = labels; cpuChart.data.datasets[0].data = props.history.map(s => s.cpu_percent); cpuChart.update('none'); }
            if (ramChart) { ramChart.data.labels = labels; ramChart.data.datasets[0].data = props.history.map(s => s.mem_percent); ramChart.update('none'); }
            if (gpuChart) { gpuChart.data.labels = labels; gpuChart.data.datasets[0].data = props.history.map(s => s.gpu ? s.gpu.utilization : 0); gpuChart.update('none'); }
        }

        onMounted(() => {
            cpuChart = makeChart('metrics-cpu', 'CPU %', '#5ca4f5');
            ramChart = makeChart('metrics-ram', 'RAM %', '#e8b84b');
            if (hasGpu.value) gpuChart = makeChart('metrics-gpu', 'GPU %', '#6ddb8b');
            updateCharts();
        });

        onUnmounted(() => {
            cpuChart?.destroy(); ramChart?.destroy(); gpuChart?.destroy();
        });

        watch(() => props.history, updateCharts, { deep: true });

        return { hasGpu };
    },
    template: `
        <div style="margin-top:14px">
            <h3>Resource History</h3>
            <div style="display:grid; gap:12px; grid-template-columns:repeat(auto-fill, minmax(240px, 1fr))">
                <div style="background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:10px">
                    <div style="font-size:11px; color:var(--muted); margin-bottom:4px">CPU %</div>
                    <div style="height:70px; position:relative"><canvas id="metrics-cpu"></canvas></div>
                </div>
                <div style="background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:10px">
                    <div style="font-size:11px; color:var(--muted); margin-bottom:4px">Memory %</div>
                    <div style="height:70px; position:relative"><canvas id="metrics-ram"></canvas></div>
                </div>
                <div v-if="hasGpu" style="background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); padding:10px">
                    <div style="font-size:11px; color:var(--muted); margin-bottom:4px">GPU %</div>
                    <div style="height:70px; position:relative"><canvas id="metrics-gpu"></canvas></div>
                </div>
            </div>
        </div>
    `,
};

// ---------------------------------------------------------------------------
// DashboardPanel component
// ---------------------------------------------------------------------------

const DashboardPanel = {
    components: { MetricsCharts },
    setup() {
        const status = inject('status');
        const stats = ref(null);
        const statsHistory = ref([]);
        const restarting = ref(false);
        const restartMsg = ref('');
        const logsOutput = ref('');
        const logsRunning = ref(false);
        const showLogs = ref(false);
        const rebuildOutput = ref('');
        const rebuildRunning = ref(false);
        const showRebuild = ref(false);

        let stopLogs = null;
        let stopRebuild = null;
        let statsTimer = null;

        async function loadStats() {
            try {
                stats.value = await api.get('/api/sandbox/stats');
                statsHistory.value = await api.get('/api/sandbox/stats/history');
            } catch (_) {}
        }

        async function restart() {
            restarting.value = true;
            restartMsg.value = '';
            try {
                const result = await api.post('/api/sandbox/restart', {});
                restartMsg.value = result.ok ? '✔ Sandbox restarted.' : `Failed: ${result.error}`;
            } catch (e) {
                restartMsg.value = `Error: ${e.message}`;
            } finally {
                restarting.value = false;
            }
        }

        function toggleLogs() {
            if (logsRunning.value) {
                stopLogs?.();
                stopLogs = null;
                logsRunning.value = false;
                return;
            }
            logsOutput.value = '';
            showLogs.value = true;
            logsRunning.value = true;
            stopLogs = streamWs('/ws/logs', {
                onChunk: (chunk) => {
                    logsOutput.value += chunk;
                    nextTick(() => {
                        const el = document.getElementById('logs-pre');
                        if (el) el.parentElement.scrollTop = el.parentElement.scrollHeight;
                    });
                },
                onDone: () => { logsRunning.value = false; },
                onError: (e) => { logsOutput.value += `\nError: ${e}\n`; logsRunning.value = false; },
            });
        }

        function rebuild() {
            if (rebuildRunning.value) return;
            rebuildOutput.value = '';
            showRebuild.value = true;
            rebuildRunning.value = true;
            stopRebuild = streamWs('/ws/rebuild', {
                onChunk: (chunk) => {
                    rebuildOutput.value += chunk;
                    nextTick(() => {
                        const el = document.getElementById('rebuild-pre');
                        if (el) el.parentElement.scrollTop = el.parentElement.scrollHeight;
                    });
                },
                onDone: () => { rebuildRunning.value = false; },
                onError: (e) => { rebuildOutput.value += `\nError: ${e}\n`; rebuildRunning.value = false; },
            });
        }

        function statBarClass(pct) {
            if (pct > 85) return 'err';
            if (pct > 60) return 'warn';
            return 'ok';
        }

        onMounted(() => {
            loadStats();
            statsTimer = setInterval(loadStats, 5000);
        });

        onUnmounted(() => {
            clearInterval(statsTimer);
            stopLogs?.();
            stopRebuild?.();
        });

        return {
            status, stats, statsHistory, restarting, restartMsg,
            logsOutput, logsRunning, showLogs,
            rebuildOutput, rebuildRunning, showRebuild,
            restart, toggleLogs, rebuild, statBarClass,
        };
    },
    template: `
        <div>
            <div class="panel">
                <h2>System Status</h2>
                <div class="cards" v-if="status">
                    <div class="card" :class="status.docker_connected ? 'card-ok' : 'card-err'">
                        <div class="card-label">Docker Socket</div>
                        <div class="card-value">{{ status.docker_connected ? 'Connected' : 'Disconnected' }}</div>
                    </div>
                    <div class="card" :class="status.sandbox_running ? 'card-ok' : 'card-err'">
                        <div class="card-label">Sandbox</div>
                        <div class="card-value">{{ status.sandbox_status }}</div>
                    </div>
                    <div class="card card-info" v-if="stats && !stats.is_mock">
                        <div class="card-label">CPU</div>
                        <div class="card-value">{{ stats.cpu_percent }}%</div>
                        <div class="stat-bar">
                            <div class="stat-bar-fill"
                                :class="statBarClass(stats.cpu_percent)"
                                :style="{ width: Math.min(stats.cpu_percent, 100) + '%' }"
                            ></div>
                        </div>
                    </div>
                    <div class="card card-info" v-if="stats && !stats.is_mock">
                        <div class="card-label">RAM — {{ stats.mem_usage_mb }} / {{ stats.mem_limit_mb }} MB</div>
                        <div class="card-value">{{ stats.mem_percent }}%</div>
                        <div class="stat-bar">
                            <div class="stat-bar-fill"
                                :class="statBarClass(stats.mem_percent)"
                                :style="{ width: Math.min(stats.mem_percent, 100) + '%' }"
                            ></div>
                        </div>
                    </div>
                    <div class="card card-info" v-if="stats && stats.gpu">
                        <div class="card-label">GPU — {{ stats.gpu.name }}</div>
                        <div class="card-value">{{ stats.gpu.utilization }}% &nbsp;<span class="muted" style="font-size:11px">{{ stats.gpu.mem_used_mb }}/{{ stats.gpu.mem_total_mb }} MB</span></div>
                        <div class="stat-bar">
                            <div class="stat-bar-fill"
                                :class="statBarClass(stats.gpu.utilization)"
                                :style="{ width: Math.min(stats.gpu.utilization, 100) + '%' }"
                            ></div>
                        </div>
                    </div>
                </div>
                <div v-else-if="!status" class="muted">Loading status...</div>

                <div class="form-row" style="margin-top:14px; gap:8px; flex-wrap:wrap">
                    <button class="btn-secondary" @click="restart" :disabled="restarting">
                        {{ restarting ? 'Restarting…' : '↺ Restart Sandbox' }}
                    </button>
                    <button class="btn-secondary" @click="rebuild" :disabled="rebuildRunning">
                        {{ rebuildRunning ? 'Building…' : '⚒ Rebuild Image' }}
                    </button>
                    <button class="btn-secondary" @click="toggleLogs">
                        {{ logsRunning ? '■ Stop Logs' : '▶ Live Logs' }}
                    </button>
                </div>
                <div v-if="restartMsg"
                    :class="restartMsg.startsWith('✔') ? 'success-msg' : 'error-msg'"
                    style="margin-top:8px"
                >{{ restartMsg }}</div>
            </div>

            <div class="panel" v-if="showLogs">
                <h2>Live Container Logs</h2>
                <div class="terminal-output">
                    <pre id="logs-pre" :class="{ 'terminal-cursor': logsRunning }">{{ logsOutput || 'Waiting for log stream…' }}</pre>
                </div>
                <button class="btn-sm" @click="logsOutput = ''" style="margin-top:6px">Clear</button>
            </div>

            <div class="panel" v-if="showRebuild">
                <h2>Rebuild Output</h2>
                <div class="terminal-output">
                    <pre id="rebuild-pre" :class="{ 'terminal-cursor': rebuildRunning }">{{ rebuildOutput || 'Waiting for build output…' }}</pre>
                </div>
                <button class="btn-sm" @click="rebuildOutput = ''" style="margin-top:6px">Clear</button>
            </div>

            <div class="panel" v-if="statsHistory.length">
                <MetricsCharts :history="statsHistory" />
            </div>
        </div>
    `,
};

// ---------------------------------------------------------------------------
// TerminalPanel component
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// TerminalPanel component
// ---------------------------------------------------------------------------

const TerminalPanel = {
    setup() {
        const ecosystem = ref('uv');
        const pkgName = ref('');
        const rawCmd = ref('');
        const output = ref('');
        const running = ref(false);
        const bakeIntoDockerfile = ref(false);
        const saveNote = ref(false);
        const error = ref('');
        const history = ref(loadHistory());
        const histIdx = ref(-1);
        const histDraft = ref('');

        const snippets = ref([
            { title: "uv install", code: "uv pip install -r requirements.txt" },
            { title: "pip list", code: "pip list" },
            { title: "conda env list", code: "conda env list" },
            { title: "system updates", code: "dnf update -y" },
            { title: "running processes", code: "ps aux" },
            { title: "listening ports", code: "ss -tlnp" },
        ]);

        const newSnipTitle = ref('');
        const newSnipCode = ref('');

        let stopWs = null;

        function buildCommand() {
            if (rawCmd.value.trim()) return rawCmd.value.trim();
            const pkg = pkgName.value.trim();
            if (!pkg) return null;
            const cmds = {
                uv: `uv pip install ${pkg}`,
                conda: `conda install -y ${pkg}`,
                dnf: `dnf install -y ${pkg}`,
                npm: `npm install -g ${pkg}`,
            };
            return cmds[ecosystem.value] || `pip install ${pkg}`;
        }

        async function run() {
            const cmd = buildCommand();
            if (!cmd) { error.value = 'Enter a package name or command.'; return; }
            error.value = '';
            output.value = '';
            running.value = true;
            history.value = pushHistory(cmd, history.value);
            histIdx.value = -1;

            stopWs = streamExec(cmd, {
                onChunk: (chunk) => {
                    output.value += chunk;
                    nextTick(() => {
                        const el = document.getElementById('terminal-pre-output');
                        if (el) el.parentElement.scrollTop = el.parentElement.scrollHeight;
                    });
                },
                onDone: async () => {
                    running.value = false;
                    const pkg = pkgName.value.trim();
                    if (bakeIntoDockerfile.value && pkg) {
                        try {
                            await api.post('/api/config/dockerfile', {
                                package: pkg, ecosystem: ecosystem.value, use_sudo: false,
                            });
                        } catch (_) {}
                    }
                    if (saveNote.value && pkg) {
                        try {
                            await api.post('/api/config/readme', {
                                note: `Installed ${pkg} via ${ecosystem.value}`,
                            });
                        } catch (_) {}
                    }
                },
                onError: (msg) => {
                    output.value += `\nError: ${msg}\n`;
                    running.value = false;
                },
            });
        }

        function clearOutput() { output.value = ''; }

        function onRawKeydown(e) {
            if (e.key === 'ArrowUp') {
                e.preventDefault();
                if (histIdx.value === -1) histDraft.value = rawCmd.value;
                if (histIdx.value < history.value.length - 1) {
                    histIdx.value++;
                    rawCmd.value = history.value[histIdx.value];
                }
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                if (histIdx.value > 0) {
                    histIdx.value--;
                    rawCmd.value = history.value[histIdx.value];
                } else if (histIdx.value === 0) {
                    histIdx.value = -1;
                    rawCmd.value = histDraft.value;
                }
            }
        }

        function loadCustomSnippets() {
            try {
                const stored = JSON.parse(localStorage.getItem('aios_custom_snippets') || '[]');
                snippets.value = [...snippets.value.filter(s => !s.custom), ...stored.map(s => ({ ...s, custom: true }))];
            } catch (_) {}
        }

        function addCustomSnippet() {
            if (!newSnipTitle.value || !newSnipCode.value) return;
            const newSnip = {
                title: newSnipTitle.value,
                code: newSnipCode.value,
                custom: true
            };
            const stored = JSON.parse(localStorage.getItem('aios_custom_snippets') || '[]');
            stored.push(newSnip);
            localStorage.setItem('aios_custom_snippets', JSON.stringify(stored));
            newSnipTitle.value = '';
            newSnipCode.value = '';
            loadCustomSnippets();
            addToast('Custom snippet saved.', 'success');
        }

        function deleteSnippet(snip) {
            const stored = JSON.parse(localStorage.getItem('aios_custom_snippets') || '[]');
            const next = stored.filter(s => s.title !== snip.title || s.code !== snip.code);
            localStorage.setItem('aios_custom_snippets', JSON.stringify(next));
            loadCustomSnippets();
            addToast('Snippet removed.', 'info');
        }

        function useSnippet(code) {
            rawCmd.value = code;
            addToast('Snippet loaded in prompt.', 'success');
        }

        loadCustomSnippets();

        return {
            ecosystem, pkgName, rawCmd, output, running,
            bakeIntoDockerfile, saveNote, error,
            history, histIdx,
            snippets, newSnipTitle, newSnipCode,
            run, clearOutput, onRawKeydown,
            addCustomSnippet, deleteSnippet, useSnippet,
        };
    },
    template: `
        <div class="terminal-with-snippets">
            <div class="panel">
                <h2>Terminal</h2>
                <div class="form-row">
                    <select v-model="ecosystem" class="input-flex" style="max-width:110px">
                        <option value="uv">uv pip</option>
                        <option value="conda">conda</option>
                        <option value="dnf">dnf</option>
                        <option value="npm">npm</option>
                    </select>
                    <input type="text" v-model="pkgName" placeholder="package name" class="input-flex" @keyup.enter="run" />
                    <button class="btn-primary" @click="run" :disabled="running">
                        {{ running ? 'Running…' : 'Install' }}
                    </button>
                </div>
                <div class="form-row">
                    <input
                        type="text"
                        v-model="rawCmd"
                        placeholder="Or type a raw command… (↑↓ history)"
                        class="input-flex"
                        @keyup.enter="run"
                        @keydown="onRawKeydown"
                    />
                    <button class="btn-secondary" @click="run" :disabled="running">Run</button>
                </div>
                <div v-if="history.length" class="hint" style="margin-bottom:8px">
                    ↑↓ to navigate {{ history.length }} saved command{{ history.length === 1 ? '' : 's' }}
                </div>
                <label class="checkbox-row">
                    <input type="checkbox" v-model="bakeIntoDockerfile" /> Bake into Dockerfile
                </label>
                <label class="checkbox-row">
                    <input type="checkbox" v-model="saveNote" /> Save note to README
                </label>
                <div v-if="error" class="error-msg">{{ error }}</div>
                <div class="terminal-output">
                    <pre id="terminal-pre-output" :class="{ 'terminal-cursor': running }">{{ output || (running ? '' : 'Output will appear here…') }}</pre>
                </div>
                <button class="btn-sm" @click="clearOutput" :disabled="running">Clear</button>
            </div>

            <div class="snippets-panel">
                <h3>Snippet Library</h3>
                <div class="snippet-list">
                    <div v-for="snip in snippets" :key="snip.title" class="snippet-card" @click="useSnippet(snip.code)">
                        <div style="display:flex; justify-content:space-between; align-items:center">
                            <span class="snippet-title">{{ snip.title }}</span>
                            <button v-if="snip.custom" class="btn-sm" style="padding:1px 4px; font-size:10px" @click.stop="deleteSnippet(snip)">✕</button>
                        </div>
                        <div class="snippet-code">{{ snip.code }}</div>
                    </div>
                </div>
                <div style="border-top: 1px solid var(--border); padding-top:10px; margin-top:5px">
                    <h4 style="font-size:11px; margin-bottom:6px" class="muted">Add Custom Snippet</h4>
                    <input type="text" v-model="newSnipTitle" placeholder="Snippet name..." style="width:100%; margin-bottom:6px" />
                    <input type="text" v-model="newSnipCode" placeholder="Command..." style="width:100%; margin-bottom:6px" />
                    <button class="btn-secondary btn-sm" style="width:100%" @click="addCustomSnippet" :disabled="!newSnipTitle || !newSnipCode">Save Snippet</button>
                </div>
            </div>
        </div>
    `,
};

// ---------------------------------------------------------------------------
// PtyTerminalPanel component — full interactive shell via xterm.js + PTY WebSocket
// ---------------------------------------------------------------------------

const PtyTerminalPanel = {
    setup() {
        const connected = ref(false);
        const connecting = ref(false);
        const termContainer = ref(null);

        let term = null;
        let fitAddon = null;
        let ws = null;

        function connect() {
            if (ws || connected.value) return;
            const XTerm = window.Terminal;
            const XFitAddon = window.FitAddon && window.FitAddon.FitAddon;
            if (!XTerm) { addToast('xterm.js not loaded — check CDN', 'error'); return; }

            connecting.value = true;
            term = new XTerm({
                cursorBlink: true,
                fontSize: 13,
                fontFamily: 'JetBrains Mono, Cascadia Code, monospace',
                theme: { background: '#1e1e1e', foreground: '#d4d4d4', cursor: '#007acc' },
            });

            if (XFitAddon) { fitAddon = new XFitAddon(); term.loadAddon(fitAddon); }
            if (termContainer.value) term.open(termContainer.value);
            if (fitAddon) fitAddon.fit();

            const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${proto}//${location.host}/ws/pty`);
            ws.binaryType = 'arraybuffer';

            ws.onopen = () => {
                connecting.value = false;
                connected.value = true;
                if (fitAddon) {
                    const d = fitAddon.proposeDimensions();
                    if (d) ws.send(JSON.stringify({ type: 'resize', rows: d.rows, cols: d.cols }));
                }
            };
            ws.onmessage = (e) => {
                if (e.data instanceof ArrayBuffer) term.write(new Uint8Array(e.data));
                else term.write(e.data);
            };
            ws.onclose = () => {
                connected.value = false;
                connecting.value = false;
                term && term.writeln('\r\n\r\n[Session closed]');
            };
            ws.onerror = () => { addToast('PTY connection error', 'error'); connecting.value = false; };

            term.onData((data) => { if (ws && ws.readyState === 1) ws.send(data); });
            term.onResize(({ rows, cols }) => {
                if (ws && ws.readyState === 1) ws.send(JSON.stringify({ type: 'resize', rows, cols }));
            });
        }

        function disconnect() {
            ws && ws.close(); ws = null;
            term && term.dispose(); term = null;
            connected.value = false;
        }

        onUnmounted(disconnect);

        return { connected, connecting, termContainer, connect, disconnect };
    },
    template: `
        <div class="panel">
            <h2>PTY Shell</h2>
            <div class="form-row" style="margin-bottom:10px; gap:8px">
                <button class="btn-primary" @click="connect" :disabled="connected || connecting">
                    {{ connecting ? 'Connecting…' : '▶ Open Shell' }}
                </button>
                <button class="btn-secondary" @click="disconnect" :disabled="!connected">Disconnect</button>
                <span v-if="connected" style="color:var(--ok); font-size:12px; align-self:center">● Shell active — ai_tui_sandbox</span>
            </div>
            <div ref="termContainer" style="height:480px; background:#1e1e1e; border:1px solid var(--border); border-radius:var(--radius); overflow:hidden"></div>
        </div>
    `,
};

// ---------------------------------------------------------------------------
// VolumePanel component
// ---------------------------------------------------------------------------

const VolumePanel = {
    setup() {
        const route = VueRouter.useRoute();
        const router = VueRouter.useRouter();
        const view = ref('volumes');
        const volumes = ref([]);
        const browseIdx = ref(null);
        const browseVol = ref(null);
        const files = ref([]);
        const currentPath = ref('');
        const pathHistory = ref([]);
        const loadingFiles = ref(false);
        const chmodTarget = ref(null);
        const chmodMode = ref('');
        const error = ref('');
        const modeMsg = ref('');
        const deleteConfirm = ref(null);

        async function loadVolumes() {
            try {
                volumes.value = await api.get('/api/volumes');
                const volIdx = route.query.volIdx;
                const dir = route.query.dir;
                if (volIdx !== undefined && dir) {
                    const idx = parseInt(volIdx, 10);
                    const vol = volumes.value.find(v => v.index === idx);
                    if (vol) {
                        browseIdx.value = vol.index;
                        browseVol.value = vol;
                        currentPath.value = dir;
                        const root = vol.container_path;
                        if (dir.startsWith(root) && dir !== root) {
                            const relative = dir.substring(root.length).split('/').filter(Boolean);
                            let temp = root;
                            pathHistory.value = [root];
                            for (let i = 0; i < relative.length - 1; i++) {
                                temp += '/' + relative[i];
                                pathHistory.value.push(temp);
                            }
                        } else {
                            pathHistory.value = [];
                        }
                        view.value = 'browser';
                        await loadFiles(vol.index, dir);
                    }
                } else if (browseVol.value !== null) {
                    browseVol.value = volumes.value.find(v => v.index === browseIdx.value) || null;
                }
            } catch (e) {
                error.value = `Failed to load volumes: ${e.message}`;
            }
        }

        async function loadFiles(idx, path) {
            loadingFiles.value = true;
            files.value = [];
            chmodTarget.value = null;
            try {
                files.value = await api.get(`/api/volumes/${idx}/files?path=${encodeURIComponent(path)}`);
            } catch (e) {
                error.value = `Failed to list files: ${e.message}`;
            } finally {
                loadingFiles.value = false;
            }
        }

        async function enterVolume(vol) {
            browseIdx.value = vol.index;
            browseVol.value = vol;
            currentPath.value = vol.container_path;
            pathHistory.value = [];
            view.value = 'browser';
            await loadFiles(vol.index, vol.container_path);
        }

        function backToVolumes() {
            view.value = 'volumes';
            browseIdx.value = null;
            browseVol.value = null;
            files.value = [];
            currentPath.value = '';
            pathHistory.value = [];
            modeMsg.value = '';
        }

        async function goBack() {
            if (pathHistory.value.length) {
                const prev = pathHistory.value.pop();
                currentPath.value = prev;
                await loadFiles(browseIdx.value, prev);
            } else {
                backToVolumes();
            }
        }

        async function enterDir(file) {
            if (!file.is_dir || file.name === currentPath.value) return;
            pathHistory.value.push(currentPath.value);
            currentPath.value = file.name;
            await loadFiles(browseIdx.value, file.name);
        }

        async function navigateTo(path) {
            if (path === currentPath.value) return;
            pathHistory.value.push(currentPath.value);
            currentPath.value = path;
            await loadFiles(browseIdx.value, path);
        }

        const breadcrumbs = computed(() => {
            const segs = [{ label: 'Volumes', path: null }];
            if (!currentPath.value) return segs;
            const parts = currentPath.value.split('/').filter(Boolean);
            let built = '';
            for (const part of parts) {
                built += '/' + part;
                segs.push({ label: part, path: built });
            }
            return segs;
        });

        async function toggleMode(vol) {
            const target = vol || browseVol.value;
            if (!target) return;
            const newMode = target.mode === 'rw' ? 'ro' : 'rw';
            modeMsg.value = '';
            try {
                const result = await api.post(`/api/volumes/${target.index}/mode`, { mode: newMode });
                await loadVolumes();
                if (result.live_applied) {
                    modeMsg.value = `live:${target.container_path} → ${newMode}`;
                } else {
                    modeMsg.value = `compose:docker-compose.yml updated. Live apply failed (${result.live_msg || 'unknown'}). Restart container to apply.`;
                }
            } catch (e) {
                error.value = `Failed to update mode: ${e.message}`;
            }
        }

        async function deleteVolume(vol) {
            if (deleteConfirm.value !== vol.index) {
                deleteConfirm.value = vol.index;
                return;
            }
            deleteConfirm.value = null;
            try {
                await api.delete(`/api/volumes/${vol.index}`);
                await loadVolumes();
            } catch (e) {
                error.value = `Delete failed: ${e.message}`;
            }
        }

        function isWritable(file) {
            return Boolean(parseInt(file.permissions, 8) & 0o200);
        }

        function isHidden(file) {
            return parseInt(file.permissions, 8) === 0;
        }

        async function toggleHide(file) {
            const newMode = isHidden(file) ? (file.is_dir ? '755' : '644') : '000';
            try {
                await api.post('/api/volumes/chmod', { path: file.name, mode: newMode });
                await loadFiles(browseIdx.value, currentPath.value);
            } catch (e) {
                error.value = `Hide failed: ${e.message}`;
            }
        }

        async function toggleFileMode(file) {
            const writable = isWritable(file);
            const newMode = writable
                ? (file.is_dir ? '555' : '444')
                : (file.is_dir ? '755' : '644');
            try {
                await api.post('/api/volumes/chmod', { path: file.name, mode: newMode });
                await loadFiles(browseIdx.value, currentPath.value);
            } catch (e) {
                error.value = `Mode change failed: ${e.message}`;
            }
        }

        function startChmod(file) {
            chmodTarget.value = file;
            chmodMode.value = file.permissions;
        }

        async function applyChmodReal() {
            if (!chmodTarget.value) return;
            try {
                await api.post('/api/volumes/chmod', {
                    path: chmodTarget.value.name,
                    mode: chmodMode.value,
                });
                chmodTarget.value = null;
                await loadFiles(browseIdx.value, currentPath.value);
            } catch (e) {
                error.value = `chmod failed: ${e.message}`;
            }
        }

        function isEditable(file) {
            if (file.is_dir) return false;
            const ext = file.name.split('.').pop().toLowerCase();
            return ['txt', 'py', 'js', 'json', 'sh', 'md', 'yml', 'yaml', 'css', 'html'].includes(ext);
        }

        function isDatabase(file) {
            if (file.is_dir) return false;
            const ext = file.name.split('.').pop().toLowerCase();
            return ['db', 'sqlite', 'sqlite3'].includes(ext);
        }

        function editFile(file) {
            router.push({ 
                path: '/editor', 
                query: { 
                    path: file.name,
                    volIdx: browseIdx.value,
                    dir: currentPath.value
                } 
            });
        }

        function inspectDb(file) {
            router.push({ 
                path: '/db-viewer', 
                query: { 
                    path: file.name,
                    volIdx: browseIdx.value,
                    dir: currentPath.value
                } 
            });
        }

        function downloadFile(file) {
            window.open(`/api/volumes/download?path=${encodeURIComponent(file.name)}`, '_blank');
            addToast(`Download of ${basename(file.name)} initiated.`, 'success');
        }

        async function uploadFile(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const formData = new FormData();
            formData.append('file', file);
            formData.append('path', `${currentPath.value}/${file.name}`);
            
            try {
                const res = await fetch('/api/volumes/upload', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                if (data.ok) {
                    addToast(`File ${file.name} uploaded successfully.`, 'success');
                    await loadFiles(browseIdx.value, currentPath.value);
                } else {
                    addToast(`Upload failed: ${data.detail}`, 'error');
                }
            } catch (e) {
                addToast(`Upload error: ${e.message}`, 'error');
            }
        }

        function isEnvFile(file) {
            if (file.is_dir) return false;
            return basename(file.name) === '.env' || file.name.endsWith('.env');
        }

        function manageEnv(file) {
            router.push({
                path: '/config',
                query: {
                    tab: 'env-manager',
                    path: file.name,
                    volIdx: browseIdx.value,
                    dir: currentPath.value
                }
            });
        }

        onMounted(loadVolumes);

        return {
            view, volumes, browseIdx, browseVol, files, currentPath, pathHistory,
            breadcrumbs, loadingFiles, chmodTarget, chmodMode, error, modeMsg, deleteConfirm,
            enterVolume, backToVolumes, goBack, enterDir, navigateTo,
            toggleMode, deleteVolume, startChmod, applyChmodReal,
            isWritable, toggleFileMode, isHidden, toggleHide,
            basename, octalToSymbolic,
            isEditable, isDatabase, editFile, inspectDb, downloadFile, uploadFile,
            isEnvFile, manageEnv,
        };
    },
    template: `
        <div class="panel">
            <div v-if="error" class="error-msg">{{ error }}</div>
            <div v-if="modeMsg" :class="modeMsg.startsWith('live:') ? 'success-msg' : 'warn-msg'">
                {{ modeMsg.startsWith('live:') ? '✔ Applied live — ' + modeMsg.slice(5) : modeMsg.slice(8) }}
            </div>

            <!-- ── Volumes list ── -->
            <div v-if="view === 'volumes'">
                <h2>Volumes</h2>
                <table class="data-table" v-if="volumes.length">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Host Path</th>
                            <th>Container Path</th>
                            <th>Mode</th>
                            <th>SELinux</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="vol in volumes" :key="vol.index"
                            class="vol-row"
                            @click="enterVolume(vol)"
                        >
                            <td class="muted">{{ vol.index }}</td>
                            <td class="path">{{ vol.host_path }}</td>
                            <td class="path">{{ vol.container_path }}</td>
                            <td><span :class="vol.mode === 'rw' ? 'badge-rw' : 'badge-ro'">{{ vol.mode }}</span></td>
                            <td class="muted">{{ vol.selinux || '—' }}</td>
                            <td @click.stop>
                                <div class="actions-cell">
                                    <button class="btn-sm" @click="toggleMode(vol)">
                                        → {{ vol.mode === 'rw' ? 'ro' : 'rw' }}
                                    </button>
                                    <button
                                        :class="deleteConfirm === vol.index ? 'btn-confirm' : 'btn-danger'"
                                        @click="deleteVolume(vol)"
                                    >
                                        {{ deleteConfirm === vol.index ? 'Confirm?' : 'Detach' }}
                                    </button>
                                    <button v-if="deleteConfirm === vol.index" class="btn-sm" @click.stop="deleteConfirm = null">✕</button>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div v-else class="muted hint">No volumes found in docker-compose.yml.</div>
                <div class="hint" style="margin-top:10px">Click a row to browse its contents.</div>
            </div>

            <!-- ── File browser ── -->
            <div v-else>
                <div class="file-browser-nav">
                    <button class="btn-sm" @click="goBack">← Back</button>
                    <div class="breadcrumb">
                        <span v-for="(seg, i) in breadcrumbs" :key="i" class="breadcrumb-item">
                            <span v-if="i > 0" class="breadcrumb-sep">/</span>
                            <span
                                class="breadcrumb-seg"
                                :class="{ active: i === breadcrumbs.length - 1 }"
                                @click="seg.path === null ? backToVolumes() : (i < breadcrumbs.length - 1 && navigateTo(seg.path))"
                            >{{ seg.label }}</span>
                        </span>
                    </div>
                    
                    <label class="btn-upload-label" style="margin-right:8px" v-if="browseVol">
                        📤 Upload File
                        <input type="file" @change="uploadFile" style="display:none" />
                    </label>

                    <div v-if="browseVol" class="actions-cell" style="flex-shrink:0">
                        <span :class="browseVol.mode === 'rw' ? 'badge-rw' : 'badge-ro'">{{ browseVol.mode }}</span>
                        <button class="btn-sm" @click="toggleMode(null)">
                            → {{ browseVol.mode === 'rw' ? 'ro' : 'rw' }}
                        </button>
                    </div>
                </div>

                <div v-if="loadingFiles" class="muted" style="padding: 8px 0">Loading…</div>
                <div class="file-browser-scroll" v-else-if="files.length">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Permissions</th>
                                <th>Symbolic</th>
                                <th>Owner</th>
                                <th>Size</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="file in files.filter(f => f.name !== currentPath)" :key="file.name"
                                :class="{ 'dir-row': file.is_dir }"
                                @click="enterDir(file)"
                            >
                                <td>
                                    <span class="file-icon">{{ file.is_dir ? '📁' : '📄' }}</span>
                                    {{ basename(file.name) }}
                                </td>
                                <td><code>{{ file.permissions }}</code></td>
                                <td><code class="muted">{{ octalToSymbolic(file.permissions) }}</code></td>
                                <td class="muted">{{ file.owner }}</td>
                                <td class="muted">{{ file.size }}</td>
                                <td @click.stop>
                                    <div class="actions-cell">
                                        <!-- Slot 1: Primary Action (edit / inspect / placeholder) -->
                                        <button class="btn-sm btn-primary" style="width: 70px; text-align: center" v-if="isEditable(file)" @click="editFile(file)">edit</button>
                                        <button class="btn-sm btn-primary" style="width: 70px; text-align: center" v-else-if="isDatabase(file)" @click="inspectDb(file)">inspect</button>
                                        <button class="btn-sm btn-env-mgr" style="width: 70px; text-align: center" v-else-if="isEnvFile(file)" @click="manageEnv(file)">env</button>
                                        <button class="btn-sm" style="width: 70px; text-align: center; visibility: hidden; pointer-events: none;" v-else>inspect</button>

                                        <!-- Slot 2: Download Action (⬇ / placeholder) -->
                                        <button class="btn-sm" style="width: 32px; text-align: center" v-if="!file.is_dir" @click="downloadFile(file)">⬇</button>
                                        <button class="btn-sm" style="width: 32px; text-align: center; visibility: hidden; pointer-events: none;" v-else>⬇</button>

                                        <!-- Slot 3: Chmod Action -->
                                        <button class="btn-sm" style="width: 60px; text-align: center" @click="startChmod(file)">chmod</button>

                                        <!-- Slot 4: Hide Action (fixed width to prevent toggle shift) -->
                                        <button class="btn-sm btn-hide" style="width: 70px; text-align: center" @click="toggleHide(file)">
                                            {{ isHidden(file) ? 'unhide' : 'hide' }}
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div v-else class="muted hint">No files found or directory is empty.</div>

                <div v-if="chmodTarget" class="chmod-form">
                    <div class="chmod-form-header">
                        <span class="chmod-path">{{ basename(chmodTarget.name) }}</span>
                        <button class="btn-secondary btn-sm" @click="chmodTarget = null">✕</button>
                    </div>
                    <div class="chmod-presets">
                        <span class="chmod-preset-label">AI access:</span>
                        <button class="btn-sm preset-rw" @click="chmodMode = chmodTarget.is_dir ? '755' : '644'">rw — 755/644</button>
                        <button class="btn-sm preset-ro" @click="chmodMode = chmodTarget.is_dir ? '555' : '444'">ro — 555/444</button>
                        <button class="btn-sm preset-hide" @click="chmodMode = '000'">hide — 000</button>
                        <button class="btn-sm preset-priv" @click="chmodMode = chmodTarget.is_dir ? '700' : '600'">private — 700/600</button>
                    </div>
                    <div class="chmod-note">
                        <code>r</code>=read &nbsp;<code>w</code>=write &nbsp;<code>x</code>=exec &nbsp;|&nbsp;
                        <code>7</code>=rwx &nbsp;<code>6</code>=rw- &nbsp;<code>5</code>=r-x &nbsp;<code>4</code>=r-- &nbsp;<code>0</code>=---
                        &nbsp;|&nbsp; digits: <em>owner / group / others</em>
                    </div>
                    <div class="chmod-apply-row">
                        <input type="text" v-model="chmodMode" placeholder="755" style="width:70px; font-family: var(--font-mono)" />
                        <button class="btn-primary btn-sm" @click="applyChmodReal">Apply</button>
                    </div>
                </div>

                <div class="hint" style="margin-top:10px">
                    Volume mode changes write to <code>docker-compose.yml</code> and apply live (requires <code>SYS_ADMIN</code> cap on sandbox).
                </div>
    `,
};

// ---------------------------------------------------------------------------
// ProcessesPanel component
// ---------------------------------------------------------------------------

const ProcessesPanel = {
    setup() {
        const activeTab = ref('processes');
        const processes = ref([]);
        const ports = ref([]);
        const search = ref('');
        let timer = null;

        async function loadData() {
            try {
                if (activeTab.value === 'processes') {
                    processes.value = await api.get('/api/sandbox/processes');
                } else {
                    ports.value = await api.get('/api/sandbox/ports');
                }
            } catch (e) {
                addToast(`Failed to load: ${e.message}`, 'error');
            }
        }

        async function killProc(pid) {
            try {
                const res = await api.post('/api/sandbox/processes/kill', { pid });
                if (res.ok) {
                    addToast(`Process ${pid} killed.`, 'success');
                    loadData();
                } else {
                    addToast(`Failed to kill process: ${res.error}`, 'error');
                }
            } catch (e) {
                addToast(`Error: ${e.message}`, 'error');
            }
        }

        const filteredProcesses = computed(() => {
            const query = search.value.toLowerCase().trim();
            if (!query) return processes.value;
            return processes.value.filter(p => 
                p.command.toLowerCase().includes(query) || 
                p.pid.includes(query) || 
                p.user.toLowerCase().includes(query)
            );
        });

        onMounted(() => {
            loadData();
            timer = setInterval(loadData, 5000);
        });

        onUnmounted(() => {
            clearInterval(timer);
        });

        return { activeTab, search, filteredProcesses, ports, killProc, loadData };
    },
    template: `
        <div class="panel">
            <h2>Processes & Ports</h2>
            <div class="processes-tabs">
                <button class="tab-btn" :class="{ active: activeTab === 'processes' }" @click="activeTab = 'processes'; loadData()">
                    ⚙ Running Processes ({{ filteredProcesses.length }})
                </button>
                <button class="tab-btn" :class="{ active: activeTab === 'ports' }" @click="activeTab = 'ports'; loadData()">
                    🔌 Listening Ports ({{ ports.length }})
                </button>
            </div>

            <!-- Processes Tab -->
            <div v-if="activeTab === 'processes'">
                <div class="form-row" style="margin-bottom:12px">
                    <input type="text" v-model="search" placeholder="Search processes by command/PID..." class="input-flex" />
                    <button class="btn-secondary text-sm" @click="loadData">Refresh</button>
                </div>
                <div class="file-browser-scroll" style="max-height: 480px">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>PID</th>
                                <th>USER</th>
                                <th>CPU%</th>
                                <th>MEM%</th>
                                <th>COMMAND</th>
                                <th>ACTIONS</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="p in filteredProcesses" :key="p.pid">
                                <td><code>{{ p.pid }}</code></td>
                                <td class="muted">{{ p.user }}</td>
                                <td>
                                    <div style="display:flex; align-items:center; gap:5px">
                                        <span style="min-width:36px; font-size:11px">{{ p.cpu }}%</span>
                                        <div class="stat-bar" style="width:44px; flex-shrink:0">
                                            <div class="stat-bar-fill" :class="parseFloat(p.cpu)>50?'err':parseFloat(p.cpu)>15?'warn':'ok'" :style="{width:Math.min(parseFloat(p.cpu)||0,100)+'%'}"></div>
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    <div style="display:flex; align-items:center; gap:5px">
                                        <span style="min-width:36px; font-size:11px">{{ p.mem }}%</span>
                                        <div class="stat-bar" style="width:44px; flex-shrink:0">
                                            <div class="stat-bar-fill" :class="parseFloat(p.mem)>50?'err':parseFloat(p.mem)>15?'warn':'ok'" :style="{width:Math.min(parseFloat(p.mem)||0,100)+'%'}"></div>
                                        </div>
                                    </div>
                                </td>
                                <td style="font-family: var(--font-mono); font-size:11px; max-width: 400px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap" :title="p.command">
                                    {{ p.command }}
                                </td>
                                <td>
                                    <button class="btn-danger" @click="killProc(p.pid)">Kill</button>
                                </td>
                            </tr>
                            <tr v-if="!filteredProcesses.length">
                                <td colspan="6" class="muted hint" style="text-align:center; padding: 20px">No running processes found.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Ports Tab -->
            <div v-else>
                <div class="form-row" style="margin-bottom:12px">
                    <button class="btn-secondary btn-sm" @click="loadData" style="margin-left: auto">Refresh</button>
                </div>
                <div class="file-browser-scroll">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Proto</th>
                                <th>Local Address</th>
                                <th>Program</th>
                                <th>PID</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="p in ports" :key="p.local_addr">
                                <td><span class="badge-rw">{{ p.proto }}</span></td>
                                <td><span class="port-badge">{{ p.local_addr }}</span></td>
                                <td class="path">{{ p.program }}</td>
                                <td><code>{{ p.pid }}</code></td>
                            </tr>
                            <tr v-if="!ports.length">
                                <td colspan="4" class="muted hint" style="text-align:center; padding: 20px">No active listening ports found.</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    `
};

// ---------------------------------------------------------------------------
// EditorPanel component
// ---------------------------------------------------------------------------

const EditorPanel = {
    setup() {
        const route = VueRouter.useRoute();
        const router = VueRouter.useRouter();
        const path = computed(() => route.query.path || '');
        const saving = ref(false);
        let cmInstance = null;

        async function loadFile() {
            if (!path.value) return;
            try {
                const res = await api.post('/api/editor/read', { path: path.value });
                if (res.ok) {
                    cmInstance.setValue(res.content);
                    detectAndSetMode();
                } else {
                    addToast(`Failed to load file: ${res.detail || 'unknown error'}`, 'error');
                }
            } catch (e) {
                addToast(`Error: ${e.message}`, 'error');
            }
        }

        function detectAndSetMode() {
            const ext = path.value.split('.').pop().toLowerCase();
            let mode = 'text/plain';
            if (ext === 'py') mode = 'python';
            else if (ext === 'js' || ext === 'json') mode = 'javascript';
            else if (ext === 'sh' || ext === 'bash') mode = 'shell';
            else if (ext === 'md') mode = 'markdown';
            else if (ext === 'yml' || ext === 'yaml') mode = 'yaml';
            cmInstance.setOption('mode', mode);
        }

        async function save() {
            if (!path.value) return;
            saving.value = true;
            try {
                const val = cmInstance.getValue();
                const res = await api.post('/api/editor/write', { path: path.value, content: val });
                if (res.ok) {
                    addToast('File saved successfully.', 'success');
                } else {
                    addToast(`Failed to save: ${res.detail || 'unknown error'}`, 'error');
                }
            } catch (e) {
                addToast(`Error: ${e.message}`, 'error');
            } finally {
                saving.value = false;
            }
        }

        onMounted(() => {
            const textarea = document.getElementById('cm-textarea');
            if (textarea) {
                cmInstance = CodeMirror.fromTextArea(textarea, {
                    lineNumbers: true,
                    theme: 'material-darker',
                    mode: 'text/plain',
                    viewportMargin: Infinity,
                });
                loadFile();
            }
        });

        function goBack() {
            const volIdx = route.query.volIdx;
            const dir = route.query.dir;
            if (volIdx !== undefined && dir) {
                router.push({ path: '/volumes', query: { volIdx, dir } });
            } else {
                router.push('/volumes');
            }
        }

        return { path, saving, save, goBack };
    },
    template: `
        <div class="panel">
            <h2>File Editor</h2>
            <div v-if="!path" class="muted hint" style="padding: 20px; text-align: center">
                No file selected. Please select a file to edit from the Volumes tab.
                <br/><br/>
                <button class="btn-primary" @click="goBack">Go to Volumes</button>
            </div>
            <div v-else>
                <div class="editor-container">
                    <div class="editor-header">
                        <span class="file-path">📝 {{ path }}</span>
                        <div class="actions-cell">
                            <button class="btn-secondary btn-sm" @click="goBack">Back</button>
                            <button class="btn-primary btn-sm" @click="save" :disabled="saving">
                                {{ saving ? 'Saving...' : '💾 Save' }}
                            </button>
                        </div>
                    </div>
                    <textarea id="cm-textarea"></textarea>
                </div>
            </div>
        </div>
    `
};

// ---------------------------------------------------------------------------
// DbViewerPanel component
// ---------------------------------------------------------------------------

const DbViewerPanel = {
    setup() {
        const route = VueRouter.useRoute();
        const router = VueRouter.useRouter();
        const path = computed(() => route.query.path || '');
        const tables = ref([]);
        const activeTable = ref('');
        const rawSql = ref('');
        const results = ref(null);
        const executing = ref(false);
        const error = ref('');

        async function loadTables() {
            if (!path.value) return;
            try {
                const res = await api.post('/api/db/query', {
                    db_path: path.value,
                    query: "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';"
                });
                if (res.ok) {
                    tables.value = res.rows.map(r => r.name);
                    if (tables.value.length) {
                        selectTable(tables.value[0]);
                    }
                } else {
                    addToast(`DB Load Failed: ${res.error || 'unknown error'}`, 'error');
                }
            } catch (e) {
                addToast(`DB Load Error: ${e.message}`, 'error');
            }
        }

        async function selectTable(tbl) {
            activeTable.value = tbl;
            rawSql.value = `SELECT * FROM "${tbl}" LIMIT 50;`;
            runQuery();
        }

        async function runQuery() {
            if (!path.value || !rawSql.value.trim()) return;
            executing.value = true;
            error.value = '';
            results.value = null;
            try {
                const res = await api.post('/api/db/query', {
                    db_path: path.value,
                    query: rawSql.value
                });
                if (res.ok) {
                    results.value = res;
                } else {
                    error.value = res.error;
                }
            } catch (e) {
                error.value = e.message;
            } finally {
                executing.value = false;
            }
        }

        onMounted(() => {
            if (path.value) {
                loadTables();
            }
        });

        function goBack() {
            const volIdx = route.query.volIdx;
            const dir = route.query.dir;
            if (volIdx !== undefined && dir) {
                router.push({ path: '/volumes', query: { volIdx, dir } });
            } else {
                router.push('/volumes');
            }
        }

        return { path, tables, activeTable, rawSql, results, executing, error, selectTable, runQuery, goBack };
    },
    template: `
        <div class="panel">
            <h2>SQLite DB Viewer</h2>
            <div v-if="!path" class="muted hint" style="padding: 20px; text-align: center">
                No database file selected. Select a SQLite database (.db / .sqlite) in the Volumes tab.
                <br/><br/>
                <button class="btn-primary" @click="goBack">Go to Volumes</button>
            </div>
            <div v-else>
                <div style="margin-bottom:10px; display:flex; justify-content:space-between; align-items:center">
                    <span class="path">🗄️ {{ path }}</span>
                    <button class="btn-secondary btn-sm" @click="goBack">Back</button>
                </div>
                <div class="db-viewer-layout">
                    <aside class="db-sidebar">
                        <h3>Tables</h3>
                        <ul class="db-table-list">
                            <li v-for="t in tables" :key="t" 
                                class="db-table-item" 
                                :class="{ active: activeTable === t }"
                                @click="selectTable(t)"
                            >
                                📊 {{ t }}
                            </li>
                            <li v-if="!tables.length" class="muted hint">No tables found.</li>
                        </ul>
                    </aside>
                    <main class="sql-editor-panel">
                        <textarea v-model="rawSql" rows="3" class="sql-textarea" placeholder="Enter custom SQL query here..."></textarea>
                        <div class="form-row">
                            <button class="btn-primary" @click="runQuery" :disabled="executing">
                                {{ executing ? 'Executing...' : '⚡ Run Query' }}
                            </button>
                        </div>
                        <div v-if="error" class="error-msg">{{ error }}</div>
                        <div v-if="results" style="margin-top:10px">
                            <div class="hint" style="margin-bottom:6px">
                                Query returned <strong>{{ results.count || 0 }}</strong> rows.
                            </div>
                            <div class="file-browser-scroll" style="max-height: 320px; overflow-x: auto" v-if="results.columns && results.columns.length">
                                <table class="data-table">
                                    <thead>
                                        <tr>
                                            <th v-for="col in results.columns" :key="col">{{ col }}</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr v-for="(row, idx) in results.rows" :key="idx">
                                            <td v-for="col in results.columns" :key="col" style="font-family:var(--font-mono); font-size:11px">
                                                {{ row[col] !== null ? row[col] : 'NULL' }}
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                            <div v-else-if="results.ok && !results.columns" class="success-msg">
                                Query executed successfully (affected {{ results.count }} rows).
                            </div>
                        </div>
                    </main>
                </div>
            </div>
        </div>
    `
};

// ---------------------------------------------------------------------------
// ConfigPanel component
// ---------------------------------------------------------------------------

const ConfigPanel = {
    setup() {
        const route = VueRouter.useRoute();
        const router = VueRouter.useRouter();
        const activeTab = ref('dockerfile');
        const tabs = [
            { id: 'dockerfile', label: 'Dockerfile' },
            { id: 'readme',     label: 'README' },
            { id: 'environment', label: 'Conda yml' },
            { id: 'env-manager', label: '.env Manager' },
            { id: 'volume',     label: 'Volume' },
        ];

        const df  = reactive({ package: '', ecosystem: 'uv', use_sudo: false });
        const rm  = reactive({ note: '' });
        const env = reactive({ package: '' });
        const vol = reactive({ host_path: '', container_path: '' });

        const customPath = computed(() => route.query.path || '');
        const dotenvVars = ref({});
        const containerEnvVars = ref({});
        const newEnvKey = ref('');
        const newEnvVal = ref('');

        const success = ref('');
        const error   = ref('');

        const registeredEnvPaths = ref([]);
        const selectedEnvPath = ref('');

        function loadRegisteredEnvPaths() {
            try {
                const data = localStorage.getItem('registered_env_paths');
                registeredEnvPaths.value = data ? JSON.parse(data) : [];
            } catch (e) {
                registeredEnvPaths.value = [];
            }
        }

        function registerEnvPath(path) {
            if (!path) return;
            loadRegisteredEnvPaths();
            if (!registeredEnvPaths.value.includes(path)) {
                registeredEnvPaths.value.push(path);
                localStorage.setItem('registered_env_paths', JSON.stringify(registeredEnvPaths.value));
            }
        }

        function unregisterEnvPath(path) {
            loadRegisteredEnvPaths();
            registeredEnvPaths.value = registeredEnvPaths.value.filter(p => p !== path);
            localStorage.setItem('registered_env_paths', JSON.stringify(registeredEnvPaths.value));
            if (customPath.value === path) {
                router.push({
                    path: '/config',
                    query: {
                        ...route.query,
                        path: undefined
                    }
                });
            }
        }

        function switchEnvFile() {
            router.push({
                path: '/config',
                query: {
                    ...route.query,
                    path: selectedEnvPath.value || undefined
                }
            });
        }

        watch(customPath, (newVal) => {
            selectedEnvPath.value = newVal || '';
            if (newVal) {
                registerEnvPath(newVal);
            }
            loadEnvVars();
        }, { immediate: true });

        function clearMessages() { success.value = ''; error.value = ''; }

        async function loadEnvVars() {
            try {
                const pathParam = customPath.value ? `?path=${encodeURIComponent(customPath.value)}` : '';
                const res = await api.get(`/api/sandbox/env${pathParam}`);
                dotenvVars.value = res.dotenv || {};
                containerEnvVars.value = res.container_env || {};
            } catch (_) {}
        }

        async function deleteEnvVar(key) {
            if (!confirm(`Are you sure you want to delete variable "${key}"?`)) return;
            try {
                const res = await api.post('/api/sandbox/env/delete', {
                    key: key,
                    path: customPath.value || null
                });
                if (res.ok) {
                    addToast(`Deleted ${key} successfully.`, 'success');
                    loadEnvVars();
                } else {
                    addToast(`Failed to delete: ${res.error}`, 'error');
                }
            } catch (e) {
                addToast(`Error: ${e.message}`, 'error');
            }
        }

        async function saveEnvVar() {
            if (!newEnvKey.value) return;
            try {
                const res = await api.post('/api/sandbox/env/save', {
                    key: newEnvKey.value,
                    value: newEnvVal.value,
                    path: customPath.value || null
                });
                if (res.ok) {
                    addToast(`Saved ${newEnvKey.value} successfully.`, 'success');
                    newEnvKey.value = '';
                    newEnvVal.value = '';
                    loadEnvVars();
                } else {
                    addToast(`Failed to save: ${res.error}`, 'error');
                }
            } catch (e) {
                addToast(`Error: ${e.message}`, 'error');
            }
        }

        async function submitDockerfile() {
            clearMessages();
            try {
                await api.post('/api/config/dockerfile', {
                    package: df.package, ecosystem: df.ecosystem, use_sudo: df.use_sudo,
                });
                success.value = `Added ${df.package} to Dockerfile.`;
                df.package = '';
            } catch (e) { error.value = e.message; }
        }

        async function submitReadme() {
            clearMessages();
            try {
                await api.post('/api/config/readme', { note: rm.note });
                success.value = 'Note appended to README.';
                rm.note = '';
            } catch (e) { error.value = e.message; }
        }

        async function submitEnvironment() {
            clearMessages();
            try {
                await api.post('/api/config/environment', { package: env.package });
                success.value = `Added ${env.package} to environment.yml.`;
                env.package = '';
            } catch (e) { error.value = e.message; }
        }

        async function submitVolume() {
            clearMessages();
            try {
                await api.post('/api/config/volume', {
                    host_path: vol.host_path,
                    container_path: vol.container_path,
                });
                success.value = 'Volume added to docker-compose.yml.';
                vol.host_path = '';
                vol.container_path = '';
            } catch (e) { error.value = e.message; }
        }

        function goBackToVolumes() {
            const volIdx = route.query.volIdx;
            const dir = route.query.dir;
            if (volIdx !== undefined && dir) {
                router.push({ path: '/volumes', query: { volIdx, dir } });
            } else {
                router.push('/volumes');
            }
        }

        onMounted(() => {
            if (route.query.tab) {
                activeTab.value = route.query.tab;
            }
            loadRegisteredEnvPaths();
            loadEnvVars();
        });

        return {
            activeTab, tabs,
            df, rm, env, vol,
            customPath, dotenvVars, containerEnvVars, newEnvKey, newEnvVal,
            registeredEnvPaths, selectedEnvPath, switchEnvFile, unregisterEnvPath, deleteEnvVar,
            success, error,
            submitDockerfile, submitReadme, submitEnvironment, submitVolume, saveEnvVar, loadEnvVars, goBackToVolumes,
            basename,
        };
    },
    template: `
        <div class="panel">
            <h2>Config</h2>

            <div class="tab-bar">
                <button
                    v-for="tab in tabs"
                    :key="tab.id"
                    class="tab-btn"
                    :class="{ active: activeTab === tab.id }"
                    @click="activeTab = tab.id; loadEnvVars()"
                >{{ tab.label }}</button>
            </div>

            <div v-if="success" class="success-msg">{{ success }}</div>
            <div v-if="error" class="error-msg">{{ error }}</div>

            <div v-if="activeTab === 'dockerfile'">
                <div class="form-group">
                    <label>Ecosystem</label>
                    <select v-model="df.ecosystem">
                        <option value="uv">uv pip</option>
                        <option value="conda">conda</option>
                        <option value="dnf">dnf</option>
                        <option value="npm">npm</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Package</label>
                    <input type="text" v-model="df.package" placeholder="e.g. requests" class="input-flex" />
                </div>
                <label class="checkbox-row">
                    <input type="checkbox" v-model="df.use_sudo" /> Use sudo
                </label>
                <button class="btn-primary" @click="submitDockerfile" :disabled="!df.package">Add to Dockerfile</button>
            </div>

            <div v-if="activeTab === 'readme'">
                <div class="form-group">
                    <label>Note</label>
                    <textarea v-model="rm.note" rows="4" placeholder="Note to append to README…"></textarea>
                </div>
                <button class="btn-primary" @click="submitReadme" :disabled="!rm.note">Append to README</button>
            </div>

            <div v-if="activeTab === 'environment'">
                <div class="form-group">
                    <label>Package</label>
                    <input type="text" v-model="env.package" placeholder="e.g. numpy" class="input-flex" />
                </div>
                <button class="btn-primary" @click="submitEnvironment" :disabled="!env.package">Add to environment.yml</button>
            </div>

            <div v-if="activeTab === 'env-manager'">
                <!-- Premium registered .env selector bar -->
                <div style="margin-bottom:16px; display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.03); padding:12px; border-radius:6px; border:1px solid var(--border); gap:12px">
                    <div style="display:flex; align-items:center; gap:10px; flex-grow:1">
                        <span style="font-size:13px; font-weight:600; white-space:nowrap">📂 Active .env File:</span>
                        <select v-model="selectedEnvPath" @change="switchEnvFile" class="input-flex" style="max-width:320px; font-size:13px; padding:4px 8px; height:32px">
                            <option value="">Workspace Root (.env)</option>
                            <option v-for="p in registeredEnvPaths" :key="p" :value="p">
                                {{ basename(p) }} ({{ p }})
                            </option>
                        </select>
                        <button class="btn-sm btn-danger" style="height:32px; padding:4px 10px; display:inline-flex; align-items:center; justify-content:center" v-if="selectedEnvPath" @click="unregisterEnvPath(selectedEnvPath)" title="Remove this file from managed environments list">
                            Unregister
                        </button>
                    </div>
                    <div style="display:flex; align-items:center; gap:8px">
                        <button class="btn-secondary btn-sm" style="height:32px; font-weight:600" @click="goBackToVolumes" v-if="customPath">
                            ← Back to Files
                        </button>
                    </div>
                </div>

                <div class="form-row" style="margin-bottom:14px; gap:10px">
                    <input type="text" v-model="newEnvKey" placeholder="KEY (e.g. OPENAI_API_KEY)" class="input-flex" style="max-width:260px" />
                    <input type="text" v-model="newEnvVal" placeholder="VALUE" class="input-flex" />
                    <button class="btn-primary" @click="saveEnvVar" :disabled="!newEnvKey">💾 Save to .env</button>
                </div>
                
                <div class="process-grid" style="margin-top:14px">
                    <div class="panel" style="margin-bottom:0">
                        <h3>Workspace .env variables</h3>
                        <div class="file-browser-scroll" style="max-height: 280px">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Key</th>
                                        <th>Value</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(val, key) in dotenvVars" :key="key">
                                        <td><code>{{ key }}</code></td>
                                        <td class="muted" style="max-width: 140px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap" :title="val">
                                            {{ val }}
                                        </td>
                                        <td>
                                            <div style="display:flex; gap:6px">
                                                <button class="btn-sm btn-primary" style="padding:1px 8px; font-size:11px" @click="newEnvKey = key; newEnvVal = val">edit</button>
                                                <button class="btn-sm btn-danger" style="padding:1px 8px; font-size:11px; margin-left:0" @click="deleteEnvVar(key)">delete</button>
                                            </div>
                                        </td>
                                    </tr>
                                    <tr v-if="!Object.keys(dotenvVars).length">
                                        <td colspan="3" class="muted hint" style="text-align:center; padding:12px">No workspace variables found in .env.</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                    
                    <div class="panel" style="margin-bottom:0">
                        <h3>Active Container runtime env</h3>
                        <div class="file-browser-scroll" style="max-height: 280px">
                            <table class="data-table">
                                <thead>
                                    <tr>
                                        <th>Key</th>
                                        <th>Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(val, key) in containerEnvVars" :key="key">
                                        <td><code>{{ key }}</code></td>
                                        <td class="muted" style="max-width: 180px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap" :title="val">
                                            {{ val }}
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <div class="hint" style="margin-top:12px">
                    ⚡ Saving a variable writes it directly to the <code>{{ customPath ? basename(customPath) : '.env' }}</code> file. To apply changes to the active container, please restart the sandbox.
                </div>
            </div>

            <div v-if="activeTab === 'volume'">
                <div class="form-group">
                    <label>Host Path</label>
                    <input type="text" v-model="vol.host_path" placeholder="e.g. ./data" class="input-flex" />
                </div>
                <div class="form-group">
                    <label>Container Path</label>
                    <input type="text" v-model="vol.container_path" placeholder="e.g. /app/data" class="input-flex" />
                </div>
                <button class="btn-primary" @click="submitVolume" :disabled="!vol.host_path || !vol.container_path">Add Volume</button>
            </div>
        </div>
    `,
};

// ---------------------------------------------------------------------------
// GitPanel component — branch status, diff viewer, stage/commit/push
// ---------------------------------------------------------------------------

const GitPanel = {
    setup() {
        const repoPath = ref('/workspace');
        const status = ref(null);
        const diff = ref('');
        const showDiff = ref(false);
        const commitMsg = ref('');
        const loading = ref(false);
        const opOutput = ref('');
        const opError = ref('');

        async function loadStatus() {
            loading.value = true;
            status.value = null;
            opError.value = '';
            try {
                const res = await api.get(`/api/git/status?path=${encodeURIComponent(repoPath.value)}`);
                if (res.ok) status.value = res;
                else opError.value = res.error || 'git status failed';
            } catch (e) {
                opError.value = e.message;
            } finally {
                loading.value = false;
            }
        }

        async function toggleDiff() {
            showDiff.value = !showDiff.value;
            if (!showDiff.value) return;
            try {
                const res = await api.post('/api/git/diff', { path: repoPath.value, staged: false });
                diff.value = res.diff || '(no diff)';
            } catch (e) { diff.value = `Error: ${e.message}`; }
        }

        async function stageAndCommit() {
            if (!commitMsg.value.trim()) { addToast('Enter a commit message', 'error'); return; }
            opOutput.value = ''; opError.value = '';
            try {
                const stageRes = await api.post('/api/git/stage', { path: repoPath.value });
                opOutput.value += stageRes.output || '';
                if (!stageRes.ok) { opError.value = 'git add failed'; return; }
                const commitRes = await api.post('/api/git/commit', { path: repoPath.value, message: commitMsg.value });
                opOutput.value += commitRes.output || '';
                if (commitRes.ok) { addToast('Committed.', 'success'); commitMsg.value = ''; loadStatus(); }
                else opError.value = 'git commit failed';
            } catch (e) { opError.value = e.message; }
        }

        async function push() {
            opOutput.value = ''; opError.value = '';
            try {
                const res = await api.post('/api/git/push', { path: repoPath.value });
                opOutput.value = res.output || '';
                if (res.ok) { addToast('Pushed.', 'success'); loadStatus(); }
                else opError.value = 'git push failed';
            } catch (e) { opError.value = e.message; }
        }

        onMounted(loadStatus);

        return { repoPath, status, diff, showDiff, commitMsg, loading, opOutput, opError, loadStatus, toggleDiff, stageAndCommit, push };
    },
    template: `
        <div class="panel">
            <h2>Git Manager</h2>
            <div class="form-row" style="margin-bottom:12px">
                <input type="text" v-model="repoPath" placeholder="/workspace" class="input-flex" />
                <button class="btn-secondary" @click="loadStatus" :disabled="loading">{{ loading ? 'Loading…' : '↻ Refresh' }}</button>
            </div>

            <div v-if="status">
                <div style="display:flex; align-items:center; gap:10px; flex-wrap:wrap; padding:10px; background:var(--surface); border:1px solid var(--border); border-radius:var(--radius); margin-bottom:12px">
                    <span style="font-size:13px">⎇ <strong>{{ status.branch || 'unknown' }}</strong></span>
                    <span class="badge-rw" style="font-size:10px">{{ status.staged.length }} staged</span>
                    <span class="badge-ro" style="font-size:10px">{{ status.unstaged.length }} unstaged</span>
                    <span class="muted" style="font-size:11px">{{ status.untracked.length }} untracked</span>
                </div>

                <div v-if="status.staged.length || status.unstaged.length" style="margin-bottom:12px">
                    <div v-if="status.staged.length" style="margin-bottom:6px">
                        <div class="hint" style="margin-bottom:3px">Staged:</div>
                        <div v-for="f in status.staged" :key="f.file" style="font-family:var(--font-mono); font-size:11px; color:var(--ok)">+ {{ f.file }}</div>
                    </div>
                    <div v-if="status.unstaged.length">
                        <div class="hint" style="margin-bottom:3px">Unstaged:</div>
                        <div v-for="f in status.unstaged" :key="f.file" style="font-family:var(--font-mono); font-size:11px; color:var(--err)">~ {{ f.file }}</div>
                    </div>
                </div>

                <div style="margin-bottom:12px">
                    <button class="btn-sm btn-secondary" @click="toggleDiff">{{ showDiff ? '▲ Hide diff' : '▼ Show diff' }}</button>
                    <div v-if="showDiff" class="terminal-output" style="max-height:200px; margin-top:8px">
                        <pre style="font-size:10px; white-space:pre-wrap; word-break:break-all">{{ diff }}</pre>
                    </div>
                </div>

                <div style="padding:12px; background:var(--surface); border:1px solid var(--border); border-radius:var(--radius)">
                    <div class="form-row" style="margin-bottom:8px">
                        <input type="text" v-model="commitMsg" placeholder="Commit message…" class="input-flex" @keyup.enter="stageAndCommit" />
                    </div>
                    <div class="form-row" style="gap:8px">
                        <button class="btn-primary" @click="stageAndCommit" :disabled="!commitMsg.trim()">⚡ Stage All & Commit</button>
                        <button class="btn-secondary" @click="push">↑ Push</button>
                    </div>
                </div>
            </div>

            <div v-if="opOutput" class="terminal-output" style="margin-top:10px; max-height:160px">
                <pre style="font-size:11px">{{ opOutput }}</pre>
            </div>
            <div v-if="opError" class="error-msg" style="margin-top:8px">{{ opError }}</div>
        </div>
    `,
};

// ---------------------------------------------------------------------------
// Router
// ---------------------------------------------------------------------------

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        { path: '/',           redirect: '/terminal' },
        { path: '/dashboard',  component: DashboardPanel },
        { path: '/terminal',   component: TerminalPanel },
        { path: '/pty',        component: PtyTerminalPanel },
        { path: '/volumes',    component: VolumePanel },
        { path: '/processes',  component: ProcessesPanel },
        { path: '/editor',     component: EditorPanel },
        { path: '/db-viewer',  component: DbViewerPanel },
        { path: '/config',     component: ConfigPanel },
        { path: '/git',        component: GitPanel },
    ],
});

// ---------------------------------------------------------------------------
// Root App
// ---------------------------------------------------------------------------

createApp({
    components: { StatusBar },
    setup() {
        const status = ref(null);
        provide('status', status);

        const navItems = [
            { path: '/dashboard', label: '⬡ Dashboard' },
            { path: '/terminal',  label: '⌨ Terminal' },
            { path: '/pty',       label: '> PTY Shell' },
            { path: '/volumes',   label: '📦 Volumes' },
            { path: '/processes', label: '📊 Processes' },
            { path: '/git',       label: '⎇ Git' },
            { path: '/config',    label: '⚙ Config' },
        ];

        const theme = ref('dark');

        function toggleTheme() {
            theme.value = theme.value === 'dark' ? 'light' : 'dark';
            localStorage.setItem('aios_theme', theme.value);
            applyTheme();
        }

        function applyTheme() {
            if (theme.value === 'light') {
                document.body.classList.add('theme-light');
            } else {
                document.body.classList.remove('theme-light');
            }
        }

        async function fetchStatus() {
            try {
                status.value = await api.get('/api/status');
            } catch (_) {
                status.value = null;
            }
        }

        onMounted(() => {
            fetchStatus();
            setInterval(fetchStatus, 15000);
            theme.value = localStorage.getItem('aios_theme') || 'dark';
            applyTheme();
        });

        return { navItems, theme, toggleTheme, toasts };
    },
    template: `
        <div id="app-root">
            <StatusBar />
            <div class="layout">
                <aside class="sidebar">
                    <nav>
                        <router-link
                            v-for="item in navItems"
                            :key="item.path"
                            :to="item.path"
                            custom
                            v-slot="{ navigate, isActive }"
                        >
                            <button
                                @click="navigate"
                                class="nav-item"
                                :class="{ active: isActive }"
                            >{{ item.label }}</button>
                        </router-link>
                    </nav>
                    <div class="theme-toggle-container">
                        <button class="btn-theme-toggle" @click="toggleTheme">
                            {{ theme === 'dark' ? '☀️ Light' : '🌙 Dark' }}
                        </button>
                    </div>
                </aside>
                <main class="content">
                    <router-view />
                </main>
            </div>
            
            <!-- Global Toasts -->
            <div class="toast-container">
                <div v-for="t in toasts" :key="t.id" :class="['toast', t.type]">
                    <span>{{ t.message }}</span>
                    <button class="toast-close" @click="toasts = toasts.filter(x => x.id !== t.id)">✕</button>
                </div>
            </div>
        </div>
    `,
}).use(router).mount('#app');
