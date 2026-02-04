#!/usr/bin/env python3

from alchemy.grimoire import validate_ingredients, record_spell

if __name__ == "__main__":
    print("\n=== Circular Curse Breaking ===\n")
    print("Testing ingredients validation:")
    print(
        'validate_ingredients("fire air"):'
        f'{validate_ingredients("fire air")}'
    )
    print(
        'validate_ingredients("dragon scales"):'
        f'{validate_ingredients("dragon scales")}'
    )
    print("\nTesting spell recording with validation:")
    print(
        'record_spell("Fireball", "fire air"):'
        f'{record_spell("Fireball", "fire air")}'
    )
    print(
        'record_spell("Dark Magic", "shadow"):'
        f'{record_spell("Dark Magic", "shadow")}'
    )
