from sprites import Sprite, tile_size
from typing import Any
import pygame

top_offset = 120


class Pacgum(Sprite):
    def __init__(self, color: str, radius: int, score: int):
        super().__init__(color, radius)
        self.score = score
        self.eaten = False
        self.rad = radius
        self.radius = radius/2

    def ghost_move(self,
                   radius: int,
                   maze: list[list[int]],
                   old_maze: list[list[int]],
                   pacman: Any) -> None:
        pass


class SuperPacgum(Pacgum):
    def __init__(self, color: str, radius: int, score: int):
        super().__init__(color, radius, score)
        self.eaten = False
        self.rad = radius
        self.radius = radius/2


def pacgums_gen(maze_side: int,
                nb_of_pacgums: int,
                score_pacgums: int,
                score_super_pacgums: int,
                maze: list[list[int]],
                pacman_coord: tuple[int, int]) -> list[Pacgum]:

    pacman_pos_x, pacman_pos_y = pacman_coord
    pacgums_list: list[Pacgum] = [] 
    for y in range(1, maze_side + 1):
        for x in range(1, maze_side + 1):
            if ((x == 1 and y == 1) or
               (x == maze_side and y == 1) or
               (x == 1 and y == maze_side) or
               (x == maze_side and y == maze_side)):
                supercell = SuperPacgum('white', 10, score_super_pacgums)
                assert supercell.rect is not None
                supercell.rect.x = int(x * tile_size)
                supercell.rect.y = int(y * tile_size + top_offset)
                pacgums_list.append(supercell)
            elif x == pacman_pos_x and y == pacman_pos_y:
                pass
            elif maze[y][x] != 15:
                cell = Pacgum('yellow', 2, score_pacgums)
                assert cell.rect is not None
                cell.rect.x = int((x) * tile_size)
                cell.rect.y = int((y) * tile_size + top_offset)
                pacgums_list.append(cell)

    return pacgums_list
