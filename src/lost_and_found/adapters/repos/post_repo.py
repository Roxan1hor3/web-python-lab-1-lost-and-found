from src.lost_and_found.adapters.orm import PostOrm
from src.lost_and_found.adapters.repos.base import BaseSQLAlchemyRepo


class PostRepo(BaseSQLAlchemyRepo):
    orm_model = PostOrm
