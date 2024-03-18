from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.lost_and_found.adapters.orm.base import BaseOrmModel


class Post(BaseOrmModel):
    __tablename__ = "post"

    name = Column(String(60))
    description = Column(String(255))
    author_id = Column(Integer, ForeignKey("user.id"))
    photo = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

    def __repr__(self):
        return f"<Post(id={self.id}, name={self.name})>"
