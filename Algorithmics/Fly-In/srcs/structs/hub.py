from .drone import Drone
from enum import Enum
from typing import Self
from pydantic import BaseModel, Field, model_validator
from pydantic import ValidationError, ConfigDict


class Zones(Enum):
    """Zones enum, with values going from least to more valuable
    zone (blocked is deleted from the graph)

    Args:
        Enum (_type_): _description_

    Returns:
        _type_: _description_
    """
    RESTRICTED = 1
    NORMAL = 2
    PRIORITY = 3

    @staticmethod
    def zone_name(zone: "Zones") -> str:
        return str(zone.name).lower()


class NextHubInfos:
    """Contains hubs infos, used by hubs to know to which send drones
    """
    def __init__(self, max_drones: int,
                 max_link_capacity: int,
                 zone: int) -> None:
        self.max_drones = max_drones
        self.max_link_capacity = max_link_capacity
        self.zone = zone


class Hub(BaseModel):
    """A hub, whoch contains drones and communicates with other hubs

    Args:
        BaseModel (_type_): _description_

    Raises:
        ValidationError: _description_

    Returns:
        _type_: _description_
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: str = Field()
    zone: Zones = Field(default=Zones.NORMAL)
    color: str = Field(default="none")
    max_drones: int = Field(default=1)
    next_hubs: dict[str, NextHubInfos] = Field(default=dict())
    drones: list[Drone] = Field(default=[])

    @model_validator(mode='after')
    def validate_color(self) -> Self:
        """validates the color input of each hub

        Raises:
            ValidationError: _description_

        Returns:
            Self: _description_
        """
        if len(self.color.split("_")) > 1:
            raise ValidationError("Color is made of more than 2 words."
                                  "Please use one")
        return self
