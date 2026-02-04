from .Card import Card
from typing import Dict


class CreatureCard(Card):
    def __init__(
            self,
            name: str,
            cost: int,
            rarity: str,
            attack: int,
            health: int
                ):
        super().__init__(name, cost, rarity)
        self.__attack = 1
        self.__health = 1
        self.type = "Creature"
        self.attack = attack
        self.health = health

    @property
    def attack(self):
        return self.__attack

    @attack.setter
    def attack(self, attack: int):
        if attack <= 0:
            print("Attack damages not high enough. Automatically set to 1.")
        else:
            self.__attack = attack

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health: int):
        if health <= 0:
            print("Health not high enough. Automatically set to 1.")
        else:
            self.__health = health

    def get_card_info(self) -> Dict:
        dict_1 = super().get_card_info()
        dict_1.update({
                    "type": self.type,
                    "attack": self.attack,
                    "health": self.health
                    })
        return dict_1

    def attack_target(self, target) -> Dict:
        resolved = False
        print(f"{self.name} attacks {target.name}:")
        if self.attack >= target.health:
            resolved = True
        return {
            "attacker": self.name,
            "target": target.name,
            "damage_dealt": self.attack,
            "combat_resolved": resolved
        }

    def play(self, game_state: Dict) -> Dict:
        available_mana = game_state.get("available_mana")
        print(f"Playing {self.name} with {available_mana} mana available:")
        playable = self.is_playable(available_mana)
        print(f"Playable: {playable}")
        action_state = {}
        if playable is True:
            action_state.update({"card_played": self.name})
            action_state.update({"mana_used": self.cost})
            action_state.update({"effect": "Creature summoned to battlefield"})
        else:
            action_state.update({"card_played": None})
            action_state.update({"mana_used": 0})
            action_state.update({"effect": "No creature was summoned"})
        return action_state
