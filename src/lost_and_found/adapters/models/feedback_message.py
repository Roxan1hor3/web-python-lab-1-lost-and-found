from datetime import datetime

from pydantic import BaseModel

from src.lost_and_found.adapters.models.base import EntityModel


class FeedbackMessageRetrieveModel(EntityModel):
    email: str
    text: str
    date: datetime


class FeedbackMessageCreateModel(BaseModel):
    email: str
    text: str
