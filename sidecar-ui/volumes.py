import os
from typing import Optional
import yaml

WORKSPACE_DIR: str = "/workspace" if os.path.exists("/workspace") else os.path.join(os.path.dirname(__file__), "../../")
DOCKER_COMPOSE_PATH: str = os.path.join(WORKSPACE_DIR, "docker-compose.yml")


def _parse_volume_string(raw: str) -> dict:
    """Parse a docker-compose volume string into its components."""
    parts = raw.split(":")
    host_path = parts[0] if len(parts) > 0 else ""
    container_path = parts[1] if len(parts) > 1 else ""
    options_str = parts[2] if len(parts) > 2 else ""

    options = [o.strip() for o in options_str.split(",") if o.strip()] if options_str else []

    mode = "rw"
    selinux: Optional[str] = None
    for opt in options:
        if opt in ("rw", "ro"):
            mode = opt
        elif opt in ("z", "Z"):
            selinux = opt

    return {
        "host_path": host_path,
        "container_path": container_path,
        "mode": mode,
        "selinux": selinux,
        "raw": raw,
    }


def list_volumes() -> list[dict]:
    """
    Parse docker-compose.yml and return the volumes for the sandbox service.
    Each entry is a dict with: index, host_path, container_path, mode, selinux, raw.
    """
    try:
        with open(DOCKER_COMPOSE_PATH, "r") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        return []
    except Exception:
        return []

    try:
        raw_volumes: list = data["services"]["sandbox"]["volumes"]
    except (KeyError, TypeError):
        return []

    result: list[dict] = []
    for idx, vol in enumerate(raw_volumes):
        if not isinstance(vol, str):
            continue
        parsed = _parse_volume_string(vol)
        parsed["index"] = idx
        result.append(parsed)

    return result


def update_volume_mode(index: int, new_mode: str) -> None:
    """
    Update the rw/ro mode for the volume at the given index.
    Writes back to docker-compose.yml preserving comments and formatting.
    Validates that new_mode is 'rw' or 'ro'.
    """
    if new_mode not in ("rw", "ro"):
        raise ValueError(f"Invalid mode '{new_mode}': must be 'rw' or 'ro'")

    volumes = list_volumes()
    if index < 0 or index >= len(volumes):
        raise IndexError(f"Volume index {index} out of range")

    vol = volumes[index]
    old_raw = vol["raw"]
    old_mode = vol["mode"]
    other_mode = "ro" if new_mode == "rw" else "rw"

    # Build the new raw string by manipulating the options portion
    parts = old_raw.split(":")
    if len(parts) < 3:
        # No options yet — append the mode
        new_raw = old_raw + ":" + new_mode
    else:
        options_str = parts[2]
        options = [o.strip() for o in options_str.split(",") if o.strip()]
        new_options: list[str] = []
        replaced = False
        for opt in options:
            if opt == other_mode:
                new_options.append(new_mode)
                replaced = True
            elif opt == new_mode:
                new_options.append(opt)
                replaced = True
            else:
                new_options.append(opt)
        if not replaced:
            new_options.insert(0, new_mode)
        parts[2] = ",".join(new_options)
        new_raw = ":".join(parts)

    # Raw line search/replace in the file to preserve comments
    with open(DOCKER_COMPOSE_PATH, "r") as f:
        content = f.read()

    # Match the exact raw string as it appears (with possible leading whitespace/dash)
    # We replace the first occurrence that contains old_raw
    new_content = content.replace(old_raw, new_raw, 1)

    with open(DOCKER_COMPOSE_PATH, "w") as f:
        f.write(new_content)
