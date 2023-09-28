from typing import TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .chat_session import ChatSession


class ChatPromptBase(BaseModel):
    prompt: str


class ChatPrompt(BaseModel):
    id: int
    answer: str
    session: 'ChatSession'

    class Config:
        from_attributes = True


class ChatPromptIn(BaseModel):
    pass


class ChatPromptCreate(BaseModel):
    answer: str
