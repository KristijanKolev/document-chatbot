from fastapi import status
from fastapi.testclient import TestClient

from backend.crud import chat_session as chat_session_crud
from backend.service.chat_session_service import ChatSessionService


def test_create_session(test_client: TestClient, db) -> None:
    response = test_client.post(
        "/api/sessions/",
        json={}
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["name"] == "New session"
    assert data["prompts"] == []
    session_id = data["id"]

    response = test_client.get("/api/sessions/")
    assert response.status_code == 200, response.text
    data = response.json()
    data = [session for session in data if session["id"] == session_id]
    assert len(data) == 1
    session = data[0]
    assert session["name"] == "New session"

    chat_session_crud.remove(db, id=session_id)


def test_update_session(test_user, test_session, test_client):
    new_name = "Changed name"
    response = test_client.put(
        f"/api/sessions/{test_session.id}",
        json={"name": new_name}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == new_name
    assert data["id"] == test_session.id
    assert data["prompts"] == []


def test_prompt(test_user, test_session, test_client):
    user_input = "Hello LLM!"
    response = test_client.post(
        f"/api/sessions/{test_session.id}/prompt",
        json={"prompt": user_input}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    prompt = data['prompt']
    session_updated = data['session_updated']
    assert not session_updated
    assert prompt["prompt"] == user_input
    assert prompt["answer"] == user_input  # Dummy chain return prompt as answer
    assert "id" in prompt
    assert prompt["session"]["name"] == test_session.name
    assert prompt["session"]["id"] == test_session.id
    assert len(prompt["session"]["prompts"]) == 1


def test_prompt_limit(db, test_user, test_session, test_client):
    prompt = "Hello LLM!"
    # Create prompts up to limit
    for _ in range(ChatSessionService._MAX_PROMPTS_PER_SESSION):
        test_client.post(
            f"/api/sessions/{test_session.id}/prompt",
            json={"prompt": prompt}
        )

    # Send prompt after limit is reached
    response = test_client.post(
        f"/api/sessions/{test_session.id}/prompt",
        json={"prompt": prompt}
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.text

    refresh_session = chat_session_crud.get(db, id=test_session.id)
    assert len(refresh_session.prompts) == ChatSessionService._MAX_PROMPTS_PER_SESSION
