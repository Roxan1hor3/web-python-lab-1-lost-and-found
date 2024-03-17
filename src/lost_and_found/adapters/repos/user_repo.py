from src.lost_and_found.adapters.orm import User
from src.lost_and_found.adapters.repos.base import BaseSQLAlchemyRepo


class UserRepo(BaseSQLAlchemyRepo):
    orm_model = User
