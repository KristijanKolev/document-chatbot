from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from langchain.chains import ConversationalRetrievalChain

from backend import schemas, crud
from backend.models import User
from backend.service import ChatSessionService
from ..deps import get_db, get_chat_session_service, get_conversation_chain, get_current_user


router = APIRouter()


@router.get("/", response_model=list[schemas.ChatSessionSimple])
def get_user_sessions(
        db: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)],
):
    return crud.chat_session.get_all_for_user(db, user=user)


@router.get("/{session_id}", response_model=schemas.ChatSession)
def get_session_details(
        db: Annotated[Session, Depends(get_db)],
        session_id: int,
):
    return crud.chat_session.get_or_404(db=db, id=session_id)


@router.post("/", response_model=schemas.ChatSession)
def create_session(
        chat_session_service: Annotated[ChatSessionService, Depends(get_chat_session_service)],
        user: Annotated[User, Depends(get_current_user)],
):
    return chat_session_service.create_default_session(user)


@router.put("/{session_id}", response_model=schemas.ChatSession)
def update_session(
        db: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)],
        session_id: int,
        session_in: schemas.ChatSessionUpdate,
):
    session = crud.chat_session.get_or_404(db=db, id=session_id)
    if session.user != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return crud.chat_session.update(db=db, db_obj=session, obj_in=session_in)


@router.post(
    "/{session_id}/prompt",
    response_model=schemas.ChatPrompt,
    responses={status.HTTP_409_CONFLICT: {'model': schemas.BasicErrorResponse}}
)
def prompt_session(
        db: Annotated[Session, Depends(get_db)],
        user: Annotated[User, Depends(get_current_user)],
        chat_session_service: Annotated[ChatSessionService, Depends(get_chat_session_service)],
        llm_chain: Annotated[ConversationalRetrievalChain, Depends(get_conversation_chain)],
        session_id: int,
        prompt_in: schemas.ChatPromptIn,
):
    session = crud.chat_session.get_or_404(db, id=session_id)
    if session.user != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return chat_session_service.process_prompt(llm_chain=llm_chain, session=session, prompt_in=prompt_in)
