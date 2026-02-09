from .CardFactory import CardFactory
from .GameStrategy import GameStrategy
from typing import Dict


class GameEngine:
    def configure_engine(
                        self,
                        factory: CardFactory,
                        strategy: GameStrategy
                        ) -> None:
        self.factory = factory
        self.strategy = strategy
        self.player_1 = factory.create_themed_deck(3)

    def simulate_turn(self) -> Dict:
        print("Simulating aggressive turn:")
        list_hand = []
        list_cards = []
        for _, card in self.player_1.items():
            card_info = card.get_card_info()
            list_hand.append(card_info)
            list_cards.append(f"{card_info.get("name")} ({card_info.get("cost")})")
        self.strategy.execute_turn(list_hand, [])
        print(f"Hand: [{", ".join(list_cards)}]")

    def get_engine_status(self) -> Dict:
        return {}
