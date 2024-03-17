from datetime import datetime

from src.lost_and_found.adapters.models.base import EntityModel


class CommentRetrieveModel(EntityModel):
    post_id: int
    author_id: int
    text: str
    date: datetime
