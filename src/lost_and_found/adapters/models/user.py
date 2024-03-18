from uuid import UUID

from pydantic import BaseModel

from src.lost_and_found.adapters.models.base import EntityModel


class UserRetrieveModel(EntityModel):
    password: str
    username: str
    session_uuid: UUID | None = None


class UserCreateModel(BaseModel):
    password: str
    username: str
