from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


from ..db.database import Base


class ChatSession(Base):
    __tablename__ = 'chat_sessions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    prompts = relationship('ChatPrompt', back_populates="session", order_by='ChatPrompt.id')
