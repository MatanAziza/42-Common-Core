from sprites import Sprite
from typing import Any


class Pacgum(Sprite):
    'A class for creating pacgums. Inherit from Sprite'
    def __init__(self,
                 config: dict[str, Any],
                 color: str,
                 radius: int,
                 score: int):
        super().__init__(config, color, radius)
        self.score = score
        self.eaten = False
        self.rad = radius
        self.radius = radius/2

    def ghost_move(self,
                   maze: list[list[int]],
                   old_maze: list[list[int]],
                   pacman: Any) -> None:
        pass


class SuperPacgum(Pacgum):
    'A class to create super pacgums. Inherit from Pacgum'
    def __init__(self,
                 config: dict[str, Any],
                 color: str,
                 radius: int,
                 score: int):
        super().__init__(config, color, radius, score)
        self.eaten = False
        self.rad = radius
        self.radius = radius/2


def pacgums_gen(config: dict[str, Any],
                maze_side: int,
                score_pacgums: int,
                score_super_pacgums: int,
                maze: list[list[int]],
                pacman_coord: tuple[int, int],
                top_offset: int,
                walls_name: list[str]) -> list[Pacgum]:

    '''Generate of list of Pacgum and SuperPacgum sprites
    We fill the corner with super pacgums then we fill
    then we fill the rest of the cells (except th one pacman
    spawns in) then we generate the ones between cells'''
    pacman_pos_x, pacman_pos_y = pacman_coord
    tile_size = config['tile_size']
    pacgums_list: list[Pacgum] = []

    for y in range(1, maze_side + 1):
        for x in range(1, maze_side + 1):
            if ((x == 1 and y == 1) or
               (x == maze_side and y == 1) or
               (x == 1 and y == maze_side) or
               (x == maze_side and y == maze_side)):
                supercell = SuperPacgum(config,
                                        'white',
                                        10,
                                        score_super_pacgums)
                assert supercell.rect is not None
                supercell.rect.x = int(x * tile_size)
                supercell.rect.y = int(y * tile_size + top_offset)
                pacgums_list.append(supercell)

            elif x == pacman_pos_x and y == pacman_pos_y:
                pass
            elif maze[y][x] != 15:
                cell = Pacgum(config, 'yellow', 2, score_pacgums)
                assert cell.rect is not None
                cell.rect.x = int((x) * tile_size)
                cell.rect.y = int((y) * tile_size + top_offset)
                pacgums_list.append(cell)

            wall = walls_name[maze[y][x]]
            if 'south' not in wall:
                cell = Pacgum(config, 'yellow', 2, score_pacgums)
                assert cell.rect is not None
                cell.rect.x = int((x) * tile_size)
                cell.rect.y = int((y) *
                                  tile_size +
                                  top_offset +
                                  (tile_size / 2))
                pacgums_list.append(cell)
            if 'east' not in wall and x < maze_side:
                cell = Pacgum(config, 'yellow', 2, score_pacgums)
                assert cell.rect is not None
                cell.rect.x = int((x) * tile_size + (tile_size / 2))
                cell.rect.y = int((y) * tile_size + top_offset)
                pacgums_list.append(cell)

    return pacgums_list
