#!/usr/bin/env python3

import alchemy.elements
from alchemy.elements import create_earth
from alchemy.potions import wisdom_potion as wis, strength_potion as strt
from alchemy.elements import create_fire, create_water


if __name__ == "__main__":
    print("\n=== Import Transmutation Mastery ===\n")
    print("Method 1 - Full module import:")
    print(f"alchemy.elements.create_air(): {alchemy.elements.create_air()}")
    print("\nMethod 2 - Specific function import:")
    print(f"create_earth(): {create_earth()}")
    print("\nMethod 3 - Aliased import:")
    print(f"wis(): {wis()}")
    print("\nMethod 4 - Multiple imports:")
    print(f"create_earth(): {create_water()}")
    print(f"create_fire(): {create_fire()}")
    print(f"strength_potion():{strt()}")
    print("\nAll imports transmutaion methos mastered!")
