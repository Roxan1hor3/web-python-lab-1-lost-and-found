from datetime import datetime

from src.lost_and_found.adapters.models.base import EntityModel


class PostRetrieveModel(EntityModel):
    name: str
    description: str
    photo: str
    founder_contact: str | None = None
    author_id: int
    date: datetime
