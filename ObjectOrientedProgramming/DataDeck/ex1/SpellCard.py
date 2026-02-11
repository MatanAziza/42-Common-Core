from DataDeck.ex0.Card import Card
from typing import Dict, List
from enum import Enum


class Effect(Enum):
    DAMAGE = 3
    HEAL = 3
    BUFF = 2
    DEBUFF = 2


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
        targets_dict = dict()
        for target in targets:
            if "damage" in self.effect_type:
                target.health -= Effect.DAMAGE.value
            elif "heal" in self.effect_type:
                target.health += Effect.HEAL.value
            elif "debuff" in self.effect_type:
                target.attack -= Effect.DEBUFF.value
            elif "buff" in self.effect_type:
                target.attack += Effect.BUFF.value
            targets_dict.update({target.name: target})
        return targets_dict

    def play(self, game_state: Dict) -> Dict:
        action_result = {
                        "card_played": self.name,
                        "mana_used": 0,
                        "effect": "Unsufficient mana. This card has no effect"
                        }
        if game_state.get("available_mana") >= self.cost:
            action_result.update({"mana_used": self.cost})
            if "damage" in self.effect_type:
                action_result.update({
                    "effect": f"Deal {Effect.DAMAGE.value} damage to target"
                                    })
            elif "heal" in self.effect_type:
                action_result.update({
                    "effect": f"Heal the target by {Effect.HEAL.value} HP"
                                    })
            elif "debuff" in self.effect_type:
                action_result.update({
                  "effect": f"Buff the target by {Effect.DAMAGE.value} damage"
                                    })
            elif "buff" in self.effect_type:
                action_result.update({
                 "effect": f"Debuff the target by {Effect.DAMAGE.value} damage"
                                      })
            else:
                action_result.update({
                    "effect": "This card has no effect"
                                      })
        return action_result

    def get_card_info(self) -> Dict:
        dict_1 = super().get_card_info()
        dict_1.update({"effect": self.effect_type})
        return dict_1
