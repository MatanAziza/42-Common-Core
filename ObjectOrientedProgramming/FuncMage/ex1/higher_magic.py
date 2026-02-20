from typing import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    return lambda *args: (spell1(*args), spell2(*args))


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    return lambda: base_spell() * multiplier


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    return lambda *args: spell(*args) if condition(*args) else "Spell fizzled"


def spell_sequence(spells: list[Callable]) -> Callable:
    return lambda *args: [spell(*args) for spell in spells]


def fireball(target: str) -> str:
    return f"FireBall hits {target}"


def heal(target: str) -> str:
    return f"Heal {target}"


def freeze(target: str) -> str:
    return f"Freezes {target}"


def fire_ball() -> int:
    return 50


def condition_check(power: int) -> bool:
    if power <= 10:
        return False
    return True


def ice_ball(power: int) -> str:
    return f"Iceball with {power} power"


if __name__ == "__main__":
    target = "Dragon"
    res = spell_combiner(fireball, heal)(target)
    print("Spell combined: Fireball, Heal")
    print(res[0], ", ", res[1])
    megafire_ball = power_amplifier(fire_ball, 5)
    print("\nSpell amplifier target: Fireball")
    print(f"Original: {fire_ball()}, Amplified: {megafire_ball()}")
    potential_spell = conditional_caster(condition_check, ice_ball)
    print("\nConditional casting with minpower = 10, power = 10:")
    print(potential_spell(10))
    print("Conditional casting with minpower = 10, power = 50:")
    print(potential_spell(50))
    spells = spell_sequence([fireball, freeze, heal])
    print("\nSequence spelling (fireball, freeze, heal:")
    print(", ".join(spells("Dragon")))
