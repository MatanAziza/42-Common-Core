from .CardFactory import CardFactory
from ex0 import Card, CreatureCard
from ex1 import SpellCard, ArtifactCard
from typing import Dict, Any
import random


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
        elements = {"Fire": 4, "Ice": 2, "Lightning": 3}
        elem_rar = {
                        "Fire": "Epic",
                        "Ice": "Common",
                        "Lightning": "Rare"
                        }
        cost = 0
        elements = {"Fire": 4, "Ice": 2, "Lightning": 3}
        for value in elements.keys():
            if value in name_or_power:
                cost += elements.get(value)
        rarity: str = ""
        effect: str = ""
        for value in elem_rar.keys():
            if value in name_or_power:
                rarity = elem_rar.get(value)
                effect = str(value) + " damage"
        card = SpellCard(
                            name_or_power,
                            cost,
                            rarity,
                            effect
                            )
        return card

    def create_artifact(self, name_or_power: str | int | None = None) -> Card:
        rarity = [
                "Common",
                "Rare",
                "Epic",
                "Legendary"
                ]
        cost = random.randrange(1, 5)
        elem_effect = {
                        "Ring": f"+{2 * cost - 1} damage while active",
                        "Staff": f"+{2 * cost - 1} defense while active",
                        "Crystal": f"+{2 * cost - 1} mana per turn"
                        }
        effect: str = ""
        for value in elem_effect.keys():
            if value in name_or_power:
                effect = elem_effect.get(value)
        card = ArtifactCard(
                            name_or_power,
                            cost,
                            rarity[cost - 1],
                            cost * 3 - 2,
                            effect
        )
        return card

    def create_themed_deck(self, size: int) -> Dict:
        elements_crea = ["Fire", "Ice", "Storm", None]
        enemies = ["Dragon", "Goblin", "Kobold"]
        classes = ["Warrior", "Rogue"]
        elems = ["Fire Ball", "Ice Shards", "Lightning Strike"]
        colors = ["Crimson", "Cyan", "Golden", "Silver", "Purple"]
        artifacts = ["Ring", "Staff", "Crystal"]
        functions = [
                    self.create_artifact,
                    self.create_creature,
                    self.create_spell
                    ]
        name: Any = ""
        deck = dict()
        i = 0
        while i < size:
            elem = random.randrange(0, 3)
            if elem == 0:
                name = random.choice(colors) + " " + random.choice(artifacts)
            elif elem == 1:
                name = random.choice(elements_crea)
                if name is None:
                    name = random.choice(enemies)
                    name += " " + random.choice(classes)
                else:
                    name += " " + random.choice(enemies)
            elif elem == 2:
                name = random.choice(elems)
            card = functions[elem](name)
            can_add = False
            for _, cards in deck.items():
                infos = cards.get_card_info()
                if infos.get("name") == card.get_card_info().get("name"):
                    can_add = True
            if not can_add:
                deck.update({f"Card {i + 1}": card})
            else:
                i-=1
            i += 1
        return deck

    def get_supported_types(self) -> Dict:
        return {"Supported types": [
                                    "SpellCard",
                                    "ArtifactCard",
                                    "CreatureCard"
                                    ]}
