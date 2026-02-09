from .FantasyCardFactory import FantasyCardFactory

if __name__ == "__main__":
    factory = FantasyCardFactory()
    card = factory.create_creature("Fire Dragon")
    print(card.get_card_info())
    card_2 = factory.create_spell("Lightning Strike")
    print(card_2.get_card_info())
    card_3 = factory.create_artifact("Crimson Ring")
    print(card_3.get_card_info())
