#!/usr/bin/env python3

class DataBase:
    """Database containing all players, achievements and their data,
    operations possible to do on them"""
    base = []
    scores_rank_values = {'high': 3, 'medium': 2, 'low': 1}
    achievements = {}

    @classmethod
    def add_achs(cls, achs: list):
        """Adds many achievements to the list of achievements"""
        cls.achievements = set(achs)

    @classmethod
    def get_player(cls, nametag):
        """Returns a player based on its nametag"""
        for player in cls.base:
            if nametag == player.player:
                return player

    """List comprehension"""
    @classmethod
    def get_scores_higher(cls, value):
        """returns list of player with higher score than value"""
        return [player.player for player in cls.base if player.score > value]

    @classmethod
    def mult_score(cls, mult):
        """returns a list of all players score multiplied by a value"""
        return [int(mult)*player.score for player in cls.base]

    @classmethod
    def active_players(cls):
        """returns a list of active players"""
        return [player.player for player in cls.base if player.active == 1]
    """Dict comprehension"""
    @classmethod
    def dict_all_players(cls):
        """returns a dict of players with their respective score"""
        return {player.player: player.score for player in cls.base}

    @classmethod
    def score_rank(cls):
        """returns the list of score rank value"""
        return cls.scores_rank_values

    @classmethod
    def players_achievents_count(cls):
        """returns a dict of players with their achievement count"""
        return {player.player: len(player.achievements) for player in cls.base}

    """Set comprehension"""
    @classmethod
    def unique_players(cls):
        """returns a set of unique players"""
        return {player.player for player in cls.base}

    @classmethod
    def unique_achs(cls):
        """Returns all achievements owned by 1 or less players"""
        count_achs = {ach: 0 for ach in cls.achievements}
        for p1 in cls.base:
            count_achs.update(
                {ach: count_achs.get(ach)+1 for ach in p1.achievements}
            )
        return {name for name, value in count_achs.items() if value <= 1}

    @classmethod
    def active_region(cls):
        """returns a set of regions of a player is active"""
        return {player.region for player in cls.base if player.active == 1}

    @classmethod
    def list_achievements(cls):
        """returns the total list of achievements"""
        return cls.achievements

    @classmethod
    def mvp(cls):
        """returns the current mvp"""
        for player, score in cls.dict_all_players().items():
            if score == max(cls.dict_all_players().values()):
                return [p for p in cls.base if p.player == player]

    class Player:
        """Player Class"""
        def __init__(self, player, score, lst, region):
            """Create a player's account with its gamertag, its owned
            achievements, and adding it to the player database"""
            self.player = player
            self.active = 1 if player[0].lower() <= 'c' else 0
            self.score = score
            self.region = region
            self.achievements = set(lst)
            DataBase.base.append(self)


if __name__ == "__main__":
    print("=== Game Analytics Dashboard ===\n")
    DataBase.add_achs([
                    "first_kill",
                    "level_10",
                    "treasure_hunter",
                    "cheater",
                    "speed_demon",
                    "boss_slayer",
                    "collector",
                    "perfectionist"
                    ])
    alice = DataBase.Player('Alice', 2300, [
                            "first_kill",
                            "level_10",
                            "treasure_hunter",
                            "speed_demon",
                            "cheater"
                            ],
                            'north')
    bob = DataBase.Player('Bob', 1800, [
                        "first_kill",
                        "level_10",
                        "boss_slayer",
                        "collector"
                        ],
                          'east')
    charlie = DataBase.Player('Charlie', 2150,  [
                                "level_10",
                                "treasure_hunter",
                                "speed_demon",
                                "boss_slayer",
                                "perfectionist"
                                ],
                              'central')
    diana = DataBase.Player('Diana', 2050, [
                        "first_kill",
                        "level_10"
                        ],
                            'south')
    print("===List Comprehension Examples ===")
    print(f"High scores (>2000): {DataBase.get_scores_higher(2000)}")
    print(f"Scores doubled: {DataBase.mult_score(2)}")
    print(f"Active players: {DataBase.active_players()}")
    print("\n=== Dict Comprehension Examples ===")
    print(f"Player score: {DataBase.dict_all_players()}")
    print(f"Score categories: {DataBase.score_rank()}")
    print(f"Achievement counts: {DataBase.players_achievents_count()}")
    print("\n=== Set Comprehension Examples ===")
    print(f"Unique players: {DataBase.unique_players()}")
    print(f"Unique achievements: {DataBase.unique_achs()}")
    print(f"Active regions: {DataBase.active_region()}")
    print("\n=== Combined Analysis ===")
    print(f"Total player: {len(DataBase.get_scores_higher(0))}")
    print(f"Total unique achievements: {len(DataBase.list_achievements())}")
    list_scores = DataBase.mult_score(1)
    print(f"Average score: {sum(list_scores)/len(list_scores)}")
    mvp = DataBase.mvp()[0]
    print(
        f"Top performer: {mvp.player} ({mvp.score} points"
        f", {DataBase.players_achievents_count().get(mvp.player)}"
        " achievements)"
    )
