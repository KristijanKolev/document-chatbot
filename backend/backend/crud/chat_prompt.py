from typing import Any, Dict, Union

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from backend.schemas.chat_prompt import ChatPromptCreate
from backend.models.chat_prompt import ChatPrompt
from .base import CRUDBase


class CRUDChatPrompt(CRUDBase[ChatPrompt, ChatPromptCreate, None]):
    def update(*args, **kwargs):
        # Updates not supported for prompts
        raise NotImplementedError
    
    def create_with_session(
            self, db: Session, *, obj_in: ChatPromptCreate, schema_id: int
    ) -> ChatPrompt:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, schema_id=schema_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_multi_by_session(
            self, db: Session, *, session_id: int, skip: int = 0, limit: int = 100
    ) -> list[ChatPrompt]:
        return (
            db.query(self.model)
            .filter(ChatPrompt.session_id == session_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


chat_prompt = CRUDChatPrompt(ChatPrompt)
