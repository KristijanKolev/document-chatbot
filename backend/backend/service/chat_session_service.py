from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from langchain.chains import ConversationalRetrievalChain

from backend import models, schemas, crud
from backend.config.settings import settings


class ChatSessionService:
    _DEFAULT_SESSION_NAME = "New session"
    _MAX_PROMPTS_PER_SESSION = 20

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_default_session(self, user: models.User) -> models.ChatSession:
        period_timedelta = timedelta(hours=settings.SESSIONS_LIMIT_PERIOD_LENGTH)
        ts_now = datetime.utcnow()
        filter_timestamp = ts_now - period_timedelta
        recent_user_sessions = crud.chat_session.get_all_for_user_after_timestamp(
            self.db,
            user=user,
            timestamp=filter_timestamp
        )
        if len(recent_user_sessions) >= settings.SESSIONS_LIMIT_PER_PERIOD:
            earliest_session = recent_user_sessions[0]
            # Calculate when a new session can be created
            wait_delta = period_timedelta - (ts_now - earliest_session.created_at)
            wait_hours = int(wait_delta.total_seconds() // 3600)
            wait_minutes = int((wait_delta.total_seconds() // 60) % 60) + 1
            if wait_hours > 0:
                wait_time_str = f"{wait_hours} hours, {wait_minutes} minutes"
            else:
                wait_time_str = f"{wait_minutes} minutes"
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Exceeded limit of {settings.SESSIONS_LIMIT_PER_PERIOD} sessions in the last "
                       f"{settings.SESSIONS_LIMIT_PERIOD_LENGTH} hours! Try again in {wait_time_str}."
            )
        chat_session_in = schemas.ChatSessionCreate(name=self._DEFAULT_SESSION_NAME, user_id=user.id)
        return crud.chat_session.create(self.db, obj_in=chat_session_in)

    def process_prompt(self, llm_chain: ConversationalRetrievalChain, session: models.ChatSession,
                       prompt_in: schemas.ChatPromptIn) -> schemas.ChatPrompt:
        if len(session.prompts) >= self._MAX_PROMPTS_PER_SESSION:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Exceeded limit of {self._MAX_PROMPTS_PER_SESSION} prompts per session! "
                       f"Create a new session and prompt away!"
            )

        # Format previous prompts and answers to be used by the LLM chain
        chat_history = [(prompt.prompt, prompt.answer) for prompt in session.prompts]
        result = llm_chain({
            "question": prompt_in.prompt,
            "chat_history": chat_history
        })

        prompt_create = schemas.ChatPromptCreate(prompt=prompt_in.prompt, answer=result['answer'],
                                                 session_id=session.id)
        return crud.chat_prompt.create(self.db, obj_in=prompt_create)
