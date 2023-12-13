from datetime import datetime

from sqlalchemy.orm import Session

from backend.schemas.chat_session import ChatSessionCreate, ChatSessionUpdate
from backend.models import ChatSession, User
from .base import CRUDBase


class CRUDChatSession(CRUDBase[ChatSession, ChatSessionCreate, ChatSessionUpdate]):

    def get_all_for_user(self, db: Session, user: User) -> list[ChatSession]:
        return db.query(ChatSession).filter(
            ChatSession.user_id == user.id
        ).order_by(ChatSession.created_at.asc()).all()

    def get_all_for_user_after_timestamp(self, db: Session, user: User, timestamp: datetime) -> list[ChatSession]:
        return db.query(ChatSession).filter(
                    ChatSession.user_id == user.id,
                    ChatSession.created_at >= timestamp
                ).order_by(ChatSession.created_at.asc()).all()


chat_session = CRUDChatSession(ChatSession)
