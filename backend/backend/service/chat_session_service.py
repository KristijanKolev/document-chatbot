from sqlalchemy.orm import Session
from backend import models, schemas, crud


class ChatSessionService:
    _DEFAULT_SESSION_NAME = "New session"

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_default_session(self) -> models.ChatSession:
        chat_session_in = schemas.ChatSessionCreate(name=self._DEFAULT_SESSION_NAME)
        return crud.chat_session.create(self.db, obj_in=chat_session_in)

    def process_prompt(self, session: models.ChatSession, prompt_in: schemas.ChatPromptIn) -> schemas.ChatPrompt:
        answer = ''  # Replace with call to LLM
        prompt_create = schemas.ChatPromptCreate(prompt=prompt_in.prompt, answer=answer, session_id=session.id)
        return crud.chat_prompt.create(self.db, obj_in=prompt_create)
