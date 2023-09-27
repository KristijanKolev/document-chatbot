from pydantic import BaseModel

from .chat_session import ChatSession


class ChatPromptBase(BaseModel):
    prompt: str


class ChatPrompt(BaseModel):
    id: int
    answer: str
    session: ChatSession

    class Config:
        orm_mode = True


class ChatPromptIn(BaseModel):
    pass


class ChatPromptCreate(BaseModel):
    answer: str
