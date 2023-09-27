from backend.schemas.chat_session import ChatSessionCreate, ChatSessionUpdate
from backend.models.chat_session import ChatSession
from .base import CRUDBase


class CRUDChatSession(CRUDBase[ChatSession, ChatSessionCreate, ChatSessionUpdate]):
    pass
