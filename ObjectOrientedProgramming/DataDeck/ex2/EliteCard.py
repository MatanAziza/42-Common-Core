from .Combatable import Combatable
from .Magical import Magical
from ex0.Card import Card
from typing import Dict, List, Any


class EliteCard(Card, Combatable, Magical):
    def __init__(self, name, cost, rarity, health, atk, defense, mana):
        super().__init__(name, cost, rarity)
        self.health = health
        self.atk = atk
        self.defense = defense
        self.mana = mana

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

    def get_card_info(self) -> Dict:
        dic = super().get_card_info()
        dic.update({
                    "health": self.health,
                    "mana": self.mana,
                    "attack": self.atk,
                    "defense": self.defense
                    })
        return dic

    def attack(self, target: Any) -> Dict:
        return {
                "attacker": self.name,
                "target": target.name,
                "damage": self.atk,
                "combat_type": "melee"
                }

    def defend(self, incoming_damage: int) -> Dict:
        dic = {
                "defender": self.name,
                "damage_taken": incoming_damage,
                "damage_blocked": 3,
                "still_alive": True
        }
        final_blow = dic.get("damage_blocked") - dic.get("damage_taken")
        if self.health - final_blow <= 0:
            dic.update({"still_alive": False})
        return dic

    def get_combat_stats(self) -> Dict:
        return {
                "attack": self.atk,
                "defense": self.defense
                }

    def cast_spell(self, spell_name: str, targets: List) -> Dict:
        spells = {"Fireball": 4, "Vines": 3, "Excaliburne": 6}
        cost = 0
        try:
            cost = spells.get(spell_name)
        except Exception:
            spell_name = "No such spell"
        return {
                "caster": self.name,
                "spell": spell_name,
                "targets": [target.name for target in targets],
                "mana_used": cost
                }

    def channel_mana(self, amount: int) -> Dict:
        return {
                "channeled": amount,
                "total_mana": self.mana + amount
                }

    def get_magic_stats(self) -> Dict:
        return {
            "mana": self.mana
        }
