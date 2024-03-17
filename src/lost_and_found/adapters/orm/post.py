from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from src.lost_and_found.adapters.orm.base import BaseOrmModel


class PostOrm(BaseOrmModel):
    __tablename__ = "post"

    name = Column(String(60))
    description = Column(String(255))
    author_id = Column(Integer, ForeignKey("user.id"))
    photo = Column(String)
    founder_contact = Column(String(60), nullable=True)
    date = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, name={self.name})>"
