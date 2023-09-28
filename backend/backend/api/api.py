from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from backend import models, schemas, crud
from backend.service import ChatSessionService
from .deps import get_db, get_chat_session_service

app = FastAPI()


@app.get("/sessions", response_model=list[schemas.ChatSession])
def get_all_sessions(
        db: Annotated[Session, Depends(get_db)]
):
    return crud.chat_session.get_all(db)


@app.post("/sessions", response_model=schemas.ChatSession)
def create_session(
        chat_session_service: Annotated[ChatSessionService, Depends(get_chat_session_service)]
):
    return chat_session_service.create_default_session()


@app.post("/sessions/{session_id}/prompt", response_model=schemas.ChatSession)
def prompt_session(session_id: int, db: Annotated[Session, Depends(get_db)]):
    pass
