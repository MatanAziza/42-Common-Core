import sys
import json
from datetime import datetime
from typing import Self, List, Any, Dict
from enum import Enum
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


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)

    def get_member_infos(self) -> str:
        return f"- {self.name} ({self.rank.value}) - {self.specialization}\n"


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission_id(self) -> Self:
        if self.mission_id[0] != 'M':
            raise ValueError(
                "Space Mission ID must begin with 'M'.\n"
                "Please provide correct informations."
            )
        return self

    @model_validator(mode='after')
    def check_leader(self) -> Self:
        crew = self.crew
        leaders = ["commander", "captain"]
        for member in crew:
            if member.rank.value in leaders:
                return self
        raise ValueError(
            "No commander or captain aboard.\n"
            "Please hire an officer with a high enough rank."
                        )

    @model_validator(mode='after')
    def validate_long_mission(self) -> Self:
        if self.duration_days <= 365:
            return self
        crew = self.crew
        exp_members = 0
        for member in crew:
            exp_members += 1 if member.years_experience > 5 else 0
        if exp_members * 2 < len(crew):
            raise ValueError(
                "Not enough experienced members for this mission.\n"
                "Please hire more."
                                 )
        return self

    @model_validator(mode='after')
    def validate_crew(self) -> Self:
        for member in self.crew:
            if not member.is_active:
                raise ValueError(
                    "Some crew members are not active.\n"
                    "Please hire members willing to work."
                                )
        return self

    def get_infos(self) -> str:
        result = "========================================\n"
        result += "Valid mission created:\n"
        result += f"Mission: {self.mission_name}\n"
        result += f"ID: {self.mission_id}\n"
        result += f"Destination: {self.destination}\n"
        result += f"Duration: {self.duration_days} days\n"
        result += f"Budget: ${self.budget_millions}M\n"
        result += f"Crew size: {len(self.crew)}\n"
        result += "Crew members:\n"
        for member in self.crew:
            result += member.get_member_infos()
        result += "\n========================================"
        return result


def data_tester() -> None:
    list_missions: List[SpaceMission] = list()
    file_to_open = "../data_generator/generated_data/space_missions.json"
    with open(file_to_open) as file:
        data = json.load(file)
        for mission in data:
            try:
                list_missions.append(SpaceMission(**mission))
            except ValidationError as e:
                s = e.errors()[0]
                if s["loc"]:
                    print(f"{str(s["loc"])[2:-3].upper()}: ", end='')
                print(f"{s["msg"]}")
        for mission in list_missions:
            print(mission.get_infos())


def incorrect_data_tester() -> None:
    dict1: Dict[str, Any] = {
        "mission_id": "M2024_EUROPA",
        "mission_name": "Saturn Rings Research Mission",
        "destination": "Saturn Rings",
        "launch_date": "2024-09-18T00:00:00",
        "duration_days": 602,
        "crew": [{
            "member_id": "CM041",
            "name": "William Davis",
            "rank": "captain",
            "age": 35,
            "specialization": "Medical Officer",
            "years_experience": 14,
            "is_active": True
                    },
                 {
                   "member_id": "CM042",
                   "name": "Sarah Smith",
                   "rank": "captain",
                   "age": 55,
                   "specialization": "Research",
                   "years_experience": 30,
                   "is_active": True
                     },
                 {
                   "member_id": "CM043",
                   "name": "Elena Garcia",
                   "rank": "commander",
                   "age": 55,
                   "specialization": "Research",
                   "years_experience": 30,
                   "is_active": True
                     },
                 {
                   "member_id": "CM044",
                   "name": "Sofia Williams",
                   "rank": "officer",
                   "age": 30,
                   "specialization": "Systems Analysis",
                   "years_experience": 9,
                   "is_active": True
                     },
                 {
                   "member_id": "CM045",
                   "name": "Sarah Jones",
                   "rank": "lieutenant",
                   "age": 25,
                   "specialization": "Maintenance",
                   "years_experience": 11,
                   "is_active": True
                     },
                 {
                   "member_id": "CM046",
                   "name": "Lisa Rodriguez",
                   "rank": "officer",
                   "age": 30,
                   "specialization": "Life Support",
                   "years_experience": 12,
                   "is_active": True
                     },
                 {
                   "member_id": "CM047",
                   "name": "Sarah Smith",
                   "rank": "cadet",
                   "age": 28,
                   "specialization": "Pilot",
                   "years_experience": 8,
                   "is_active": False
                     }],
        "mission_status": "planned",
        "budget_millions": 1092.6
    }
    try:
        mission = SpaceMission(**dict1)
        print(mission.get_infos())
    except ValidationError as e:
        s = e.errors()[0]
        if s["loc"]:
            print(f"{str(s["loc"])[2:-3].upper()}: ", end='')
        print(f"{s["msg"]}")


def main():
    data_tester()
    incorrect_data_tester()


if __name__ == '__main__':
    in_venv = sys.prefix != sys.base_prefix
    if not in_venv:
        print(
            "Not in a virtual envorinment!\n"
            "Run:\n"
            "python -m venv space_env\n"
            "source space_env/bin/activate\n"
            "pip install pydantic\n"
            "Then re-run this program."
                )
    else:
        main()
