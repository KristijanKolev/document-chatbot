from datetime import datetime

from typing import TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .chat_session import ChatSession


class ChatPromptBase(BaseModel):
    prompt: str

    class Config:
        from_attributes = True


class ChatPromptSimple(ChatPromptBase):
    answer: str
    session_id: int
    created_at: datetime


class ChatPrompt(ChatPromptBase):
    id: int
    answer: str
    session: 'ChatSession'
    created_at: datetime


class ChatPromptIn(ChatPromptBase):
    pass


class ChatPromptCreate(ChatPromptBase):
    answer: str
    session_id: int
