from pathlib import Path
import shutil
import sys
import os

os.environ["NOTES_DIR_MOCK"] = "1"

# Add parent directory to path so main can be imported
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def setup():
    test_dir = Path("private-notes-test")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    test_dir.mkdir(parents=True, exist_ok=True)

def teardown():
    test_dir = Path("private-notes-test")
    if test_dir.exists():
        shutil.rmtree(test_dir)

def run_tests():
    setup()
    try:
        # 1. Create a note
        payload = {
            "title": "Test YouTube Idea",
            "category": "YouTube",
            "status": "Draft",
            "tags": ["test", "video"],
            "content": "This is test content"
        }
        resp = client.post("/api/notes", json=payload)
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"
        data = resp.json()
        assert data["title"] == "Test YouTube Idea", f"Expected title, got {data['title']}"
        assert data["filename"] == "test-youtube-idea.md"

        # 2. Get list of notes
        resp = client.get("/api/notes")
        assert resp.status_code == 200
        notes = resp.json()
        assert len(notes) == 1
        assert notes[0]["category"] == "YouTube"

        # 3. Get specific note
        resp = client.get("/api/notes/test-youtube-idea.md")
        assert resp.status_code == 200
        note = resp.json()
        assert note["content"] == "This is test content"

        # 4. Update note
        payload["status"] = "Active"
        payload["content"] = "Updated content"
        resp = client.put("/api/notes/test-youtube-idea.md", json=payload)
        assert resp.status_code == 200
        updated = resp.json()
        assert updated["status"] == "Active"

        # 5. Delete note
        resp = client.delete("/api/notes/test-youtube-idea.md")
        assert resp.status_code == 200
        resp = client.get("/api/notes")
        assert len(resp.json()) == 0
        
        print("ALL TESTS PASSED!")
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR RUNNING TESTS: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        teardown()

if __name__ == "__main__":
    run_tests()
