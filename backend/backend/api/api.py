from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from langchain.chains import ConversationalRetrievalChain

from backend import models, schemas, crud
from backend.service import ChatSessionService
from .deps import get_db, get_chat_session_service, get_conversation_chain

app = FastAPI()


@app.get("/sessions", response_model=list[schemas.ChatSession])
def get_all_sessions(
        db: Annotated[Session, Depends(get_db)]
):
    return crud.chat_session.get_all(db)


@app.post("/sessions", response_model=schemas.ChatSession)
def create_session(chat_session_service: Annotated[ChatSessionService, Depends(get_chat_session_service)]):
    return chat_session_service.create_default_session()


@app.put("/sessions/{session_id}", response_model=schemas.ChatSession)
def update_session(
        db: Annotated[Session, Depends(get_db)],
        session_id: int,
        session_in: schemas.ChatSessionUpdate
):
    session = crud.chat_session.get(db=db, id=session_id)
    return crud.chat_session.update(db=db, db_obj=session, obj_in=session_in)



@app.post("/sessions/{session_id}/prompt", response_model=schemas.ChatPrompt)
def prompt_session(
        db: Annotated[Session, Depends(get_db)],
        chat_session_service: Annotated[ChatSessionService, Depends(get_chat_session_service)],
        llm_chain: Annotated[ConversationalRetrievalChain, Depends(get_conversation_chain)],
        session_id: int,
        prompt_in: schemas.ChatPromptIn
):
    session = crud.chat_session.get(db, id=session_id)
    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Session with id {session_id} not found!')

    return chat_session_service.process_prompt(llm_chain=llm_chain, session=session, prompt_in=prompt_in)
