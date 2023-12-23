import pytest
from fastapi import HTTPException

from backend.config.settings import settings
from backend.crud import chat_session as chat_session_crud
from backend.schemas import ChatPromptIn
from backend.service import ChatSessionService


def test_create_session(db, test_user):
    service = ChatSessionService(db)
    new_session = service.create_default_session(user=test_user)

    assert new_session.user == test_user
    assert new_session.name == service._DEFAULT_SESSION_NAME
    assert new_session.prompts == []

    # Check DB record
    new_session = chat_session_crud.get(db, new_session.id)
    assert new_session.user == test_user
    assert new_session.name == service._DEFAULT_SESSION_NAME
    assert new_session.prompts == []

    chat_session_crud.remove(db, id=new_session.id)


def test_session_auto_naming(db, test_user, create_session, conversation_chain,
                             title_generation_chain):
    prompt_in = ChatPromptIn(prompt='Hello!')
    service = ChatSessionService(db)

    default_name_session = create_session()
    custom_name_session = create_session(name='Non-default name')

    service.process_prompt(
        llm_chain=conversation_chain,
        session=default_name_session,
        prompt_in=prompt_in,
        session_title_chain=title_generation_chain
    )
    service.process_prompt(
        llm_chain=conversation_chain,
        session=custom_name_session,
        prompt_in=prompt_in,
        session_title_chain=title_generation_chain
    )

    db.refresh(default_name_session)
    assert default_name_session.name == 'Generated title'
    assert len(default_name_session.prompts) == 1
    assert default_name_session.prompts[0].prompt == "Hello!"

    db.refresh(custom_name_session)
    assert custom_name_session.name == 'Non-default name'
    assert len(custom_name_session.prompts) == 1
    assert custom_name_session.prompts[0].prompt == "Hello!"


def test_session_prompts_limit(db, test_user, test_session, conversation_chain, title_generation_chain):
    prompt_in = ChatPromptIn(prompt='Hello!')
    service = ChatSessionService(db)
    # Send prompts up to the limit number.
    for _ in range(ChatSessionService._MAX_PROMPTS_PER_SESSION):
        service.process_prompt(
            llm_chain=conversation_chain,
            session=test_session,
            prompt_in=prompt_in,
            session_title_chain=title_generation_chain
        )
    # Assert that no more can be created.
    with pytest.raises(HTTPException):
        service.process_prompt(
            llm_chain=conversation_chain,
            session=test_session,
            prompt_in=prompt_in,
            session_title_chain=title_generation_chain
        )


def test_session_creation_limit(db, test_user):
    service = ChatSessionService(db)
    # Send prompts up to the limit number.
    for _ in range(settings.SESSIONS_LIMIT_PER_PERIOD):
        service.create_default_session(user=test_user)
    # Assert that no more can be created.
    with pytest.raises(HTTPException):
        service.create_default_session(user=test_user)
