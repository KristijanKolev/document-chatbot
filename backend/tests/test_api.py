from contextlib import contextmanager

from fastapi import status
from fastapi.testclient import TestClient

from backend.api.api import app
from backend.api.deps import (get_db, get_conversation_chain, get_current_user)
from backend.service.chat_session_service import ChatSessionService
from backend.crud import chat_session as chat_session_crud
from backend.schemas import ChatSessionCreate
from backend.models import ChatSession
from .utils import (get_in_memory_db, get_dummy_conversation_chain, setup_data, get_dummy_current_user)

app.dependency_overrides[get_db] = get_in_memory_db
app.dependency_overrides[get_conversation_chain] = get_dummy_conversation_chain
app.dependency_overrides[get_current_user] = get_dummy_current_user

client = TestClient(app)


def test_create_session():
    response = client.post(
        "/api/sessions/",
        json={}
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data
    assert data["name"] == "New session"
    assert data["prompts"] == []
    session_id = data["id"]

    response = client.get("/api/sessions/")
    assert response.status_code == 200, response.text
    data = response.json()
    data = [session for session in data if session["id"] == session_id]
    assert len(data) == 1
    session = data[0]
    assert session["name"] == "New session"


def test_update_session(setup_data):
    test_user, test_session = setup_data
    new_name = "Changed name"
    response = client.put(
        f"/api/sessions/{test_session.id}",
        json={"name": new_name}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == new_name
    assert data["id"] == test_session.id
    assert data["prompts"] == []


def test_prompt(setup_data):
    test_user, test_session = setup_data
    prompt = "Hello LLM!"
    response = client.post(
        f"/api/sessions/{test_session.id}/prompt",
        json={"prompt": prompt}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["prompt"] == prompt
    assert data["answer"] == prompt  # Dummy chain return prompt as answer
    assert "id" in data
    assert data["session"]["name"] == test_session.name
    assert data["session"]["id"] == test_session.id
    assert len(data["session"]["prompts"]) == 1


def test_prompt_limit(setup_data):
    test_user, test_session = setup_data
    with contextmanager(get_in_memory_db)() as db:
        prompt = "Hello LLM!"
        # Create prompts up to limit
        for _ in range(ChatSessionService._MAX_PROMPTS_PER_SESSION):
            client.post(
                f"/api/sessions/{test_session.id}/prompt",
                json={"prompt": prompt}
            )

        # Send prompt after limit is reached
        response = client.post(
            f"/api/sessions/{test_session.id}/prompt",
            json={"prompt": prompt}
        )
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.text

        refresh_session = chat_session_crud.get(db, id=test_session.id)
        assert len(refresh_session.prompts) == ChatSessionService._MAX_PROMPTS_PER_SESSION
