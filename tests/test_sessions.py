from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_session():
    # Ensure at least one question exists
    client.post("/questions", json={
        "title": "Session Test",
        "body": "Test Body",
        "tag": "python",
        "difficulty": "medium"
    })

    res = client.post("/sessions", json={
        "tag": "python",
        "difficulty": "medium",
        "count": 1
    })

    assert res.status_code == 201
    assert "id" in res.json()
