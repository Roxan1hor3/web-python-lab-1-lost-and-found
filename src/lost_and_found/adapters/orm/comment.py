from sqlalchemy import Column, ForeignKey, Integer, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from src.lost_and_found.adapters.orm.base import BaseOrmModel


class Comment(BaseOrmModel):
    __tablename__ = "comment"

    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))
    author_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    text = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")

    def __repr__(self):
        return f"<Comment(id={self.id}, text={self.text})>"
