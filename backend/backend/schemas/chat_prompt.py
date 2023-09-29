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


class ChatPrompt(ChatPromptBase):
    id: int
    answer: str
    session: 'ChatSession'


class ChatPromptIn(ChatPromptBase):
    pass


class ChatPromptCreate(ChatPromptBase):
    answer: str
    session_id: int
