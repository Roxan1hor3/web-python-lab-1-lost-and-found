from pydantic import ConfigDict, BaseModel


class EntityModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
