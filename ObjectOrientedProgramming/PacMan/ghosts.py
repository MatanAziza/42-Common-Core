from pygame import Vector2
from sprites import Ghost, Pacman
from djikstra import shortest_path

class Blinky(Ghost):
    def __init__(self,
                 color: str,
                 radius: float,
                 pos: Vector2,
                 cell: tuple[int, int],
                 target: tuple[int, int],
                 dt: int = 1) -> None:
        super().__init__(color, radius, pos, cell, target, dt)
        self.last_dir = 0

    def where_to_go(self, pacman: Pacman,
                    old_maze: list[list[int]],
                    walls: list[int]) -> None:
        new_pos = pacman.player_pos()
        if not pacman.can_change and 0 < new_pos[0] <= len(old_maze):
            new_pos = pacman.player_target()
        else:
        if new_pos != self.target or not self.path:
            self.target = (new_pos[0]-1, new_pos[1]-1)
            if new_pos[0] <= 0:
                self.target = (self.target[0]+1, self.target[1])
            if new_pos[0] > len(old_maze):
                self.target = (self.target[0]-1, self.target[1])
            self.path = shortest_path(old_maze,
                                        (self.pos[0]-1, self.pos[1]-1),
                                        self.target)
        if not self.path:
            if self.target[0] in [0, 1, len(old_maze)-1, len(old_maze)]:
                self.path.append(self.last_dir%4)
            elif self.target == (self.pos[0]-1, self.pos[1]-1):
                self.path.append((self.last_dir+2)%4)
        self.direction = self.path[0]
        self.last_dir = self.path[0]+2
        self.path.pop(0)
