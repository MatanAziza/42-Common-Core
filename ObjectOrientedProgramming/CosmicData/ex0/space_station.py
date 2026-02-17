import sys
import json
from datetime import datetime
from typing import Optional, Self, List
try:
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv:
        print(
            "Not in a virtual environment!\n"
            "Run:\n"
            "python -m venv space_env\n"
            "source space_env/bin/activate\n"
            "pip install pydantic\n"
            "Then re-run this program."
                )
        sys.exit(1)
    from pydantic import BaseModel, Field, model_validator, ValidationError
except ImportError:
    print("Pydantic not imported.\nRun:\npip install pydantic\nThen rerun")
    sys.exit(1)


class SpaceStation(BaseModel):
    station_id: str = Field(default='Station_01')
    name: str = Field(default='InternationalSpaceStation')
    crew_size: int = Field(default=0)
    power_level: float = Field(default=100.0)
    oxygen_level: float = Field(default=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = None

    @model_validator(mode='after')
    def validate_id(self) -> Self:
        if len(self.station_id) < 3:
            raise ValueError(
                "Station ID is too short.\n"
                "Please provide a longer ID."
                                )
        elif len(self.station_id) > 10:
            raise ValueError(
                "Station ID is too long.\n"
                "Please provide a shorter ID."
                                )
        return self

    @model_validator(mode='after')
    def validate_crew(self) -> Self:
        if self.crew_size < 0:
            raise ValueError(
                "Crew Size cannot be negative.\n"
                "Please provide a positive number"
                            )
        elif self.crew_size > 20:
            raise ValueError(
                "Crew Size cannot be over 20.\n"
                "Please provide a smaller number."
                            )
        return self

    @model_validator(mode='after')
    def validate_name(self) -> Self:
        if len(self.name) < 1:
            raise ValueError(
                "Station Name is too short.\n"
                "Please provide a longer name."
                                )
        elif len(self.name) > 50:
            raise ValueError(
                "Station Name is too long.\n"
                "Please provide a shorter ID."
                                )
        return self

    @model_validator(mode='after')
    def validate_power(self) -> Self:
        if self.power_level < 0:
            raise ValueError(
                "Power level is too low.\n"
                "Please provide a higher value."
                            )
        elif self.power_level > 100.0:
            raise ValueError(
                "Power level is too high.\n"
                "Please provide a lower value."
            )
        return self

    @model_validator(mode='after')
    def validate_oxygen(self) -> Self:
        if self.power_level < 0:
            raise ValueError(
                "Oxygen level is too low.\n"
                "Please provide a higher value."
                            )
        elif self.power_level > 100.0:
            raise ValueError(
                "Oxygen level is too high.\n"
                "Please provide a lower value."
            )
        return self

    def get_infos(self) -> str:
        result = "========================================\n"
        result += "Valid station created:\n"
        result += f"ID: {self.station_id}\n"
        result += f"Name: {self.name}\n"
        result += f"Crew: {self.crew_size}\n"
        result += f"Power: {self.power_level}\n"
        result += f"Oxygen: {self.oxygen_level}\n"
        result += f"Status: {"Operational" if self.is_operational else "OOR"}"
        result += "\n\n========================================"
        return result


def data_tester() -> None:
    list_contacts: List[SpaceStation] = list()
    file_to_open = "../data_generator/generated_data/space_stations.json"
    with open(file_to_open) as file:
        data = json.load(file)
        for station in data:
            try:
                list_contacts.append(SpaceStation(**station))
            except ValidationError as e:
                s = e.errors()[0]
                if s["loc"]:
                    print(f"{str(s["loc"])[2:-3].upper()}: ", end='')
                print(f"{s["msg"]}")
        for station in list_contacts:
            print(station.get_infos())


def main():
    dict1 = {
             'station_id': "ISS_001",
             'name': "International Space Station",
             'crew_size': 5,
             'power_level': 90.8,
             'oxygen_level': 87.3,
             'last_maintenance': '2023-09-25T00:00:00',
             'is_operational': True,
             'notes': 'System diagnostics required'
             }
    try:
        station = SpaceStation(**dict1)
        print(station.get_infos())
    except ValidationError as e:
        s = e.errors()[0]
        if s["loc"]:
            print(f"{str(s["loc"])[2:-3].upper()}: ", end='')
        print(f"{s["msg"]}")
    data_tester()


if __name__ == '__main__':
    main()
