from datetime import datetime

from pydantic import BaseModel

from src.lost_and_found.adapters.models.base import EntityModel
from src.lost_and_found.adapters.models.comment import CommentRetrieveModel
from src.lost_and_found.adapters.models.user import UserRetrieveModel


class PostRetrieveModel(EntityModel):
    name: str
    description: str
    photo: str
    author_id: int
    date: datetime
    author: UserRetrieveModel

class PostCreateModel(BaseModel):
    name: str
    description: str
    photo: str
    author_id: int


class PostWithCommentsRetrieveModel(EntityModel):
    name: str
    description: str
    photo: str
    author_id: int
    date: datetime
    author: UserRetrieveModel
    comments: list[CommentRetrieveModel]
