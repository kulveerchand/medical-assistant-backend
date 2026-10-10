from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        nullable=False,
        index=True
    )

    question = Column(
        Text,
        nullable=False
    )

    response = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )