from sqlalchemy import MetaData, Column, Integer
from sqlalchemy.orm import DeclarativeBase

my_metadata = MetaData()


class BaseOrmModel(DeclarativeBase):
    metadata = my_metadata
    id = Column(Integer, primary_key=True)
