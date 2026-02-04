from ex0.Card import Card
from typing import Dict

class ArtifactCard(Card):
    def __init__(
                self,
                name: str,
                cost: int,
                rarity: str,
                durability: int,
                effect: str
                ):
        super().__init__(name, cost, rarity)
        self.durability = durability
        self.effect = effect

    def play(self, game_state: Dict) -> Dict:
        return {}

    def activate_ability(self) -> Dict:
        return {}
