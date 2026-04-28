from pydantic import BaseModel, Field, model_validator, ValidationError
from structs.hub import Hub

class Graph(BaseModel):
    nodes: list[Hub] = Field()
    paths_normal: dict[str, list[str]] = Field()
    paths_reverse: dict[str, list[str]] = Field()
