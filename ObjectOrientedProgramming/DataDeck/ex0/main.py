#!/usr/bin/env python3

from .CreatureCard import CreatureCard


if __name__ == "__main__":
    fire_dragon = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
    fire_dragon_2 = CreatureCard("Fire Dragon", 5, "Legendary", 7, 5)
    goblin = CreatureCard("Goblin Warrior", 3, "Unconmmon", 2, 3)
    print(f"CreatureCard Info:\n{fire_dragon.get_card_info()}\n")
    mana = 13
    action_state = fire_dragon.play({"available_mana": mana})
    print(f"Play result: {action_state}\n")
    mana -= action_state.get("mana_used")
    attack_result = fire_dragon.attack_target(goblin)
    mana -= 5
    print(f"Attack result: {attack_result}")
    print("\nTesting insufficient mana (3 available):")
    fire_dragon_2.play({"available_mana": mana})
