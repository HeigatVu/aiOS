import streamlit as st
import time
import os
import docker_bridge
import config_editors

# Set up page configurations
st.set_page_config(
    page_title="AI Workspace Sidecar Controller",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling using CSS injection
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
    
    /* Global Typography */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Outfit', sans-serif;
        background-color: #0d1117;
        color: #f3f4f6;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }
    
    /* Headers & Text */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem !important;
    }
    
    /* Inline Code Blocks inside headers */
    code {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #1f2937 !important;
        color: #34d399 !important; /* Radiant green text */
        -webkit-text-fill-color: #34d399 !important; /* Forces visible text inside headers */
        border: 1px solid #30363d !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }
    
    /* Standard Code Blocks */
    .stCodeBlock {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
    }
    
    /* Custom buttons with vibrant green gradient */
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        color: white !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 24px !important;
        box-shadow: 0 4px 6px -1px rgba(16, 185, 129, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #34d399 0%, #10b981 100%) !important;
        box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.4) !important;
        transform: translateY(-2px) !important;
        color: white !important;
    }
    
    .stButton>button:active {
        transform: translateY(0px) !important;
    }
    
    /* Terminal Console */
    .terminal-console {
        background-color: #0b0f19 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13px !important;
        padding: 14px !important;
        color: #38bdf8 !important; /* Sky blue */
        overflow-y: auto !important;
        max-height: 250px !important;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.8) !important;
        white-space: pre-wrap !important;
    }
    
    /* Connection indicators */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .status-badge.connected {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .status-badge.simulated {
        background-color: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    
    .status-badge.disconnected {
        background-color: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
        display: inline-block;
    }
    
    .pulse-dot.green {
        background-color: #10b981;
        box-shadow: 0 0 8px #10b981;
    }
    
    .pulse-dot.yellow {
        background-color: #f59e0b;
        box-shadow: 0 0 8px #f59e0b;
    }
    
    .pulse-dot.red {
        background-color: #ef4444;
        box-shadow: 0 0 8px #ef4444;
    }

</style>
""", unsafe_allow_html=True)

# Fetch Sandbox Container and Docker Status
status = docker_bridge.get_sandbox_status()
docker_conn = status["docker_connected"]
sandbox_run = status["sandbox_running"]
is_mock = status.get("is_mock", False)

# Sidebar dashboard panel
with st.sidebar:
    st.markdown("### 🛠️ Sidecar Status")
    
    # 1. Socket Status
    if docker_conn:
        st.markdown(
            '<div class="status-badge connected"><span class="pulse-dot green"></span>Docker Socket: Active</div>',
            unsafe_allow_html=True
        )
    elif is_mock:
        st.markdown(
            '<div class="status-badge simulated"><span class="pulse-dot yellow"></span>Docker: Simulated Mode</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-badge disconnected"><span class="pulse-dot red"></span>Docker: Disconnected</div>',
            unsafe_allow_html=True
        )
        
    st.markdown("---")
    
    # 2. Target Container Sandbox status
    st.markdown("### 📦 Target Sandbox")
    st.markdown(f"**Container Name:** `ai_tui_sandbox`")
    
    if sandbox_run:
        status_label = "RUNNING"
        badge_style = "connected"
        dot_style = "green"
    else:
        status_label = "STOPPED / NOT FOUND"
        badge_style = "disconnected"
        dot_style = "red"
        
    st.markdown(
        f'<div class="status-badge {badge_style}"><span class="pulse-dot {dot_style}"></span>State: {status_label}</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.markdown("### 💾 Workspace Info")
    st.markdown(f"**Root Directory:**")
    st.code(config_editors.WORKSPACE_DIR)

# Main content area
st.title("🤖 AI Workspace Sidecar")
st.markdown("##### Control Panel & Caching Manager for `ai_tui_sandbox`")

# Tabs for separate features
tab_install, tab_mount, tab_notes = st.tabs([
    "📦 Install Packages", 
    "🔌 Mount Shared Folders", 
    "✍️ Save Notes & Blueprint"
])

# Tab 1: Installer UI
with tab_install:
    with st.container(border=True):
        st.subheader("Install Tool / Package")
        st.write("Specify package name and ecosystem to run inside the sandbox. Changes are automatically baked into infrastructure definitions.")
        
        ecosystem = st.selectbox(
            "Select Installation Ecosystem",
            ("uv", "conda", "dnf", "npm"),
            help="uv = Python libraries, conda = ML packages, dnf = system tools, npm = global Node/JS packages"
        )
        package_name = st.text_input(
            "Package Name",
            placeholder="e.g. htop, librosa, requests, @agentmemory/agentmemory",
            key="install_pkg"
        )
        
        # Dynamic sudo checkbox: default to True for system/npm, False for user managers
        use_sudo = st.checkbox(
            "Use sudo (Root privileges)", 
            value=ecosystem in ("dnf", "npm"),
            key=f"use_sudo_{ecosystem}",
            help="Toggle on if this package requires root privileges to install"
        )
        
        sudo_prefix = "sudo " if use_sudo else ""
        
        # Determine the fallback instruction and the live command to run inside sandbox
        if ecosystem == "uv":
            run_cmd = f"{sudo_prefix}uv pip install {package_name}"
            fallback_cmd = f"docker exec -it ai_tui_sandbox {sudo_prefix}uv pip install {package_name}"
        elif ecosystem == "conda":
            run_cmd = f"{sudo_prefix}conda install -y -c conda-forge {package_name}"
            fallback_cmd = f"docker exec -it ai_tui_sandbox {sudo_prefix}conda install -y -c conda-forge {package_name}"
        elif ecosystem == "dnf":
            run_cmd = f"{sudo_prefix}dnf install -y {package_name}"
            fallback_cmd = f"docker exec -it ai_tui_sandbox {sudo_prefix}dnf install -y {package_name}"
        elif ecosystem == "npm":
            run_cmd = f"{sudo_prefix}npm install -g {package_name}"
            fallback_cmd = f"docker exec -it ai_tui_sandbox {sudo_prefix}npm install -g {package_name}"
            
        st.markdown("**Manual Fallback Guide:**")
        st.caption("If background installation fails, copy and run this in your host terminal:")
        st.code(fallback_cmd, language="bash")
        
        install_button = st.button("🚀 Trigger Installation", disabled=not package_name.strip())
        
        st.markdown("**Installation Console Output:**")
        console_placeholder = st.empty()
        # Initial empty state
        console_placeholder.markdown(
            '<div class="terminal-console">Console idle. Ready for operations...</div>',
            unsafe_allow_html=True
        )
        
    # Handle installation submit trigger
    if install_button and package_name.strip():
        # Clear console and prepare streaming logs
        log_content = f"Initiating installation of '{package_name}' via {ecosystem}...\n"
        console_placeholder.markdown(
            f'<div class="terminal-console">{log_content}</div>',
            unsafe_allow_html=True
        )
        
        # 1. Run live update in sandbox using the bridge
        try:
            stream_gen = docker_bridge.execute_in_sandbox(run_cmd)
            for chunk in stream_gen:
                log_content += chunk
                console_placeholder.markdown(
                    f'<div class="terminal-console">{log_content}</div>',
                    unsafe_allow_html=True
                )
        except Exception as ex:
            log_content += f"\nSandbox execution failed: {str(ex)}\n"
            console_placeholder.markdown(
                f'<div class="terminal-console">{log_content}</div>',
                unsafe_allow_html=True
            )
            st.error(f"Installation failed: {ex}")
            st.stop()
            
        # 2. Append changes permanently to infrastructure-as-code files
        log_content += "\nSaving configurations permanently to Infrastructure definitions...\n"
        console_placeholder.markdown(
            f'<div class="terminal-console">{log_content}</div>',
            unsafe_allow_html=True
        )
        
        success = False
        try:
            if ecosystem in ("dnf", "npm"):
                config_editors.append_to_dockerfile(package_name, ecosystem, use_sudo=use_sudo)
                prefix = "sudo " if use_sudo else ""
                if ecosystem == "dnf":
                    log_content += f"✔️ Appended 'RUN {prefix}dnf install -y {package_name}' to root Dockerfile\n"
                else:
                    log_content += f"✔️ Appended 'RUN {prefix}npm install -g {package_name}' to root Dockerfile\n"
            elif ecosystem in ("uv", "conda"):
                config_editors.append_to_environment(package_name)
                log_content += f"✔️ Appended dependency '{package_name}' to environment.yml\n"
            
            # Save transaction notes to README.md
            note_str = f"Installed package '{package_name}' via {ecosystem} using the Sidecar UI."
            config_editors.append_to_readme(note_str)
            log_content += "✔️ Transaction successfully written to README.md under # Notes\n"
            success = True
        except Exception as ex:
            log_content += f"❌ Error saving configurations: {str(ex)}\n"
            st.error(f"Config saving failed: {ex}")
            
        log_content += "\nFinished operation successfully!\n"
        console_placeholder.markdown(
            f'<div class="terminal-console">{log_content}</div>',
            unsafe_allow_html=True
        )
        if success:
            st.success(f"Successfully installed '{package_name}' and updated workspace files!")

# Tab 2: Volume Mounter UI
with tab_mount:
    with st.container(border=True):
        st.subheader("Mount Host Shared Folder")
        st.write("Surgically map folders from the host laptop directly into the Sandbox environment.")
        
        host_path = st.text_input(
            "Host Path (Absolute or relative to workspace)",
            placeholder="e.g. ./datasets/audio-files or /home/user/downloads"
        )
        container_path = st.text_input(
            "Container Path (Destination path inside Sandbox)",
            placeholder="e.g. /data/audio-files or /workspace/my-downloads"
        )
        
        mount_button = st.button("🔌 Map Volume & Restart warning", disabled=not (host_path.strip() and container_path.strip()))
        
        st.warning("⚠️ **Volume Mapping Warning:** Modifying ports or volumes in `docker-compose.yml` requires reloading the service container layers. You must run `docker compose down && docker compose up -d` on your host machine to apply volume mounts.")
        st.markdown("**Example Output Map:**")
        if host_path and container_path:
            st.code(f"- {host_path}:{container_path}:rw, z", language="yaml")
            
    if mount_button and host_path.strip() and container_path.strip():
        try:
            config_editors.add_volume_to_compose(host_path.strip(), container_path.strip())
            
            # Save note to README
            note_str = f"Mounted folder mapping '{host_path.strip()}:{container_path.strip()}' in docker-compose.yml."
            config_editors.append_to_readme(note_str)
            
            st.success("Successfully injected volume configuration to docker-compose.yml!")
            st.info("Remember to run `docker compose down && docker compose up -d` on your Fedora Host terminal to activate this mount!")
        except Exception as ex:
            st.error(f"Failed to mount volume: {ex}")

# Tab 3: Note Saver UI
with tab_notes:
    with st.container(border=True):
        st.subheader("Workspace Notebook & Quick Notes")
        st.write("Write quick notes, timestamps, or blueprint instructions to persist memory directly under the designated `# Notes` section in `README.md`.")
        
        note_text = st.text_area(
            "Enter note content",
            placeholder="e.g. Remember to run python test_signal.py with CUDA enabled next time.",
            height=150
        )
        
        save_button = st.button("✍️ Commit Note to README.md", disabled=not note_text.strip())
    
    if save_button and note_text.strip():
        try:
            config_editors.append_to_readme(note_text.strip())
            st.success("Successfully committed note to README.md under the # Notes section!")
            st.code(f"# Notes\n* Commit successful at {time.strftime('%Y-%m-%d %H:%M:%S')}", language="markdown")
        except Exception as ex:
            st.error(f"Failed to save note: {ex}")
