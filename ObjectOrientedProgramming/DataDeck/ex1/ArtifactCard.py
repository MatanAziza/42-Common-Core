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
        action_result = {
                        "card_played": self.name,
                        "mana_used": 0,
                        "effect": "Unsiufficient mana. This card has no effect"
                        }
        if game_state.get("available_mana") >= self.cost:
            action_result.update({
                "mana_used": self.cost,
                "effect": self.effect
                                })
        return action_result

    def activate_ability(self) -> Dict:
        return {}
