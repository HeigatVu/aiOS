import docker.errors

import docker_bridge


def _exec_git(path: str, args: list[str]) -> tuple[int, str]:
    client = docker_bridge.get_docker_client()
    if not client:
        return 0, "[MOCK] git not available in mock mode"
    try:
        container = client.containers.get("ai_tui_sandbox")
        result = container.exec_run(["git", "-C", path] + args, user="root")
        output = result.output.decode("utf-8", errors="replace") if result.output else ""
        return result.exit_code, output
    except docker.errors.NotFound:
        return 1, "Container 'ai_tui_sandbox' not found"
    except Exception as e:
        return 1, str(e)


def get_git_status(path: str) -> dict:
    exit_code, output = _exec_git(path, ["status", "--porcelain=v1", "-b"])
    if exit_code != 0:
        return {"ok": False, "error": output, "branch": "", "staged": [], "unstaged": [], "untracked": []}

    branch = ""
    staged: list[dict] = []
    unstaged: list[dict] = []
    untracked: list[str] = []

    for line in output.splitlines():
        if line.startswith("## "):
            branch = line[3:].split("...")[0].strip()
        elif line.startswith("?? "):
            untracked.append(line[3:].strip())
        elif len(line) >= 2:
            x, y = line[0], line[1]
            fname = line[3:].strip()
            if x not in (" ", "?"):
                staged.append({"status": x, "file": fname})
            if y not in (" ", "?"):
                unstaged.append({"status": y, "file": fname})

    return {
        "ok": True,
        "branch": branch,
        "staged": staged,
        "unstaged": unstaged,
        "untracked": untracked,
    }


def get_git_diff(path: str, staged: bool = False) -> str:
    args = ["diff", "--stat", "--patch"] if not staged else ["diff", "--cached", "--stat", "--patch"]
    _, output = _exec_git(path, args)
    return output or "(no diff)"


def git_stage_all(path: str) -> dict:
    code, output = _exec_git(path, ["add", "-A"])
    return {"ok": code == 0, "output": output}


def git_commit(path: str, message: str) -> dict:
    code, output = _exec_git(path, ["commit", "-m", message])
    return {"ok": code == 0, "output": output}


def git_push(path: str) -> dict:
    code, output = _exec_git(path, ["push"])
    return {"ok": code == 0, "output": output}
