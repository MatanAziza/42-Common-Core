from typing import Callable, Any
import time
import random


def spell_timer(func: Callable) -> Callable:
    def new_func(*args) -> Any:
        start = time.time()
        print(f"Casting {func.__name__}...")
        result = func(*args)
        print(f"Spell executed in {time.time() - start}")
        return result

    new_func.__name__ = func.__name__
    return new_func


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable):
        def new_func(*args) -> Any:
            if args[-1] >= min_power:
                return func(*args)
            else:
                return "Insufficient power for this spell"

        new_func.__name__ = func.__name__
        return new_func

    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def try_for(func: Callable):
        def new_func(*args) -> Any:
            i = 1
            while i < max_attempts:
                try:
                    result = func(*args)
                    return result
                except Exception:
                    i += 1
                    print("Spell failed, retrying...")
            return f"Spell casting failed after {max_attempts} attempts"

        new_func.__name__ = func.__name__
        return new_func

    return try_for


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        if len(name) < 3:
            return False
        for c in "0123456789":
            if c in name:
                return False
        return True

    power_10 = power_validator(10)

    @power_10
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"{spell_name} cast with {power} power"


if __name__ == "__main__":

    @spell_timer
    def first_fireball() -> str:
        return "I don't care how small the room is, I Cast Fireball!"

    print("Testing spell timer:\n" + first_fireball())

    power_50 = power_validator(50)

    @power_50
    def second_fireball(power: int) -> str:
        res = "I don't care how small the room is,"
        return res + f"I Cast Fireball ({power} power)!"

    print("\nTesting power validator with 42 then 69:")
    print(second_fireball(42))
    print(second_fireball(69))

    try_for = retry_spell(5)

    @try_for
    def russian_roulette() -> Any:
        bullet = random.choice([False, False, False, False, False, True])
        if bullet is False:
            raise Exception
        return "You are dead Comrade!"

    print("\nTesting russia- hum retry_spell on some random spell:")
    print(russian_roulette())

    guild = MageGuild()
    print("\nTesting MageGuild methods:")
    print(guild.validate_mage_name("Vladimir"))
    print(guild.validate_mage_name("C3-P0"))
    print(guild.cast_spell("Little Red Book", 1917))
    print(guild.cast_spell("Capitalism 101", 2))
