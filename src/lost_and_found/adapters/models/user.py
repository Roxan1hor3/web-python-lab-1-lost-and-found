from src.lost_and_found.adapters.models.base import EntityModel


class UserRetrieveModel(EntityModel):
    id: int
    password: str
    username: str
