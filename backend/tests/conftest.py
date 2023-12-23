from typing import Callable

import pytest
from fastapi.testclient import TestClient
from langchain.schema import BaseMessage
from langchain.schema.runnable import RunnableSerializable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from backend.db.alembic_base import Base
from backend.models import User, ChatSession
from backend.api.api import app
from backend.api.deps import (get_db, get_conversation_chain, get_current_user)
from backend.service import ChatSessionService

SQLALCHEMY_DATABASE_URL = "sqlite://"


@pytest.fixture(scope='module', name='db')
def in_memory_db() -> Session:
    """Yield in-memory DB session."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db: Session) -> User:
    test_user = User(
        id=1,
        sso_provider='test',
        sso_id='123',
        display_name='Test name',
        email='',
        picture_url=''
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    yield test_user
    db.delete(test_user)
    db.commit()


@pytest.fixture(scope='function')
def test_session(db: Session, test_user) -> ChatSession:
    test_sesssion = ChatSession(
        name="Test session 1",
        user_id=test_user.id
    )
    db.add(test_sesssion)
    db.commit()
    db.refresh(test_sesssion)
    yield test_sesssion
    db.delete(test_sesssion)
    db.commit()


@pytest.fixture
def create_session(db: Session, test_user) -> Callable:
    created_sessions = []

    def _create_session(name=ChatSessionService._DEFAULT_SESSION_NAME):
        session = ChatSession(
            name=name,
            user_id=test_user.id
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        created_sessions.append(session)
        return session

    yield _create_session

    for session in created_sessions:
        db.delete(session)
        db.commit()


@pytest.fixture(scope='module')
def conversation_chain():
    """Return an LLM chain replacement that repeats the question as an answer."""
    def prompt_repeater(prompt_input: dict) -> dict:
        res = dict(prompt_input)
        res["answer"] = prompt_input["question"]
        return res

    return prompt_repeater


class DummyTitleGenerationChain(RunnableSerializable[dict, BaseMessage]):
    """Replacement class for the title generation chain that returns a dummy value when invoked."""
    def invoke(self, *args, **kwargs) -> BaseMessage:
        return BaseMessage(content='Generated title', type='')


@pytest.fixture(scope='module')
def title_generation_chain() -> RunnableSerializable[dict, BaseMessage]:
    return DummyTitleGenerationChain()


@pytest.fixture()
def test_client(db, conversation_chain, test_user) -> TestClient:
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_conversation_chain] = lambda: conversation_chain
    app.dependency_overrides[get_current_user] = lambda: test_user
    yield TestClient(app)
    app.dependency_overrides = {}
