from DataDeck.ex0 import Card, CreatureCard
from .ArtifactCard import ArtifactCard
from .SpellCard import SpellCard
from typing import Dict, List
from random import shuffle as shuf


class Deck:
    def __init__(self, deck_name: str):
        self.name = deck_name
        self.deck: List[Card] = []

    def add_card(self, card: Card) -> None:
        self.deck.append(card)

    def remove_card(self, card_name: str) -> bool:
        for card in self.deck:
            if card_name == card.name:
                self.deck.remove(card)
                return True
        return False

    def shuffle(self) -> None:
        shuf(self.deck)

    def draw_card(self) -> Card:
        return_card = self.deck[0]
        for i in range(len(self.deck) - 1):
            self.deck[i] = self.deck[i + 1]
        self.deck.pop(-1)
        return return_card

    def get_deck_stats(self) -> Dict:
        count = [0, 0, 0]
        cost: float = 0
        for card in self.deck:
            if isinstance(card, CreatureCard):
                count[0] += 1
            elif isinstance(card, SpellCard):
                count[1] += 1
            elif isinstance(card, ArtifactCard):
                count[2] += 1
            cost += card.cost
        return {
                "total_cards": len(self.deck),
                "creatures": count[0],
                "spells": count[1],
                "artifacts": count[2],
                "avg_cost": (cost/len(self.deck)//0.01)/100
        }
