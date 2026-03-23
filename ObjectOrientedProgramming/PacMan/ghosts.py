from pygame import Vector2
from sprites import Ghost, Pacman
from djikstra import shortest_path
from utils import dec_to_bin
from typing import Any


class Blinky(Ghost):
    def __init__(self,
                 config: dict[str, Any],
                 color: str,
                 radius: float,
                 pos: Vector2,
                 cell: tuple[int, int],
                 target: tuple[int, int],
                 name: str) -> None:
        super().__init__(config, color, radius, pos, cell, target, name)
        self.last_dir = 0

    def where_to_go(self, pacman: Pacman,
                    old_maze: list[list[int]],
                    walls: list[int]) -> None:
        new_pos = pacman.player_pos()
        if not pacman.can_change and 0 < new_pos[0] <= len(old_maze):
            new_pos = pacman.player_target()
        if new_pos != self.target or not self.path:
            self.target = (new_pos[0]-1, new_pos[1]-1)
            if self.target[0] <= 0:
                self.target = (self.target[0]+1, self.target[1])
            if self.target[0] >= len(old_maze):
                self.target = (self.target[0]-1, self.target[1])
            self.path = shortest_path(old_maze,
                                      (self.pos[0]-1, self.pos[1]-1),
                                      self.target)
        if not self.path:
            self.path.append((self.last_dir+2) % 4)
        self.direction = self.path[0]
        self.last_dir = self.path[0]
        self.path.pop(0)


class Pinky(Ghost):
    def __init__(self,
                 config: dict[str, Any],
                 color: str,
                 radius: float,
                 pos: Vector2,
                 cell: tuple[int, int],
                 target: tuple[int, int],
                 name: str) -> None:
        super().__init__(config, color, radius, pos, cell, target, name)
        self.last_dir = 0

    def where_to_go(self, pacman: Pacman,
                    old_maze: list[list[int]],
                    walls: list[int]) -> None:
        new_pos = pacman.player_pos()
        p_dir = pacman.direction
        x_axis = [0, 1, 0, -1]
        y_axis = [-1, 0, 1, 0]
        radius = 0
        while radius < 2:
            if not (0 < new_pos[0] < len(old_maze) + 1 and
               0 < new_pos[1] < len(old_maze)):
                break
            cell = dec_to_bin(old_maze[new_pos[1]-1][new_pos[0]-1])
            if cell[p_dir] == 1:
                break
            radius += 1
            new_pos = (new_pos[0]+x_axis[p_dir], new_pos[1]+y_axis[p_dir])
        if new_pos != self.target or not self.path:
            self.target = (new_pos[0]-1, new_pos[1]-1)
            if self.target[0] <= 0:
                self.target = (self.target[0]+1, self.target[1])
            if self.target[0] >= len(old_maze):
                self.target = (self.target[0]-1, self.target[1])
            self.path = shortest_path(old_maze,
                                      (self.pos[0]-1, self.pos[1]-1),
                                      self.target)
        if not self.path:
            self.path.append((self.last_dir+2) % 4)
        self.direction = self.path[0]
        self.last_dir = self.path[0]
        self.path.pop(0)


class Clyde(Ghost):
    def __init__(self,
                 config: dict[str, Any],
                 color: str,
                 radius: float,
                 pos: Vector2,
                 cell: tuple[int, int],
                 target: tuple[int, int],
                 name: str) -> None:
        super().__init__(config, color, radius, pos, cell, target, name)
        self.last_dir = 0

    def where_to_go(self, pacman: Pacman,
                    old_maze: list[list[int]],
                    walls: list[int]) -> None:
        new_pos = pacman.player_pos()
        if not pacman.can_change and 0 < new_pos[0] <= len(old_maze):
            new_pos = pacman.player_target()
        elif (-2 <= self.pos[0]-new_pos[0] <= 2 and
              -2 <= self.pos[1]-new_pos[1] <= 2):
            new_pos = (1, len(old_maze)-1)
        if new_pos != self.target or not self.path:
            self.target = (new_pos[0]-1, new_pos[1]-1)
            if new_pos[0] <= 0:
                self.target = (self.target[0]+1, self.target[1])
            if new_pos[0] >= len(old_maze):
                self.target = (self.target[0]-1, self.target[1])
            self.path = shortest_path(old_maze,
                                      (self.pos[0]-1, self.pos[1]-1),
                                      self.target)
        if not self.path:
            self.path.append((self.last_dir+2) % 4)
        self.direction = self.path[0]
        self.last_dir = self.path[0]
        self.path.pop(0)
