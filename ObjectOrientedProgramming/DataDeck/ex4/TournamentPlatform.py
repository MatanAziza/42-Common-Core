from .TournamentCard import TournamentCard
from typing import Dict, List


class TournamentPlatform:
    def __init__(self):
        self.registered = []
        self.leaderboard = []
        self.match_played = 0

    def register_card(self, card: TournamentCard) -> str:
        self.registered.append(card)
        print(f"{card.name} (ID: {card.id}):")
        stats = card.get_tournament_stats()
        print(
            f"- Interfaces: {stats.get("interfaces")}\n"
            f"- Rating: {stats.get("rating")}\n"
            f"- Record: {stats.get("record")}\n"
        )
        return f"{card.name} (ID: {card.id})"

    def create_match(self, card1_id: str, card2_id: str) -> Dict:
        card1: TournamentCard
        card2: TournamentCard
        for card in self.registered:
            if card.id == card1_id:
                card1 = card
            elif card.id == card2_id:
                card2 = card
        game_state = card1.play({"available_mana": 20, "field": []})
        game_state = card2.play(game_state)
        field: List[TournamentCard] = game_state.get("field")
        while True:
            game_state = field[0].attack(field[1])
            field = game_state.get("field")
            if field[1].health <= 0:
                field[0].update_wins(field[0].wins + 1)
                field[1].update_losses(field[0].losses + 1)
                field[0].calculate_rating()
                field[1].calculate_rating()
                self.leaderboard.append(field[0])
                self.leaderboard.append(field[1])

                def sort_rating(a: TournamentCard):
                    return a.rating
                self.leaderboard.sort(key=sort_rating, reverse=True)
                self.match_played += 1
                return {
                    "winner": field[0].id,
                    "loser": field[1].id,
                    "winner_rating": field[0].rating,
                    "loser_rating": field[1].rating
                }

    def get_leaderboard(self) -> List:
        clean_lb = []
        place = 1
        for player in self.leaderboard:
            report = f"{place}.  {player.name} - Rating: "
            report += f"{player.rating} ({player.wins}-{player.losses})"
            clean_lb.append(report)
        return clean_lb

    def generate_tournament_report(self) -> Dict:
        sum_score = sum([card.rating for card in self.leaderboard])
        return {
            "total_cards": len(self.registered),
            "matches_played": self.match_played,
            "avg_rating": sum_score/len(self.leaderboard),
            "platform_status": "active"
                }
