from .CardFactory import CardFactory
from .GameStrategy import GameStrategy
from ex0 import Card
from typing import Dict


class GameEngine:
    def configure_engine(
            self,
            factory: CardFactory,
            strategy: GameStrategy
                            ) -> None:
        self.factory = factory
        self.strategy = strategy
        self.player_1 = factory.create_themed_deck(10)
        self.turns = 0
        self.damage_dealt = 0

    def simulate_turn(self) -> Dict:
        print("Simulating aggressive turn:")
        list_hand = []
        list_cards = []
        list_keys = []
        for key, card in self.player_1.items():
            list_hand.append(card)
            list_keys.append(key)
            card_info = card.get_card_info()
            list_cards.append(
                f"{card_info.get('name')}"
                f"({card_info.get('cost')})"
                                )
        print(f"Hand: [{', '.join(list_cards)}]\n")
        print("Turn execution:")
        print(f"Strategy: {type(self.strategy).__name__}")
        result = self.strategy.execute_turn(list_hand, [])
        played = result.get("cards_played")
        print(f"Actions: {result}")
        list_remove = []
        for i in range(len(list_keys)):
            j = i + 1
            while j < len(list_keys):
                card_1: Card = self.player_1.get(list_keys[i])
                card_2: Card = self.player_1.get(list_keys[j])
                name_1 = card_1.get_card_info().get("name")
                name_2 = card_2.get_card_info().get("name")
                cost_1 = card_1.get_card_info().get("cost")
                cost_2 = card_2.get_card_info().get("cost")
                name_check = name_1 in played and name_2 in played
                cost_check = cost_1 + cost_2 == result.get("mana_used")
                if name_check and cost_check:
                    list_remove.append(list_keys[i])
                    list_remove.append(list_keys[j])
                    break
                j += 1
            if list_remove:
                break
        for card in list_remove:
            self.player_1.pop(card)
        self.turns += 1
        self.damage_dealt += result.get("damage_dealt")
        return result

    def get_engine_status(self) -> Dict:
        return {
            "turns_simulated": self.turns,
            "strategy_used": type(self.strategy).__name__,
            "total_damage": self.damage_dealt
                }
