#!/usr/bin/env python3

class DataBase:
    """Database of players autoupdating when a player creates an account.
        Allows to track players achievement and to compare one to another,
        as well as getting general stats
    """
    base = []
    achievements = set()

    @classmethod
    def add_ach(cls, ach):
        """Adds an achievement to the list of achievements"""
        cls.achievements.add(ach)

    @classmethod
    def add_achs(cls, achs: list):
        """Adds many achievements to the list of achievements"""
        for elem in achs:
            cls.achievements.add(elem)

    @classmethod
    def list_ach(cls):
        """Returns the current list of achievene"""
        return cls.achievements

    @classmethod
    def update_base(cls, player):
        """Adds a player to the database"""
        cls.base.append(player)

    @classmethod
    def players_achievements(cls):
        """Prints the list of achievement obtained by a player"""
        for player in cls.base:
            print(
                f"Player {player.player} achievements: "
                f"{player.achievements}"
                )

    @classmethod
    def get_player(cls, nametag):
        """Returns a player based on its nametag"""
        for player in cls.base:
            if nametag == player.player:
                return player
        print("Player Not Found")
        return None

    @staticmethod
    def common_achs(player1, player2):
        """Returns commons achievements between two players"""
        return player1.achievements.intersection(player2.achievements)

    @classmethod
    def common_all(cls):
        """Returns all achievements owned by all the players"""
        l2 = cls.base[0].achievements
        l1 = None
        for player in cls.base[1:]:
            l1 = l2
            l2 = l1.intersection(player.achievements)
        return (l2)

    @classmethod
    def rare_achievements(cls):
        """Returns a set of achievement owned by only one player or less"""
        rare = []
        for achievement in cls.achievements:
            count = 0
            for player in cls.base:
                for ach in player.achievements:
                    if ach == achievement:
                        count += 1
            if count <= 1:
                rare.append(achievement)
        return (set(rare))

    @classmethod
    def unique_achs(cls, p1):
        """Returns all unique achievements a player has"""
        achs = p1.achievements
        for p2 in cls.base:
            if p1.player != p2.player:
                achs = achs.difference(p2.achievements)
        return achs

    class Player:
        """Player Class"""

        def __init__(self, player, lst):
            """Create a player's account with its gamertag, its owned
            achievements, and adding it to the player database"""
            self.player = player
            self.achievements = set(lst)
            DataBase.update_base(self)


if __name__ == "__main__":
    print("=== Achievement Tracker System ===\n")
    DataBase.add_achs([
                    "first_kill",
                    "level_10",
                    "treasure_hunter",
                    "cheater",
                    "speed_demon",
                    "first_kill",
                    "boss_slayer",
                    "collector",
                    "perfectionist"
                    ])
    alice = DataBase.Player("Alice", [
                            "first_kill",
                            "level_10",
                            "treasure_hunter",
                            "speed_demon",
                            "cheater"
                            ])
    bob = DataBase.Player("Bob", [
                        "first_kill",
                        "level_10",
                        "boss_slayer",
                        "collector"
                        ])
    charlie = DataBase.Player("Charlie", [
                                "level_10",
                                "treasure_hunter",
                                "speed_demon",
                                "boss_slayer",
                                "perfectionist"
                                ])
    DataBase.players_achievements()
    print("\n=== Achievement Analytics ===\n")
    set_achs = DataBase.list_ach()
    print(f"All unique achievement: {set_achs}")
    print(f"Total unique achievements: {len(set_achs)}\n")
    print(f"Common to all players: {DataBase.common_all()}")
    print(f"Rare achievements: {DataBase.rare_achievements()}\n")
    p1 = DataBase.get_player("Alice")
    p2 = DataBase.get_player("Bob")
    print(f"{p1.player} vs {p2.player} common: {DataBase.common_achs(p1, p2)}")
    print(f"{p1.player} unique: {DataBase.unique_achs(p1)}")
    print(f"{p2.player} unique: {DataBase.unique_achs(p2)}")
