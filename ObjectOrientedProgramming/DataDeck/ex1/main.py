from ex1 import SpellCard, ArtifactCard, Deck
from ex0 import CreatureCard

if __name__ == "__main__":
    print("=== DataDeck Deck Builder ===\n")
    print("Building deck with different card types...")
    deck = Deck("Test Deck")
    deck.add_card(SpellCard("Lightning Bolt", 3, "Epic", "damage"))
    deck.add_card(ArtifactCard(
                        "Mana Crystal",
                        2,
                        "Common",
                        5,
                        "Permanent: +1 mana per turn"
                                ))
    deck.add_card(CreatureCard("Fire Dragon", 5, "Legendary", 7, 6))
    print(f"Deck stats: {deck.get_deck_stats()}\n")
    print("Drawing and playing cards:")
    for i in range(3):
        card = deck.draw_card()
        print(f"Drew: {card.name} ({str(type(card).__name__)[:-4]})")
        print(f"Play result: {card.play({"available_mana": 10})}\n")
    print("Polymorphism in action: Same interface, different card behaviors!")
