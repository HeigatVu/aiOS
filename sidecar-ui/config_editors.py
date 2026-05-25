import os
import yaml
import datetime

# Determine root workspace directory dynamically.
# If /workspace exists (mounted in docker), use that.
# Otherwise, fall back to the parent directory of this file's directory.
if os.path.exists("/workspace"):
    WORKSPACE_DIR = "/workspace"
else:
    WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOCKERFILE_PATH = os.path.join(WORKSPACE_DIR, "Dockerfile")
DOCKER_COMPOSE_PATH = os.path.join(WORKSPACE_DIR, "docker-compose.yml")
ENVIRONMENT_PATH = os.path.join(WORKSPACE_DIR, "environment.yml")
README_PATH = os.path.join(WORKSPACE_DIR, "README.md")

def append_to_dockerfile(package: str, ecosystem: str):
    """
    Appends a RUN instruction for dnf install under the auto-installs marker in Dockerfile.
    """
    if not os.path.exists(DOCKERFILE_PATH):
        raise FileNotFoundError(f"Dockerfile not found at {DOCKERFILE_PATH}")
        
    with open(DOCKERFILE_PATH, 'r') as f:
        content = f.read()
        
    marker = "# --- AI SIDECAR AUTO-INSTALLS ---"
    if marker not in content:
        raise ValueError(f"Marker '{marker}' not found in Dockerfile")
        
    # Standard instruction for installing
    if ecosystem.lower() == 'dnf':
        instruction = f"RUN dnf install -y {package} && dnf clean all\n"
    elif ecosystem.lower() == 'uv':
        instruction = f"RUN uv pip install {package}\n"
    elif ecosystem.lower() == 'conda':
        instruction = f"RUN conda install -y {package} && conda clean -afy\n"
    else:
        instruction = f"RUN {ecosystem} install {package}\n"
        
    # Check if already present to avoid duplicates
    if instruction.strip() in content:
        return True # Already appended
        
    # Insert right below the marker
    parts = content.split(marker, 1)
    new_content = parts[0] + marker + "\n" + instruction + parts[1]
    
    with open(DOCKERFILE_PATH, 'w') as f:
        f.write(new_content)
    return True

def append_to_readme(note: str):
    """
    Appends a markdown note under the # Notes section in README.md.
    """
    if not os.path.exists(README_PATH):
        raise FileNotFoundError(f"README.md not found at {README_PATH}")
        
    with open(README_PATH, 'r') as f:
        content = f.read()
        
    marker = "# Notes"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bullet = f"\n* **[{timestamp}]** {note}\n"
    
    if marker not in content:
        # Create section at the end of the file
        new_content = content.rstrip() + f"\n\n{marker}\n" + bullet
    else:
        # Insert after the marker
        parts = content.split(marker, 1)
        new_content = parts[0] + marker + "\n" + bullet + parts[1]
        
    with open(README_PATH, 'w') as f:
        f.write(new_content)
    return True

def append_to_environment(package: str):
    """
    Parses environment.yml and appends the dependency safely.
    """
    if not os.path.exists(ENVIRONMENT_PATH):
        raise FileNotFoundError(f"environment.yml not found at {ENVIRONMENT_PATH}")
        
    with open(ENVIRONMENT_PATH, 'r') as f:
        data = yaml.safe_load(f)
        
    if not data or 'dependencies' not in data:
        raise ValueError("Invalid environment.yml structure: missing dependencies key")
        
    # Check if package is already in dependencies
    if package in data['dependencies']:
        return True
        
    # Append the new dependency
    data['dependencies'].append(package)
    
    with open(ENVIRONMENT_PATH, 'w') as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
    return True

def add_volume_to_compose(host_path: str, container_path: str):
    """
    Surgically injects volume mapping into services.sandbox.volumes in docker-compose.yml,
    preserving comments and indentation.
    """
    if not os.path.exists(DOCKER_COMPOSE_PATH):
        raise FileNotFoundError(f"docker-compose.yml not found at {DOCKER_COMPOSE_PATH}")
        
    with open(DOCKER_COMPOSE_PATH, 'r') as f:
        lines = f.readlines()
        
    sandbox_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('sandbox:'):
            sandbox_idx = i
            break
            
    if sandbox_idx == -1:
        raise ValueError("Could not find sandbox service in docker-compose.yml")
        
    volumes_idx = -1
    for i in range(sandbox_idx, len(lines)):
        if lines[i].strip().startswith('volumes:'):
            volumes_idx = i
            break
            
    if volumes_idx == -1:
        raise ValueError("Could not find volumes section under sandbox service")
        
    # Find the last volume entry in the sandbox volumes block
    last_val_idx = -1
    for i in range(volumes_idx + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith('-'):
            last_val_idx = i
        # If we hit another service or a higher indentation block (4 spaces or less), stop
        elif lines[i].strip() and not lines[i].startswith(' ' * 6):
            break
            
    if last_val_idx == -1:
        # No existing volume mappings (unlikely), insert right after 'volumes:'
        insert_idx = volumes_idx + 1
        indent = "      "
    else:
        insert_idx = last_val_idx + 1
        # Extract the exact leading indentation of the last entry
        line = lines[last_val_idx]
        indent = line[:line.find('-')]
        
    # Create the volume string format matching other configurations
    new_entry = f"{indent}- {host_path}:{container_path}:rw, z\n"
    
    # Check if the exact volume is already mapped
    check_str = f"{host_path}:{container_path}"
    for line in lines[volumes_idx:insert_idx]:
        if check_str in line:
            return True # Already exists
            
    lines.insert(insert_idx, new_entry)
    
    with open(DOCKER_COMPOSE_PATH, 'w') as f:
        f.writelines(lines)
    return True
