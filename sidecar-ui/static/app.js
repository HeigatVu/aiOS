'use strict';

const { createApp, ref, reactive, onMounted, nextTick } = Vue;

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
    get: (path) => apiFetch(path),
    post: (path, body) => apiFetch(path, { method: 'POST', body: JSON.stringify(body) }),
};

// ---------------------------------------------------------------------------
// WebSocket exec helper
// ---------------------------------------------------------------------------

function streamExec(cmd, { onChunk, onDone, onError }) {
    const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
    const ws = new WebSocket(`${proto}//${location.host}/ws/exec`);
    ws.onopen = () => ws.send(cmd);
    ws.onmessage = (e) => onChunk(e.data);
    ws.onerror = () => onError?.('WebSocket error');
    ws.onclose = () => onDone?.();
    return () => ws.close();
}

// ---------------------------------------------------------------------------
// Utility
// ---------------------------------------------------------------------------

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

// ---------------------------------------------------------------------------
// StatusBar component
// ---------------------------------------------------------------------------

const StatusBar = {
    props: ['status'],
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
// DashboardPanel component
// ---------------------------------------------------------------------------

const DashboardPanel = {
    props: ['status'],
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
                </div>
                <div v-else class="muted">Loading status...</div>
                <div class="hint">
                    To restart the sandbox, run <code>make restart</code> in the project root.<br>
                    To fix configuration issues, edit <code>config-file/prompt-to-fix.md</code>.
                </div>
            </div>
        </div>
    `,
};

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
                                package: pkg,
                                ecosystem: ecosystem.value,
                                use_sudo: false,
                            });
                        } catch (e) { /* best-effort */ }
                    }
                    if (saveNote.value && pkg) {
                        try {
                            await api.post('/api/config/readme', {
                                note: `Installed ${pkg} via ${ecosystem.value}`,
                            });
                        } catch (e) { /* best-effort */ }
                    }
                },
                onError: (msg) => {
                    output.value += `\nError: ${msg}\n`;
                    running.value = false;
                },
            });
        }

        function clearOutput() {
            output.value = '';
        }

        return { ecosystem, pkgName, rawCmd, output, running, bakeIntoDockerfile, saveNote, error, run, clearOutput };
    },
    template: `
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
                <input type="text" v-model="rawCmd" placeholder="Or type a raw command…" class="input-flex" @keyup.enter="run" />
                <button class="btn-secondary" @click="run" :disabled="running">Run</button>
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
    `,
};

// ---------------------------------------------------------------------------
// VolumePanel component
// ---------------------------------------------------------------------------

const VolumePanel = {
    setup() {
        const volumes = ref([]);
        const browseIdx = ref(null);
        const files = ref([]);
        const filesPath = ref('');
        const loadingFiles = ref(false);
        const chmodTarget = ref(null);
        const chmodMode = ref('');
        const error = ref('');

        async function loadVolumes() {
            try {
                volumes.value = await api.get('/api/volumes');
            } catch (e) {
                error.value = `Failed to load volumes: ${e.message}`;
            }
        }

        async function toggleMode(vol) {
            const newMode = vol.mode === 'rw' ? 'ro' : 'rw';
            try {
                await api.post(`/api/volumes/${vol.index}/mode`, { mode: newMode });
                await loadVolumes();
                // Refresh file list if browsing this volume
                if (browseIdx.value === vol.index) {
                    await browse(vol);
                }
            } catch (e) {
                error.value = `Failed to update mode: ${e.message}`;
            }
        }

        async function browse(vol) {
            if (browseIdx.value === vol.index) {
                browseIdx.value = null;
                files.value = [];
                return;
            }
            browseIdx.value = vol.index;
            filesPath.value = vol.container_path;
            loadingFiles.value = true;
            files.value = [];
            chmodTarget.value = null;
            try {
                files.value = await api.get(`/api/volumes/${vol.index}/files`);
            } catch (e) {
                error.value = `Failed to list files: ${e.message}`;
            } finally {
                loadingFiles.value = false;
            }
        }

        function startChmod(file) {
            chmodTarget.value = file;
            chmodMode.value = file.permissions;
        }

        async function applyChmodReal() {
            if (!chmodTarget.value) return;
            const savedIdx = browseIdx.value;
            try {
                await api.post('/api/volumes/chmod', {
                    path: chmodTarget.value.name,
                    mode: chmodMode.value,
                });
                chmodTarget.value = null;
                // Refresh file listing
                if (savedIdx !== null) {
                    const vol = volumes.value.find(v => v.index === savedIdx);
                    if (vol) {
                        loadingFiles.value = true;
                        try {
                            files.value = await api.get(`/api/volumes/${savedIdx}/files`);
                        } finally {
                            loadingFiles.value = false;
                        }
                    }
                }
            } catch (e) {
                error.value = `chmod failed: ${e.message}`;
            }
        }

        onMounted(loadVolumes);

        return {
            volumes, browseIdx, files, filesPath, loadingFiles,
            chmodTarget, chmodMode, error,
            toggleMode, browse, startChmod, applyChmodReal,
            basename, octalToSymbolic,
        };
    },
    template: `
        <div class="panel">
            <h2>Volumes</h2>
            <div v-if="error" class="error-msg">{{ error }}</div>
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
                    <tr v-for="vol in volumes" :key="vol.index">
                        <td class="muted">{{ vol.index }}</td>
                        <td class="path">{{ vol.host_path }}</td>
                        <td class="path">{{ vol.container_path }}</td>
                        <td>
                            <span :class="vol.mode === 'rw' ? 'badge-rw' : 'badge-ro'">{{ vol.mode }}</span>
                        </td>
                        <td class="muted">{{ vol.selinux || '—' }}</td>
                        <td>
                            <div class="actions-cell">
                                <button class="btn-sm" @click="browse(vol)">
                                    {{ browseIdx === vol.index ? 'Close' : 'Browse' }}
                                </button>
                                <button class="btn-sm" @click="toggleMode(vol)">
                                    → {{ vol.mode === 'rw' ? 'ro' : 'rw' }}
                                </button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <div v-else class="muted hint">No volumes found in docker-compose.yml.</div>

            <!-- File browser -->
            <div v-if="browseIdx !== null" class="file-browser">
                <h3>Files in <span class="path">{{ filesPath }}</span></h3>
                <div v-if="loadingFiles" class="muted">Loading…</div>
                <table class="data-table" v-else-if="files.length">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Permissions</th>
                            <th>Symbolic</th>
                            <th>Owner</th>
                            <th>Size</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="file in files" :key="file.name">
                            <td>
                                <span class="file-icon">{{ file.is_dir ? '📁' : '📄' }}</span>
                                {{ basename(file.name) }}
                            </td>
                            <td><code>{{ file.permissions }}</code></td>
                            <td><code class="muted">{{ octalToSymbolic(file.permissions) }}</code></td>
                            <td class="muted">{{ file.owner }}</td>
                            <td class="muted">{{ file.size }}</td>
                            <td>
                                <button class="btn-sm" @click="startChmod(file)">chmod</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <div v-else class="muted hint">No files found or directory is empty.</div>

                <!-- chmod inline form -->
                <div v-if="chmodTarget" class="chmod-form">
                    <span class="chmod-path">{{ basename(chmodTarget.name) }}</span>
                    <input type="text" v-model="chmodMode" placeholder="755" style="width:80px; font-family: var(--font-mono)" />
                    <button class="btn-primary btn-sm" @click="applyChmodReal">Apply</button>
                    <button class="btn-secondary btn-sm" @click="chmodTarget = null">Cancel</button>
                </div>
            </div>

            <div class="hint">
                Mode changes write to docker-compose.yml. Restart container to apply the new mode.
            </div>
        </div>
    `,
};

// ---------------------------------------------------------------------------
// ConfigPanel component
// ---------------------------------------------------------------------------

const ConfigPanel = {
    setup() {
        const activeTab = ref('dockerfile');
        const tabs = [
            { id: 'dockerfile', label: 'Dockerfile' },
            { id: 'readme', label: 'README' },
            { id: 'environment', label: 'Environment' },
            { id: 'volume', label: 'Volume' },
        ];

        // dockerfile form
        const df = reactive({ package: '', ecosystem: 'uv', use_sudo: false });
        // readme form
        const rm = reactive({ note: '' });
        // environment form
        const env = reactive({ package: '' });
        // volume form
        const vol = reactive({ host_path: '', container_path: '' });

        const success = ref('');
        const error = ref('');

        function clearMessages() { success.value = ''; error.value = ''; }

        async function submitDockerfile() {
            clearMessages();
            try {
                await api.post('/api/config/dockerfile', {
                    package: df.package,
                    ecosystem: df.ecosystem,
                    use_sudo: df.use_sudo,
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

        return {
            activeTab, tabs,
            df, rm, env, vol,
            success, error,
            submitDockerfile, submitReadme, submitEnvironment, submitVolume,
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
                    @click="activeTab = tab.id"
                >{{ tab.label }}</button>
            </div>

            <div v-if="success" class="success-msg">{{ success }}</div>
            <div v-if="error" class="error-msg">{{ error }}</div>

            <!-- Dockerfile tab -->
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

            <!-- README tab -->
            <div v-if="activeTab === 'readme'">
                <div class="form-group">
                    <label>Note</label>
                    <textarea v-model="rm.note" rows="4" placeholder="Note to append to README…"></textarea>
                </div>
                <button class="btn-primary" @click="submitReadme" :disabled="!rm.note">Append to README</button>
            </div>

            <!-- Environment tab -->
            <div v-if="activeTab === 'environment'">
                <div class="form-group">
                    <label>Package</label>
                    <input type="text" v-model="env.package" placeholder="e.g. numpy" class="input-flex" />
                </div>
                <button class="btn-primary" @click="submitEnvironment" :disabled="!env.package">Add to environment.yml</button>
            </div>

            <!-- Volume tab -->
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
// Root App
// ---------------------------------------------------------------------------

createApp({
    components: { StatusBar, DashboardPanel, TerminalPanel, VolumePanel, ConfigPanel },
    setup() {
        const activeTab = ref('terminal');
        const status = ref(null);
        const navItems = [
            { id: 'dashboard', label: '⬡ Dashboard' },
            { id: 'terminal', label: '⌨ Terminal' },
            { id: 'volumes', label: '📦 Volumes' },
            { id: 'config', label: '⚙ Config' },
        ];

        async function fetchStatus() {
            try {
                status.value = await api.get('/api/status');
            } catch (e) {
                status.value = null;
            }
        }

        onMounted(() => {
            fetchStatus();
            setInterval(fetchStatus, 15000);
        });

        return { activeTab, status, navItems };
    },
    template: `
        <div id="app-root">
            <StatusBar :status="status" />
            <div class="layout">
                <aside class="sidebar">
                    <nav>
                        <button
                            v-for="item in navItems"
                            :key="item.id"
                            class="nav-item"
                            :class="{ active: activeTab === item.id }"
                            @click="activeTab = item.id"
                        >{{ item.label }}</button>
                    </nav>
                </aside>
                <main class="content">
                    <DashboardPanel v-if="activeTab === 'dashboard'" :status="status" />
                    <TerminalPanel v-if="activeTab === 'terminal'" />
                    <VolumePanel v-if="activeTab === 'volumes'" />
                    <ConfigPanel v-if="activeTab === 'config'" />
                </main>
            </div>
        </div>
    `,
}).mount('#app');
