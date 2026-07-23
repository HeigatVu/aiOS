import asyncio
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter()
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent

@router.post("/api/update")
async def run_update():
    script_path = PROJECT_ROOT / "config-file" / "update-all.sh"
    if not script_path.exists():
        raise HTTPException(status_code=404, detail="Update script not found")

    async def _stream_update():
        try:
            proc = await asyncio.create_subprocess_exec(
                "bash", "config-file/update-all.sh",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.STDOUT,
                cwd=str(PROJECT_ROOT)
            )
            while True:
                line = await proc.stdout.readline()
                if not line:
                    break
                yield line.decode("utf-8", errors="replace")
            await proc.wait()
            yield f"\n[Process exited with code {proc.returncode}]\n"
        except Exception as e:
            yield f"\n[Error: {str(e)}]\n"

    return StreamingResponse(_stream_update(), media_type="text/plain")
