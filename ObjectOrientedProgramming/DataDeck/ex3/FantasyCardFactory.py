from .CardFactory import CardFactory
from ex0 import Card, CreatureCard
from ex1 import SpellCard, ArtifactCard
from typing import Dict


class FantasyCardFactory(CardFactory):
    def create_creature(self, name_or_power: str | int | None = None) -> Card:
        cost = 0
        elements = {"Fire": 3, "Ice": 1, "Lightning": 2}
        enemies = {"Dragon": 3, "Goblin": 1, "Kobold": 2}
        enemies_rar = {
                        "Dragon": "Legendary",
                        "Goblin": "Common",
                        "Kobold": "Epic"
                        }
        enemies_health = {
                            "Dragon": 5,
                            "Goblin": 2,
                            "Kobold": 3
                            }
        classes = {"Warrior": 2, "Rogue": 1}
        health: int = 0
        atk: int = 0
        for value in elements.keys():
            if value in name_or_power:
                cost += elements.get(value)
                health += elements.get(value)
                atk += elements.get(value) - 1
        for value in enemies.keys():
            if value in name_or_power:
                cost += enemies.get(value)
        for value in classes.keys():
            if value in name_or_power:
                cost += classes.get(value)
        rarity: str = ""
        for value in enemies_rar.keys():
            if value in name_or_power:
                rarity = enemies_rar.get(value)
        for value in enemies_health.keys():
            if value in name_or_power:
                health += enemies_health.get(value)
                atk += enemies_health.get(value)
        card = CreatureCard(
                            name_or_power,
                            cost,
                            rarity,
                            atk,
                            health
                            )
        return card

    def create_spell(self, name_or_power: str | int | None = None) -> Card:
        return SpellCard(name_or_power, 5, "e", "e")

    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        return ArtifactCard(name_or_power, 5, "e", 5, "e")

    def create_themed_deck(self, size: int) -> Dict:
        return {}

    def get_supported_types(self) -> Dict:
        return self.card
