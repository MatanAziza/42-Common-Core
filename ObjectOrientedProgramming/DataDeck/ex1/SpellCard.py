from ex0.Card import Card
from typing import Dict, List


class SpellCard(Card):
    def __init__(
                self,
                name: str,
                cost: int,
                rarity: str,
                effect_type: str
                ):
        super().__init__(name, cost, rarity)
        self.effect_type = effect_type

    def resolve_effect(self, targets: List) -> Dict:
        return {}

    def play(self, game_state: Dict) -> Dict:
        return {}






