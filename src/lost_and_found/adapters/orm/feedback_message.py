from sqlalchemy import Column, String, DateTime, Text
from datetime import datetime

from src.lost_and_found.adapters.orm.base import BaseOrmModel


class FeedbackMessage(BaseOrmModel):
    __tablename__ = "feedback_message"

    email = Column(String(255))
    text = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<FeedbackMessage(id={self.id}, email={self.email})>"
