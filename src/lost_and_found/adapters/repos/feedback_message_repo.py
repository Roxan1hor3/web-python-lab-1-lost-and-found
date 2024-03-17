from src.lost_and_found.adapters.orm import FeedbackMessage
from src.lost_and_found.adapters.repos.base import BaseSQLAlchemyRepo


class FeedbackMessageRepo(BaseSQLAlchemyRepo):
    orm_model = FeedbackMessage
