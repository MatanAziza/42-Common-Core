from abc import ABC, abstractmethod
from typing import Dict, Any


class Combatable(ABC):
    @abstractmethod
    def attack(self, target: Any) -> Dict:
        pass

    @abstractmethod
    def defend(self, incoming_damage: int) -> Dict:
        pass

    @abstractmethod
    def get_combat_stats(self) -> Dict:
        pass
