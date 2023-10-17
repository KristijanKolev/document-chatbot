import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.db.alembic_base import Base
from backend.models import User, ChatSession

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_in_memory_db():
    """Yield in-memory DB session."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def get_dummy_conversation_chain():
    """Return an LLM chain replacement that repeats the question as an answer."""
    def prompt_repeater(prompt_input: dict) -> dict:
        res = dict(prompt_input)
        res["answer"] = prompt_input["question"]
        return res

    return prompt_repeater


def get_dummy_current_user():
    return User(
        id=1,
        sso_provider='test',
        sso_id='123',
        display_name='Test name',
        email='',
        picture_url=''
    )


@pytest.fixture
def setup_data():
    test_db = next(get_in_memory_db())
    test_user = User(
        id=1,
        sso_provider='test',
        sso_id='123',
        display_name='Test name',
        email='',
        picture_url=''
    )
    test_db.add(test_user)
    test_db.commit()
    test_db.refresh(test_user)
    test_sesssion = ChatSession(
        name="Test session 1",
        user_id=test_user.id
    )
    test_db.add(test_sesssion)
    test_db.commit()
    test_db.refresh(test_sesssion)
    yield test_user, test_sesssion
    test_db.delete(test_user)
    test_db.delete(test_sesssion)
    test_db.commit()
