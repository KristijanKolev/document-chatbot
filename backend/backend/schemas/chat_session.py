from typing import TYPE_CHECKING
from datetime import datetime

from pydantic import BaseModel

if TYPE_CHECKING:
    from .chat_prompt import ChatPromptSimple


class ChatSessionBase(BaseModel):
    name: str


class ChatSessionSimple(ChatSessionBase):
    id: int
    created_at: datetime


class ChatSession(ChatSessionSimple):
    prompts: list['ChatPromptSimple']

    class Config:
        from_attributes = True


class ChatSessionCreate(ChatSessionBase):
    user_id: int


class ChatSessionUpdate(ChatSessionBase):
    pass
