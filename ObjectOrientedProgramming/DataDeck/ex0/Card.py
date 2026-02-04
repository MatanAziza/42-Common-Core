from typing import Dict
from abc import ABC, abstractmethod


class Card(ABC):
    def __init__(self, name: str, cost: int, rarity: str):
        self.name = name
        self.cost = cost
        self.rarity = rarity

    def is_playable(self, available_mana: int) -> bool:
        if self.cost <= available_mana:
            return True
        return False

    def get_card_info(self) -> Dict:
        return {
                "name": self.name,
                "cost": self.cost,
                "rarity": self.rarity
            }

    @abstractmethod
    def play(self, game_state: Dict) -> Dict:
        pass
