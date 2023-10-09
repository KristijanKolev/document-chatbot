from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.db.alembic_base import Base

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
