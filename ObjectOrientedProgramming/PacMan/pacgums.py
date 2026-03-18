from sprites import Sprite, maze_side, tile_size
from random import randint
import pygame
from pygame import Vector2
from typing import Any

top_offset = 120

class Pacgum(Sprite):
    def __init__(self, color: str, radius: int, score: int):
        super().__init__(color, radius)
        self.score = score

    def ghost_move(self,
                   radius: int,
                   maze: list[list[int]],
                   old_maze: list[list[int]],
                   pacman: Any) -> None:
        pass


class SuperPacgum(Sprite):
    def __init__(self, color: str, radius: int, score: int):
        super().__init__(color, radius)
        self.score = score

    def ghost_move(self,
                   radius: int,
                   maze: list[list[int]],
                   old_maze: list[list[int]],
                   pacman: Any) -> None:
        pass


def pacgums_gen(maze_side: int, nb_of_pacgums: int, score_pacgums: int, score_super_pacgums: int, maze: list[list[list[int]]]) -> list[Pacgum]:
    
    pacgums: list[list[str]] = []
    for y in range(maze_side):
        temp: list[bool] = []
        for x in range(maze_side):
            temp.append(False)
        pacgums.append(temp)

    actual_nb_of_pacgum = 0
    while actual_nb_of_pacgum < nb_of_pacgums:
        for y in range(1, len(pacgums)):
            for x in range(1, len(pacgums[0])):
                if ((x == 0 and y == 0) or
                    (x == maze_side - 1 and y == 0) or
                    (x == 0 and y == maze_side - 1) or
                    (x == maze_side - 1 and y == maze_side - 1) or
                    maze[y - 1][x - 1] == 15):
                    pass
                else:
                    is_pacgum = randint(0, 10)
                    if (is_pacgum == 1 and 
                        actual_nb_of_pacgum < nb_of_pacgums and
                        not pacgums[y][x]):
                        pacgums[y][x] = True
                        actual_nb_of_pacgum += 1

    pacgums_list: list[Pacgum] = []
    for y in range(len(pacgums)):
        for x in range(len(pacgums[0])):
            if ((x == 0 and y == 0) or
                (x == len(pacgums[0]) - 1 and y == 0) or
                (x == 0 and y == len(pacgums) - 1) or
                (x == len(pacgums[0]) - 1 and y == len(pacgums) - 1)):
                cell = SuperPacgum('white', 10, score_pacgums)
                cell.rect.x = int((x + 1) * tile_size)
                cell.rect.y = int((y + 1)* tile_size + top_offset)
                pacgums_list.append(cell)
            if pacgums[y][x] == True:
                cell = Pacgum('yellow', 2, score_pacgums)
                cell.rect.x = int((x + 1) * tile_size)
                cell.rect.y = int((y + 1)* tile_size + top_offset)
                pacgums_list.append(cell)
            else:
                cell = Pacgum('black', 2, 0)
                cell.rect.x = int((x + 1) * tile_size)
                cell.rect.y = int((y + 1) * tile_size + top_offset)
                pacgums_list.append(cell)

    return pacgums_list