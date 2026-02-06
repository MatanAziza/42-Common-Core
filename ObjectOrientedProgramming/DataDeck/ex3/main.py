from .FantasyCardFactory import FantasyCardFactory

if __name__ == "__main__":
    factory = FantasyCardFactory()
    card = factory.create_creature("Fire Dragon")
    print(card.get_card_info())
