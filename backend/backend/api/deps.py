from typing import Generator, Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from backend import service
from backend.db.database import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_chat_session_service(db: Annotated[Session, Depends(get_db)]) -> service.ChatSessionService:
    return service.ChatSessionService(db)
