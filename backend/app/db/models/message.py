from sqlalchemy import Column, Integer, ForeignKey, Text, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.connection import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())
    is_user = Column(Boolean, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    chat_session = relationship("ChatSession", back_populates="messages")
