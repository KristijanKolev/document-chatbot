from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from ..db.database import Base
from .mixins import TimestampMixin


class ChatSession(Base, TimestampMixin):
    __tablename__ = 'chat_sessions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    prompts = relationship("ChatPrompt", back_populates="session", order_by='ChatPrompt.id')
    user = relationship("User")
