from .AggressiveStrategy import AggressiveStrategy
from .GameEngine import GameEngine
from .FantasyCardFactory import FantasyCardFactory


if __name__ == "__main__":
    factory = FantasyCardFactory()
    strategy = AggressiveStrategy()
    # card = factory.create_creature("Fire Dragon")
    # print(card.get_card_info())
    # card_2 = factory.create_spell("Lightning Strike")
    # print(card_2.get_card_info())
    # card_3 = factory.create_artifact("Crimson Ring")
    # print(card_3.get_card_info())
    # deck = factory.create_themed_deck(10)
    # for key, value in deck.items():
    #    print(key, value.get_card_info())
    # print(factory.get_supported_types())
    game_engine = GameEngine()
    game_engine.configure_engine(factory, strategy)
    game_engine.simulate_turn()
