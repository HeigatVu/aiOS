from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Callable

from services.agents import AgentCatalog
from services.jobs import Job, JobStore


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    output: str


CommandRunner = Callable[[list[str]], CommandResult]


class AgentJobExecutor:
    def __init__(self, *, catalog: AgentCatalog, store: JobStore, command_runner: CommandRunner | None = None) -> None:
        self.catalog = catalog
        self.store = store
        self.command_runner = command_runner or self._run_command

    def run_next(self) -> Job | None:
        job = self.store.start_next()
        if job is None:
            return None
        try:
            for command in self._commands_for(job):
                self.store.append_log(job.id, "$ " + " ".join(command))
                result = self.command_runner(command)
                if result.output.strip():
                    self.store.append_log(job.id, result.output.strip())
                if result.returncode != 0:
                    return self.store.finish(job.id, status="failed")
            return self.store.finish(job.id, status="succeeded")
        except Exception as error:
            self.store.append_log(job.id, f"error: {error}")
            return self.store.finish(job.id, status="failed")

    def _commands_for(self, job: Job) -> list[list[str]]:
        if job.kind in {"agent-check", "agent-update"}:
            requested = job.payload.get("agents")
            if not isinstance(requested, list) or not requested:
                raise ValueError("Agent job has no agents")
            agents = {agent.id: agent for agent in self.catalog.agents}
            commands = []
            for agent_id in requested:
                agent = agents.get(agent_id)
                if agent is None:
                    raise ValueError(f"Unknown managed agent: {agent_id}")
                commands.append(agent.version_command if job.kind == "agent-check" else agent.update_command)
            return commands
        if job.kind == "extension-install":
            source = job.payload.get("source")
            name = job.payload.get("name")
            version = job.payload.get("version")
            if not all(isinstance(value, str) and value for value in (source, name, version)):
                raise ValueError("Extension job is incomplete")
            if source == "npm":
                return [["npm", "install", "--global", f"{name}@{version}"]]
            if source == "pypi":
                return [["uv", "tool", "install", f"{name}=={version}"]]
            raise ValueError("Unsupported extension source")
        raise ValueError(f"Unsupported job kind: {job.kind}")

    @staticmethod
    def _run_command(command: list[str]) -> CommandResult:
        completed = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=900,
        )
        return CommandResult(returncode=completed.returncode, output=completed.stdout)
