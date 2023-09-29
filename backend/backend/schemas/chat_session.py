from typing import TYPE_CHECKING
from pydantic import BaseModel

if TYPE_CHECKING:
    from .chat_prompt import ChatPromptSimple


class ChatSessionBase(BaseModel):
    name: str


class ChatSession(ChatSessionBase):
    id: int
    prompts: list['ChatPromptSimple']

    class Config:
        from_attributes = True


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(ChatSessionBase):
    pass
