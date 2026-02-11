from DataDeck.ex0 import Card
from DataDeck.ex2 import Combatable
from .Rankable import Rankable
from typing import Dict, List
from random import randrange


class TournamentCard(Card, Combatable, Rankable):
    def __init__(self,
                 name: str,
                 cost: int,
                 rarity: str,
                 health: int,
                 atk: int,
                 defense: int,
                 id: str
                 ):
        super().__init__(name, cost, rarity)
        self.id = id
        self.health = health
        self.atk = atk
        self.defense = defense
        self.wins = 0
        self.losses = 0
        self.rating = randrange(1100, 1201)
        self.game_state = {}

    def play(self, game_state: Dict) -> Dict:
        available_mana: int = game_state.get("available_mana")
        field: List = game_state.get("field")
        if self.cost <= available_mana:
            field.append(self)
            game_state.update({"field": field})
        else:
            print("Not enough mana to play this card.")
        for card in field:
            card.game_state = game_state
        return game_state

    def calculate_rating(self) -> int:
        self.rating += 15 * self.wins
        self.rating -= 10 * self.losses
        return self.rating

    def get_tournament_stats(self) -> Dict:
        return {
            "name": self.name,
            "interfaces": ["Card", "Rankable", "Combatable"],
            "rating": self.rating,
            "record": f"{self.wins}-{self.losses}"
        }

    def attack(self, target) -> Dict:
        dmg = self.atk
        target.defend(dmg)
        field = [self, target]
        target.game_state.update({"field": field})
        self.game_state.update({"field": field})
        return self.game_state

    def defend(self, incoming_damage: int) -> Dict:
        protect = self.defense
        act_dmg = 0
        if protect < incoming_damage:
            act_dmg = (incoming_damage - protect)
        self.health -= act_dmg
        return {"damage_taken": act_dmg}

    def get_combat_stats(self) -> Dict:
        return {
            "attack_damage": self.atk,
            "defense": self.defense,
            "health": self.health
                }

    def update_wins(self, wins: int) -> None:
        self.wins += wins

    def update_losses(self, losses: int) -> None:
        self.losses += losses

    def get_rank_info(self) -> Dict:
        return {
            "rank": self.rating
        }
