from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_list_questions():
    payload = {
        "title": "Test Question",
        "body": "Test Body",
        "tag": "python",
        "difficulty": "easy"
    }

    res = client.post("/questions", json=payload)
    assert res.status_code == 201

    res = client.get("/questions")
    assert res.status_code == 200
    assert len(res.json()) >= 1
