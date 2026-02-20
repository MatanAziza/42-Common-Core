from typing import Callable, Any


def mage_counter() -> Callable:
    number_calls = 0

    def called() -> int:
        nonlocal number_calls
        number_calls += 1
        return number_calls
    return called


def spell_accumulator(initial_power: int) -> Callable:
    power = initial_power

    def new_power(add_value: int) -> int:
        nonlocal power
        power += add_value
        return power
    return new_power


def enchantment_factory(enchantment_type: str) -> Callable:
    return lambda item: f"{enchantment_type} {item}"


def memory_vault() -> dict[str, Callable]:
    database = dict()

    def store(key: Any, value: Any) -> None:
        database.update({key: value})

    def recall(key: Any) -> Any:
        value = database.get(key, "error")
        return value if value != "error" else "Memory not found"
    return {
        "store": store,
        "recall": recall
            }


if __name__ == "__main__":
    spell_counter = mage_counter()
    print("Counting usage of spell:")
    for i in range(5):
        print(f"Call {i+1}: {spell_counter()}")
    init_power = 10
    print(f"\nAccumulating power with initial_power of {init_power}:")
    accumulator = spell_accumulator(init_power)
    for i in range(5):
        print(f"Adding {i+1} power: {accumulator(i+1)}")
    print("\nCreating multiples enchantment factory (flaming, frozen):")
    flame_ench = enchantment_factory("Flaming")
    froz_ench = enchantment_factory("Frozen")
    print(flame_ench("Sword"))
    print(froz_ench("Shield"))
    print("\nStorage demo:")
    funcs = memory_vault()
    store = funcs["store"]
    recall = funcs["recall"]
    values_to_store = {
        "sword": "flaming",
        "shield": "frozen",
        "spear": "justice"
                        }
    for key, value in values_to_store.items():
        store(key, value)
        print(f"Stored key/value couple {key}:{value}")
    print("Recall demo:")
    print(f"Getting 'sword' value: {recall('sword')}")
    print(f"Getting 'wrong_key' value: {recall('wrong_value')}")
