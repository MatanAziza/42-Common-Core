import sys
import json
from datetime import datetime
from typing import Optional, Self, List
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


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def validate_id(self) -> Self:
        if self.contact_id[:2] != 'AC':
            raise ValueError(
                "Contact ID must begins with 'AC'.\n"
                "Please provide correct informations."
                                )
        return self

    @model_validator(mode='after')
    def validate_physical_contact(self) -> Self:
        if self.contact_type.value == "physical" and self.is_verified is False:
            raise ValueError(
                "Physical contact is not verified.\n"
                "Please check your sources before wasting our time."
            )
        return self

    @model_validator(mode='after')
    def validate_telepathic_contact(self) -> Self:
        if self.contact_type.value == "telepathic" and self.witness_count < 3:
            raise ValueError(
                "Telepathic contact cannot be established with less than 3 "
                "witnesses.\n Please gather more people."
            )
        return self

    @model_validator(mode='after')
    def validate_strong_signal(self) -> Self:
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError(
                "Such strong signal must come from a message\n"
                "Please check your sensors again."
            )
        return self

    def get_infos(self) -> str:
        result = "========================================\n"
        result += "Valid contact report:\n"
        result += f"ID: {self.contact_id}\n"
        result += f"Type: {self.contact_type.value}\n"
        result += f"Location: {self.location}\n"
        result += f"Signal: {self.signal_strength}\n"
        result += f"Duration: {self.duration_minutes}\n"
        result += f"Witnesses: {self.witness_count}\n"
        msg = self.message_received
        result += f"Message: {msg}\n" if msg is not None else ""
        result += "\n========================================"
        return result


def data_tester() -> None:
    list_contacts: List[AlienContact] = list()
    file_to_open = "../data_generator/generated_data/alien_contacts.json"
    with open(file_to_open) as file:
        data = json.load(file)
        for contact in data:
            try:
                list_contacts.append(AlienContact(**contact))
            except ValidationError as e:
                s = e.errors()[0]
                if s["loc"]:
                    print(f"{str(s["loc"])[2:-3].upper()}: ", end='')
                print(f"{s["msg"]}")
        for contact in list_contacts:
            print(contact.get_infos())


def incorrect_data_tester() -> None:
    list_contacts: List[AlienContact] = list()
    file_to_open = "../data_generator/generated_data/invalid_contacts.json"
    with open(file_to_open) as file:
        data = json.load(file)
        for contact in data:
            try:
                list_contacts.append(AlienContact(**contact))
            except ValidationError as e:
                s = e.errors()[0]
                if s["loc"]:
                    print(f"{str(s["loc"])[2:-3].upper()}: ", end='')
                print(f"{s["msg"]}")
        for contact in list_contacts:
            print(contact.get_infos())


def main():
    dict1 = {
            "contact_id": "AC_2024_015",
            "timestamp": "2024-01-02T00:00:00",
            "location": "Roswell, New Mexico",
            "contact_type": "radio",
            "signal_strength": 2.1,
            "duration_minutes": 9,
            "witness_count": 13,
            "message_received": None,
            "is_verified": False
                }
    try:
        contact = AlienContact(**dict1)
        print(contact.get_infos())
    except ValidationError as e:
        s = e.errors()[0]
        if s["loc"]:
            print(f"{str(s["loc"])[2:-3].upper()}: ", end='')
        print(f"{s["msg"]}")
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
