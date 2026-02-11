from .TournamentPlatform import TournamentPlatform
from .TournamentCard import TournamentCard

if __name__ == "__main__":
    card_1 = TournamentCard(
        "Fire Dragon", 6, "Legendary", 10, 5, 3, "dragon_001"
                            )
    card_2 = TournamentCard("Ice Wizard", 4, "Epic", 6, 4, 4, "wizard_001")
    platform = TournamentPlatform()
    print("=== DataDeck Tournament Platform ===\n")
    print("Registering Tournament Cards...\n")
    platform.register_card(card_1)
    platform.register_card(card_2)
    print("Creating tournament match...")
    print(f"Result:{platform.create_match("dragon_001", "wizard_001")}\n")
    print("Tournament Leaderboard:")
    leaderboard = platform.get_leaderboard()
    for i in range(len(leaderboard)):
        print(leaderboard[i])
    print("\nPlatform Report:")
    print(platform.generate_tournament_report(), '\n')
