from sqlalchemy.orm import Session
from langchain.chains import ConversationalRetrievalChain

from backend import models, schemas, crud


class ChatSessionService:
    _DEFAULT_SESSION_NAME = "New session"

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_default_session(self) -> models.ChatSession:
        chat_session_in = schemas.ChatSessionCreate(name=self._DEFAULT_SESSION_NAME)
        return crud.chat_session.create(self.db, obj_in=chat_session_in)

    def process_prompt(self, llm_chain: ConversationalRetrievalChain, session: models.ChatSession,
                       prompt_in: schemas.ChatPromptIn) -> schemas.ChatPrompt:
        # Format previous prompts and answers to be used by the LLM chain
        chat_history = [(prompt.prompt, prompt.answer) for prompt in session.prompts]
        result = llm_chain({
            "question": prompt_in.prompt,
            "chat_history": chat_history
        })

        prompt_create = schemas.ChatPromptCreate(prompt=prompt_in.prompt, answer=result['answer'],
                                                 session_id=session.id)
        return crud.chat_prompt.create(self.db, obj_in=prompt_create)
