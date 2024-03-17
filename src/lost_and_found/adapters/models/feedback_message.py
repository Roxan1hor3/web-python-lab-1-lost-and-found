from datetime import datetime

from src.lost_and_found.adapters.models.base import EntityModel


class FeedbackMessageRetrieveModel(EntityModel):
    email: str
    text: str
    date: datetime
    id: int
