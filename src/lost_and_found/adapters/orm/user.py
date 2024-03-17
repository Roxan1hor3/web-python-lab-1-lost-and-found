from sqlalchemy import Column, String
from src.lost_and_found.adapters.orm.base import BaseOrmModel


class User(BaseOrmModel):
    __tablename__ = "user"

    username = Column(String(255))
    password = Column(String(255))

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"
