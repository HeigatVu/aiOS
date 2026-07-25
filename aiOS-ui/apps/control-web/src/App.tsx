import { FormEvent, useEffect, useState } from 'react';

type View = 'overview' | 'agents';

type Agent = {
  id: string;
  display_name: string;
  source: string;
  package: string;
};

type Extension = {
  source: 'npm' | 'pypi';
  name: string;
  version: string;
};

const externalNavigation = [
  ['Hermes Chat', '/hermes-chat/'],
  ['Hermes Dashboard', '/hermes-dashboard/'],
  ['Agent Memory', '/agentmemory/'],
  ['File Explorer', '/legacy#files'],
  ['Ideas & Notes', '/legacy#notes'],
  ['Shell Terminal', '/terminals'],
  ['System Update', '/legacy#update']
] as const;

async function requestJson(path: string, init?: RequestInit) {
  const response = await fetch(path, init);
  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(body.detail ?? 'Request failed');
  }
  return response.json();
}

export function App() {
  const [view, setView] = useState<View>('overview');
  const [agents, setAgents] = useState<Agent[]>([]);
  const [extensions, setExtensions] = useState<Extension[]>([]);
  const [message, setMessage] = useState('');
  const [source, setSource] = useState<Extension['source']>('npm');
  const [name, setName] = useState('');
  const [version, setVersion] = useState('');

  const refreshManagement = async () => {
    try {
      const [agentData, extensionData] = await Promise.all([
        requestJson('/api/agents'),
        requestJson('/api/extensions')
      ]);
      setAgents(agentData.agents);
      setExtensions(extensionData.extensions);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Unable to load agent information');
    }
  };

  useEffect(() => {
    void refreshManagement();
  }, []);

  const createAgentJob = async (action: 'check' | 'update', selected: string[]) => {
    try {
      const data = await requestJson(action === 'check' ? '/api/agents/check' : '/api/agent-jobs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: action === 'check' ? undefined : JSON.stringify({ action, agents: selected })
      });
      setMessage(`Job ${data.job.id.slice(0, 8)} is queued.`);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Unable to queue job');
    }
  };

  const installExtension = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      const data = await requestJson('/api/extensions', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source, name, version })
      });
      setExtensions((current) => [...current.filter((item) => item.name !== data.extension.name || item.source !== data.extension.source), data.extension]);
      setMessage(`Install job ${data.job.id.slice(0, 8)} is queued.`);
      setName('');
      setVersion('');
    } catch (error) {
      setMessage(error instanceof Error ? error.message : 'Unable to queue extension install');
    }
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="/" aria-label="aiOS Control Center">ai<span>OS</span></a>
        <nav aria-label="Primary navigation">
          <button className={view === 'overview' ? 'nav-item active' : 'nav-item'} onClick={() => setView('overview')}>Control Center</button>
          <button className={view === 'agents' ? 'nav-item active' : 'nav-item'} onClick={() => setView('agents')}>Agents &amp; Tools</button>
          {externalNavigation.map(([label, href]) => <a className="nav-item" href={href} key={label}>{label}</a>)}
        </nav>
        <a className="legacy-link" href="/legacy">Open legacy control UI</a>
      </aside>
      <main className="main-content">
        <header className="topbar">
          <p>aiOS / {view === 'overview' ? 'Control Center' : 'Agents & Tools'}</p>
          <span className="local-badge">Local control</span>
        </header>
        {view === 'overview' ? (
          <section className="page">
            <div className="page-heading">
              <div>
                <h1>Control Center</h1>
                <p>Local AI workspace services, storage, and installed tools.</p>
              </div>
              <button className="primary" onClick={() => setView('agents')}>Manage agents</button>
            </div>
            <div className="metrics" aria-label="System summary">
              <article><span>Workspace</span><strong>Mounted</strong><small>Read/write agent workspace</small></article>
              <article><span>Outputs</span><strong>Mounted</strong><small>Generated files persist on host</small></article>
              <article><span>Private notes</span><strong>Isolated</strong><small>Control service only</small></article>
            </div>
            <section className="service-grid" aria-label="Subsystems">
              <a href="/hermes-chat/"><h2>Hermes Workspace</h2><p>Chat with and orchestrate agent work.</p></a>
              <a href="/agentmemory/"><h2>Agent Memory</h2><p>Inspect persistent memory and relationships.</p></a>
              <a href="/files"><h2>File Explorer</h2><p>Browse workspace, outputs, and governed data.</p></a>
              <a href="/terminals"><h2>Shell Terminal</h2><p>Open a direct terminal in the agent environment.</p></a>
            </section>
          </section>
        ) : (
          <section className="page">
            <div className="page-heading">
              <div>
                <h1>Agents &amp; Tools</h1>
                <p>Check and update the supported agent catalog, then persist additional pinned tools.</p>
              </div>
              <button className="primary" onClick={() => void createAgentJob('check', [])}>Check versions</button>
            </div>
            {message && <p className="notice" role="status">{message}</p>}
            <section className="agent-list" aria-label="Managed agents">
              {agents.map((agent) => (
                <article className="agent-row" key={agent.id}>
                  <div><h2>{agent.display_name}</h2><p>{agent.package} via {agent.source}</p></div>
                  <button onClick={() => void createAgentJob('update', [agent.id])}>Update</button>
                </article>
              ))}
              {!agents.length && <p className="empty-state">Loading managed agents...</p>}
            </section>
            <section className="extension-panel" aria-labelledby="extensions-heading">
              <div>
                <h2 id="extensions-heading">Managed Tools</h2>
                <p>Only exact NPM and PyPI/uv versions are accepted. They are stored for the next installation.</p>
              </div>
              <form onSubmit={(event) => void installExtension(event)}>
                <select aria-label="Package source" value={source} onChange={(event) => setSource(event.target.value as Extension['source'])}>
                  <option value="npm">NPM</option>
                  <option value="pypi">PyPI / uv</option>
                </select>
                <input aria-label="Package name" value={name} onChange={(event) => setName(event.target.value)} placeholder="Package name" required />
                <input aria-label="Exact version" value={version} onChange={(event) => setVersion(event.target.value)} placeholder="Exact version" required />
                <button className="primary" type="submit">Queue install</button>
              </form>
              <ul className="extension-list">
                {extensions.map((extension) => <li key={`${extension.source}:${extension.name}`}>{extension.name}<span>{extension.source} {extension.version}</span></li>)}
              </ul>
            </section>
          </section>
        )}
      </main>
    </div>
  );
}
