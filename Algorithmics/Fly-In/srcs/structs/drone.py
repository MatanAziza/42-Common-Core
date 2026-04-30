from pydantic import BaseModel, Field


class Drone(BaseModel):
    number: int = Field(default=0)
