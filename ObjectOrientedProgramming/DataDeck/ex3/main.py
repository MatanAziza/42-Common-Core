from .AggressiveStrategy import AggressiveStrategy
from .GameEngine import GameEngine
from .FantasyCardFactory import FantasyCardFactory


if __name__ == "__main__":
    print("=== DataDeck Game Engine ===\n")
    print("Configuring Fantasy Card Game...")
    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()
    game_engine = GameEngine()
    game_engine.configure_engine(factory, strategy)
    print("Factory: FantasyCardFactory")
    print("Strategy: AggressiveStrategy")
    creatures = ["dragon", "goblin", "kobold"]
    spells = ["fireball", "ice shards", "lightning"]
    artifacts = ["crystal", "staff", "ring"]
    print(
        f"Available types: creatures: {creatures}, spells:"
        f" {spells}, artifacts: {artifacts}\n"
            )
    for i in range(1):
        game_engine.simulate_turn()
    print()
    print("Game report:")
    print(game_engine.get_engine_status())
    print(
        "\nAbstract Factory + Strategy Pattern:"
        " Maximum flexibility achieved!"
            )
