from functools import reduce, partial, lru_cache, singledispatch
from typing import Callable


def spell_reducer(spells: list[int], operation: str) -> int:
    calculus = {
        "add": reduce(lambda x, y: x + y, spells),
        "multiply": reduce(lambda x, y: x * y, spells),
        "max": reduce(lambda x, y: x if x > y else y, spells),
        "min": reduce(lambda x, y: x if x < y else y, spells)
                    }
    return calculus[operation]


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    spells = {
        "fire_enchant": partial(base_enchantment, 50, "Fire"),
        "ice_enchant": partial(base_enchantment, 50, "Ice"),
        "lightning_enchant": partial(base_enchantment, 50, "Lightning")
                }
    return spells


@lru_cache
def memoized_fibonacci(n: int) -> int:
    if n == 0 or n == 1:
        return 0 if n == 0 else 1
    return memoized_fibonacci(n-1) + memoized_fibonacci(n-2)


def spell_dispatcher() -> Callable:
    @singledispatch
    def spell(arg):
        print(arg)

    @spell.register
    def _(arg: int):
        print(f"Spell does {arg} damage")

    @spell.register
    def _(arg: str):
        print(f"Casting {arg}")

    @spell.register
    def _(arg: list):
        for spell in arg:
            print(f"Casting {spell}")

    return spell


if __name__ == "__main__":
    print("Testing differents operations on spells:")
    op = spell_reducer([1, 2, 3, 4, 5], "add")
    print("Added spells:", op)
    op = spell_reducer([1, 2, 3, 4, 5], "multiply")
    print("Multiplied spells:", op)
    op = spell_reducer([1, 2, 3, 4, 5], "max")
    print("Most powerful spell:", op)
    op = spell_reducer([1, 2, 3, 4, 5], "min")
    print("Least powerful spell:", op)
    print("\nGenerating spells ready to cast on target:")
    spells = partial_enchanter(lambda x, y, z: print(
        f"Casting {y} with {x} damage on {z}"
                                                        ))
    for spell in spells.values():
        spell("Dragon")
    print("\nTesting memoized fibonacci...")
    for i in range(7):
        print(f"Fibonacci n°{i}: {memoized_fibonacci(i)}")
    print("\nCreating singledispatch function:")
    dis = spell_dispatcher()
    print("Testing with int : 5")
    dis(5)
    print("Testing with string: 'Fireball'")
    dis("Fireball")
    print("Testing with spell list: '[Fireball, Ice shards, Lightning]'")
    dis(["Fireball", "Ice shards", "Lightning"])
