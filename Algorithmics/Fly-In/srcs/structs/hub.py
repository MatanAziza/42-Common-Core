from .drone import Drone
from enum import Enum
from typing import Self
from pydantic import BaseModel, Field, model_validator, ValidationError


class Zones(Enum):
    NORMAL = {"type": "normal", "cost": 1, "priority": False}
    BLOCKED = {"type": "blocked", "cost": -1, "priority": False}
    RESTRICTED = {"type": "restricted", "cost": 2, "priority": False}
    PRIORITY = {"type": "priority", "cost": 0, "priority": True}


class Hub(BaseModel):
    name: str = Field()
    zone: Zones = Field(default=Zones.NORMAL)
    color: str = Field(default="none")
    max_drones: int = Field(default=1)
    next_hubs: dict[str, dict[str, int | Zones]] = Field(default=dict())
    drones: list[Drone] = Field(default=[Drone()])

    @model_validator(mode='after')
    def validate_color(self) -> Self:
        if len(self.color.split(" ")) > 1:
            raise ValidationError("Color is made of more than 2 words."
                                  "Please use one")
        return self
