from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from ..db.database import Base
from .mixins import TimestampMixin


class ChatPrompt(Base, TimestampMixin):
    __tablename__ = 'chat_prompts'

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, nullable=False)
    answer = Column(String, nullable=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))

    session = relationship("ChatSession", back_populates="prompts")
