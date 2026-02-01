#!/usr/bin/env python3

import time


class PlayerBase:
    """Store all players infos, and queue operations"""
    base = []
    queue = []
    total_ops = 0
    total_chests = 0
    total_lvlup = 0

    @classmethod
    def player_level_up(cls, nametag):
        """Level up a player"""
        for player in cls.base:
            if player.name == nametag:
                player.level = next(player.level_rank)
                print(f"Player {player.name} (level {player.level}) "
                      "leveled up")
                cls.total_lvlup += 1

    @classmethod
    def player_xp_up(cls, nametag, xp_value, insert):
        """Gives an amount of XP to a player"""
        for player in cls.base:
            if player.name == nametag:
                player.xp += xp_value
                print(f"Player {player.name} (level {player.level}) "
                      f"gained {xp_value} XP")
                while (player.xp >= 10):
                    cls.queue.insert(insert, ['LevelUp', nametag])
                    player.xp -= 10

    @classmethod
    def set_player_level(cls, nametag, target_level):
        """Set a player's level to a certain value"""
        for player in cls.base:
            if player.name == nametag:
                while (player.level < target_level):
                    player.level = next(player.level_rank)
                print(f"{nametag} is at level {player.level}")

    @classmethod
    def find_treasure(cls, nametag, chest):
        """gives a chest and its content to a player"""
        for player in cls.base:
            if player.name == nametag:
                print(
                    f"Player {nametag} (level {player.level})"
                    " found a Treasure Chest"
                    )
                for loot in chest:
                    player.inventory.update(loot)
                cls.total_chests += 1

    @classmethod
    def player_inventory(cls, nametag):
        """returns a player's inventory"""
        for player in cls.base:
            if player.name == nametag:
                player.get_inventory()

    @classmethod
    def monster_kill(cls, nametag, xp_value, insert):
        """kills a monster and give the xp to a player"""
        for player in cls.base:
            if player.name == nametag:
                print(
                    f"Player {nametag} (level {player.level})"
                    " killed a monster"
                    )
                cls.queue.insert(insert, ['XP_Up', nametag, xp_value])

    @classmethod
    def add_queue(cls, list_ops):
        """adds actions to the queue"""
        for elem in list_ops:
            cls.queue.append(elem)

    @classmethod
    def exec_queue(cls, nb_ops):
        """executes the queue for a number of ops"""
        print(f"\nProcessing {nb_ops} game events...\n")
        queue_list = iter(cls.queue)
        fina_ops = 0
        try:
            for i in range(nb_ops):
                print(f"Event {i+1}: ", end='')
                elem = next(queue_list)
                if elem[0] == 'NewAccount':
                    PlayerBase.Player(elem[1])
                elif elem[0] == 'LevelUp':
                    PlayerBase.player_level_up(elem[1])
                elif elem[0] == 'XP_Up':
                    PlayerBase.player_xp_up(elem[1], elem[2], i+1)
                elif elem[0] == 'SetPlayerXP':
                    PlayerBase.set_player_level(elem[1], elem[2])
                elif elem[0] == 'MonsterKill':
                    PlayerBase.monster_kill(elem[1], elem[2], i+1)
                elif elem[0] == 'TreasureFound':
                    PlayerBase.find_treasure(elem[1], elem[2])
                elif elem[0] == 'GetInventory':
                    PlayerBase.player_inventory(elem[1])
                cls.total_ops += 1
                fina_ops += 1
        except StopIteration:
            pass
        finally:
            for _ in range(fina_ops):
                cls.queue.pop(0)

    @classmethod
    def stream_stats(cls):
        """Gives all sorts of stats"""
        print("\n=== Stream Analytics ===")
        print(f"Total events processed: {cls.total_ops}")
        nb = 0
        nb += sum(1 for player in cls.base if player.level >= 10)
        print(f"High-level players (10+): {nb}")
        print(f"Treasure events: {cls.total_chests}")
        print(f"Level-up events: {cls.total_lvlup}")

    class Player:
        """Player class"""
        def __init__(self, name):
            """creates a player account"""
            self.name = name
            self.level = 0
            self.level_rank = (x for x in range(100))
            self.xp = 0
            self.inventory = dict({})
            PlayerBase.base.append(self)
            print(f"{name} player has created an account. Welcome!")

        def get_inventory(self):
            """prints a player inventory"""
            print(f"Player {self.name}'s inventory:")
            inv = self.inventory.items()
            for stuff in inv:
                print(f"- {stuff[0]} quantity: {stuff[1]}")


def fibonacci(nb_iter):
    """fibonacci showcase for a nbrs of elements"""
    a, b = 0, 1
    for _ in range(nb_iter):
        yield a
        c = a+b
        a = b
        b = c


def prime_numbers(nb_iter):
    """returns the next prime number"""
    a = 2
    for _ in range(nb_iter):
        divider = 2
        while (divider < a):
            if a % divider == 0:
                a += 1
                divider = 2
            else:
                divider += 1
        yield a
        a += 1


if __name__ == "__main__":
    start_time = time.time()
    print("=== Game Data Stream Processor ===")
    PlayerBase.add_queue([
                        ['NewAccount', 'Alice'],
                        ['NewAccount', 'Bob'],
                        ['NewAccount', 'Charlie'],
                        ['LevelUp', 'Charlie'],
                        ['MonsterKill', 'Alice', 5],
                        ['TreasureFound', 'Bob', [
                                                    {'boots': 1},
                                                    {'magic_ring': 2}
                                                    ]],
                        ['GetInventory', 'Bob'],
                        ['XP_Up', 'Alice', 15],
                        ['SetPlayerXP', 'Alice', 12]
                        ])
    PlayerBase.exec_queue(12)
    PlayerBase.stream_stats()
    print(f"\nTime elapsed: {round(time.time() - start_time, 4)} seconds")
    print("\n=== Generator Demonstration ===")
    a = fibonacci(10)
    print("Fibonacci Sequence: ", end='')
    for i in range(10):
        print(next(a), end='')
        if i < 9:
            print(", ", end='')
    b = prime_numbers(5)
    print("\nPrime Numbers: ", end='')
    for i in range(5):
        print(next(b), end='')
        if i < 4:
            print(", ", end='')
    print('\n')
