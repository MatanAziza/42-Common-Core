from .GameStrategy import GameStrategy
from ex0 import Card, CreatureCard
from typing import List, Dict


class AggressiveStrategy(GameStrategy):
    def execute_turn(self, hand: List, battlefield: List) -> Dict:
        e = []
        for enemy in battlefield:
            if isinstance(enemy, CreatureCard):
                e.append(enemy.get_card_info().get("name"))
        s = self.prioritize_targets(hand)[:2]
        actions = dict()
        actions.update(
            {
                "cards_played": [c.get_card_info().get("name") for c in s],
                "mana_used": sum([c.get_card_info().get("cost") for c in s]),
                "targets_attacked": e,
            }
        )
        damage = 0
        for card in s:
            atk = card.get_card_info().get("attack", "error")
            if atk != "error":
                damage += atk
            else:
                effect = card.get_card_info().get("effect", "error")
                if effect != "error" and "Deal" in effect:
                    damage += int(effect[5:-17])
        actions.update({"damage_dealt": damage})
        return actions

    def get_strategy_name(self) -> str:
        return self.__name__

    def prioritize_targets(self, available_targets: List[Card]) -> List:
        def cost_sort(card: Card) -> int:
            return card.get_card_info().get("cost")

        available_targets.sort(key=cost_sort)
        return available_targets
