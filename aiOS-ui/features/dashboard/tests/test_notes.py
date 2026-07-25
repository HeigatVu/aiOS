import asyncio
import pytest
from pathlib import Path
import shutil
import httpx

# Mock path setting
import os
os.environ["NOTES_DIR_MOCK"] = "1"

# Add parent directory to path so main can be imported
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app


async def _request_async(method, path, **kwargs):
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        return await client.request(method, path, **kwargs)


def request(method, path, **kwargs):
    return asyncio.run(_request_async(method, path, **kwargs))

@pytest.fixture(autouse=True)
def setup_teardown():
    # Setup clean test private-notes
    test_dir = Path("private-notes-test")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir(parents=True, exist_ok=True)
    yield
    if test_dir.exists():
        shutil.rmtree(test_dir)

def test_notes_crud():
    # 1. Create a note
    payload = {
        "title": "Test YouTube Idea",
        "category": "YouTube",
        "status": "Draft",
        "tags": ["test", "video"],
        "content": "This is test content"
    }
    resp = request("POST", "/api/notes", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "Test YouTube Idea"
    assert data["filename"] == "test-youtube-idea.md"

    # 2. Get list of notes
    resp = request("GET", "/api/notes")
    assert resp.status_code == 200
    notes = resp.json()
    assert len(notes) == 1
    assert notes[0]["category"] == "YouTube"

    # 3. Get specific note
    resp = request("GET", "/api/notes/test-youtube-idea.md")
    assert resp.status_code == 200
    note = resp.json()
    assert note["content"] == "This is test content"

    # 4. Update note
    payload["status"] = "Active"
    payload["content"] = "Updated content"
    resp = request("PUT", "/api/notes/test-youtube-idea.md", json=payload)
    assert resp.status_code == 200
    updated = resp.json()
    assert updated["status"] == "Active"

    # 5. Delete note
    resp = request("DELETE", "/api/notes/test-youtube-idea.md")
    assert resp.status_code == 200
    resp = request("GET", "/api/notes")
    assert len(resp.json()) == 0
