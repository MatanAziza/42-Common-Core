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
            if args[0] >= min_power:
                func(*args)
            else:
                return "Insufficient power for this spell"
        new_func.__name__ = func.__name__
        return new_func
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def try_for(func: Callable):
        def new_func(*args) -> Any:
            i = 1
            while (i < max_attempts):
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
        pass

    def cast_spell(self, spell_name: str, power: int) -> str:
        pass
