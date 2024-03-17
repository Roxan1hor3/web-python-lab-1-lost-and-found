from src.lost_and_found.adapters.orm import Comment
from src.lost_and_found.adapters.repos.base import BaseSQLAlchemyRepo


class CommentRepo(BaseSQLAlchemyRepo):
    orm_model = Comment
