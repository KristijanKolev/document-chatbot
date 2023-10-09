from sqlalchemy.orm import Session

from backend.schemas.chat_session import ChatSessionCreate, ChatSessionUpdate
from backend.models import ChatSession, User
from .base import CRUDBase


class CRUDChatSession(CRUDBase[ChatSession, ChatSessionCreate, ChatSessionUpdate]):
    def get_all_for_user(self, db: Session, user: User) -> list[ChatSession]:
        return db.query(ChatSession).filter(
            ChatSession.user_id == user.id
        ).all()


chat_session = CRUDChatSession(ChatSession)
