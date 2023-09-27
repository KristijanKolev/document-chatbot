from pydantic import BaseModel

from .chat_prompt import ChatPrompt


class ChatSessionBase(BaseModel):
    name: str


class ChatSession(ChatSessionBase):
    id: int
    prompts: list[ChatPrompt]

    class Config:
        orm_mode = True


class ChatSessionCreate(ChatSessionBase):
    pass


class ChatSessionUpdate(ChatSessionBase):
    pass
