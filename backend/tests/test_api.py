from fastapi.testclient import TestClient

from backend.api.api import app
from backend.api.deps import get_db, get_conversation_chain
from .utils import get_in_memory_db, get_dummy_conversation_chain


app.dependency_overrides[get_db] = get_in_memory_db
app.dependency_overrides[get_conversation_chain] = get_dummy_conversation_chain

client = TestClient(app)


def test_create_session():
    response = client.post(
        "/sessions/",
        json={}
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["name"] == "New session"
    assert data["prompts"] == []
    session_id = data["id"]

    response = client.get("/sessions/")
    assert response.status_code == 200, response.text
    data = response.json()
    data = [session for session in data if session["id"] == session_id]
    assert len(data) == 1
    session = data[0]
    assert session["name"] == "New session"
    assert session["prompts"] == []


def test_update_session():
    response = client.post(
        "/sessions/",
        json={}
    )
    data = response.json()
    session_id = data["id"]

    new_name = "Changed name"
    response = client.put(
        f"/sessions/{session_id}",
        json={"name": new_name}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == new_name
    assert data["id"] == session_id
    assert data["prompts"] == []


def test_prompt():
    response = client.post(
        "/sessions/",
        json={}
    )
    session = response.json()

    prompt = "Hello LLM!"
    response = client.post(
        f"/sessions/{session['id']}/prompt",
        json={"prompt": prompt}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["prompt"] == prompt
    assert data["answer"] == prompt  # Dummy chain return prompt as answer
    assert "id" in data
    assert data["session"]["name"] == session["name"]
    assert data["session"]["id"] == session["id"]
    assert len(data["session"]["prompts"]) == 1


