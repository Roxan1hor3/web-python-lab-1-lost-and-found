from sqlalchemy import Column, String, Uuid
from sqlalchemy.orm import relationship

from src.lost_and_found.adapters.orm.base import BaseOrmModel


class User(BaseOrmModel):
    __tablename__ = "user"

    username = Column(String(255))
    password = Column(String(255))
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    session_uuid = Column(Uuid, unique=True, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
