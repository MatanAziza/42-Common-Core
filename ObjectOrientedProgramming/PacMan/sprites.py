from abc import ABC, abstractmethod
import pygame
from pygame import K_RIGHT, K_LEFT, K_UP, K_DOWN, K_a, K_w, K_s, K_d, Vector2
from pygame.key import ScancodeWrapper
from djikstra import shortest_path
from utils import dec_to_bin
from random import randint
from typing import Any


class Sprite(pygame.sprite.Sprite, ABC):
    "Sprite class"
    def __init__(self, config: dict[str, Any],
                 color: str,
                 radius: float) -> None:
        super().__init__()
        tile_size = config['tile_size']
        self.image = pygame.Surface([tile_size, tile_size])
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        pygame.draw.circle(self.image, color,
                           (tile_size/2+1, tile_size/2+1), radius/2)
        self.rect = self.image.get_rect()
        self.eatable: bool = False
        self.eaten: bool = False
        self.color = ''
        self.dt: int = 1
        self.path_changed: bool = False
        self.config = config

    @abstractmethod
    def ghost_move(self,
                   maze: list[list[int]],
                   old_maze: list[list[int]],
                   pacman: Any) -> None:
        "method determining where a ghost should go"
        pass

    def animate(self, config: dict[str, Any], timer: float) -> None:
        pass


class Walls(Sprite):
    def __init__(self, config: dict[str, Any], sprite: str) -> None:
        super().__init__(config, 'black', 0)
        tile_size = config['tile_size']
        self.image = pygame.Surface((int(tile_size), int(tile_size)))
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        if 'north' in sprite:
            pygame.draw.line(self.image, 'navy', (0, 0), (tile_size-2, 0), 4)
        if 'south' in sprite:
            pygame.draw.line(self.image, 'navy', (0, tile_size-2),
                             (tile_size-2, tile_size-2), 4)
        if 'east' in sprite:
            pygame.draw.line(self.image, 'navy', (tile_size-2, 0),
                             (tile_size-2, tile_size-2), 4)
        if 'west' in sprite:
            pygame.draw.line(self.image, 'navy', (0, 0), (0, tile_size-2), 4)
        pygame.draw.circle(self.image, 'navy', (0, 0), 3)
        pygame.draw.circle(self.image, 'navy', (0, tile_size), 3)
        pygame.draw.circle(self.image, 'navy', (tile_size, 0), 3)
        pygame.draw.circle(self.image, 'navy', (tile_size, tile_size), 3)
        self.rect = self.image.get_rect()

    def ghost_move(self,
                   maze: list[list[int]],
                   old_maze: list[list[int]],
                   pacman: Any) -> None:
        "method determining where a ghost should go. useless here"
        pass


class Pacman(Sprite):
    "Pacman class"
    def __init__(self,
                 config: dict[str, Any],
                 color: str,
                 radius: float,
                 pos: Vector2,
                 cell: tuple[int, int], dt: int = 2) -> None:
        super().__init__(config, color, 0)
        self.rad = radius
        self.radius = radius/2.5
        self.color = color
        self.pos = cell
        assert self.rect is not None
        self.rect.x = int(pos.x)
        self.rect.y = int(pos.y)
        self.can_change = True
        self.distance = 0
        self.direction = 1
        self.next_direction = 1
        self.dt = dt
        self.target = cell

    def init(self,
             color: str,
             radius: float,
             pos: Vector2,
             cell: tuple[int, int], dt: int = 2) -> None:
        "reproduces the __init__ method"
        self.rad = radius
        self.radius = radius/2.5
        self.color = color
        self.pos = cell
        assert self.rect is not None
        self.rect.x = int(pos.x)
        self.rect.y = int(pos.y)
        self.can_change = True
        self.distance = 0
        self.direction = 1
        self.next_direction = 1
        self.dt = dt
        self.target = cell

    def animate(self, config: dict[str, Any], timer: float) -> None:
        "changes the displayed sprite for a character to animate it"
        dir = ['up', 'right', 'down', 'left']
        tile_size = config['tile_size']
        f = 1 if self.distance % (tile_size/2) < tile_size/8 else 2
        f = f if self.distance % (tile_size/2) < tile_size/4 else 3
        f = f if self.distance % (tile_size/2) < 3*tile_size/8 else 4
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        name = f'{dir[self.direction]}_{f}'
        img = pygame.transform.scale(pygame.image.load(
            f'pacman/{name}.png'), (self.rad, self.rad))
        img.set_colorkey('black')
        img.convert_alpha()
        pygame.Surface.blit(self.image, img, (tile_size/2-self.rad/2,
                                              tile_size/2-self.rad/2))

    def player_pos(self) -> tuple[int, int]:
        "return the player position"
        return self.pos

    def ghost_move(self,
                   maze: list[list[int]],
                   old_maze: list[list[int]],
                   pacman: Any) -> None:
        "method determining where a ghost should go. useless here"
        pass

    def player_target(self) -> tuple[int, int]:
        "returns the player next position"
        x_axis = [0, 1, 0, -1]
        y_axis = [-1, 0, 1, 0]
        return (self.pos[0]+x_axis[self.direction],
                self.pos[1]+y_axis[self.direction])

    def player_move(self,
                    keys: ScancodeWrapper, maze: list[list[int]]) -> None:
        "Makes the player move depending on his position and the keys pressed"
        x_axis = [0, 1, 0, -1]
        y_axis = [-1, 0, 1, 0]
        tile_size = self.config['tile_size']
        config = self.config
        assert self.rect is not None
        if self.distance >= tile_size and not self.can_change:
            self.distance = 0
            self.can_change = True
            self.pos = (self.pos[0]+x_axis[self.direction],
                        self.pos[1]+y_axis[self.direction])
        if self.pos[0] in [config['side'][config['level']] + 2, -1]:
            if self.pos[0] == config['side'][config['level']]+2:
                self.pos = (0, self.pos[1])
            else:
                self.pos = (config['side'][config['level']]+1,
                            self.pos[1])
            assert self.rect is not None
            self.rect.x = 0 if self.pos[0] == 0 else int(660 - tile_size)
            self.image = pygame.Surface([tile_size, tile_size])
            self.image.set_colorkey('black')
            self.image.convert_alpha()
        max_w = 660 - self.rad
        max_h = 990 - self.rad - 128
        if self.can_change:
            self.rect.x = int(self.pos[0]*tile_size)
            self.rect.y = int(self.pos[1]*tile_size + 120)
            walls = dec_to_bin(maze[self.pos[1]][self.pos[0]])
            self.cell = walls
            moved = 0
            up, down = keys[K_w] or keys[K_UP], keys[K_s] or keys[K_DOWN]
            left, right = keys[K_a] or keys[K_LEFT], keys[K_d] or keys[K_RIGHT]
            if right and self.rect.x < max_w and self.cell[1] == 0:
                self.direction = 1
                moved = 1
            elif left and self.rect.x > 0 and self.cell[3] == 0:
                self.direction = 3
                moved = 1
            elif up and self.rect.y > 0 and self.cell[0] == 0:
                self.direction = 0
                moved = 1
            elif down and self.rect.y < max_h and self.cell[2] == 0:
                self.direction = 2
                moved = 1
            if self.cell[self.next_direction] == 0:
                moved = 1
                self.direction = self.next_direction
            if moved == 1 or not self.cell[self.direction]:
                self.can_change = False
        cant_move = not self.can_change
        if cant_move and self.direction >= 0 and not self.cell[self.direction]:
            if not self.cell[self.direction]:
                self.rect.x += self.dt*x_axis[self.direction]
            if not self.cell[self.direction]:
                self.rect.y += self.dt*y_axis[self.direction]
            self.distance += self.dt
        if (keys[pygame.K_d] or keys[K_RIGHT]) and self.rect.x < max_w:
            self.next_direction = 1
        elif (keys[pygame.K_a] or keys[K_LEFT]) and self.rect.x > -tile_size:
            self.next_direction = 3
        elif (keys[pygame.K_w] or keys[K_UP]) and self.rect.y > 0:
            self.next_direction = 0
        elif (keys[pygame.K_s] or keys[K_DOWN]) and self.rect.y < max_h:
            self.next_direction = 2

    def tp_ltr(self, radius: float) -> None:
        "teleports the player from left to right"
        tile_size = self.config['tile_size']
        self.image = pygame.Surface([tile_size+660, tile_size])
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (tile_size/2+1,
                                                    tile_size/2+1), radius/2)
        pygame.draw.circle(self.image, self.color, (tile_size/2+1+660,
                                                    tile_size/2+1), radius/2)
        self.is_tping = True

    def tp_rtl(self, radius: float) -> None:
        "teleports the player from right to left"
        assert self.rect is not None
        tile_size = self.config['tile_size']
        self.image = pygame.Surface([tile_size+660, tile_size])
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        self.rect.x = int(-tile_size)
        pygame.draw.circle(self.image, self.color, (tile_size/2+1,
                                                    tile_size/2+1), radius/2)
        pygame.draw.circle(self.image, self.color, (tile_size/2+1 + 660,
                                                    tile_size/2+1), radius/2)
        self.is_tping = True


class Ghost(Sprite):
    "Generic Ghost class"
    _ghosts: list[Sprite] = []

    def __init__(self,
                 config: dict[str, Any],
                 color: str,
                 radius: float,
                 pos: Vector2,
                 cell: tuple[int, int],
                 target: tuple[int, int],
                 name: str,
                 dt: int = 2) -> None:
        super().__init__(config, 'black', radius)
        assert self.rect is not None
        self.rad = radius
        self.radius = radius/2.1
        self.name = name
        img = pygame.transform.scale(
            pygame.image.load(f'ghosts/{name}_left_1.png'),
            (radius, radius))
        img.set_colorkey('black')
        img.convert_alpha()
        self.color = color
        self.rect.x = int(pos.x)
        self.rect.y = int(pos.y)
        pygame.Surface.blit(self.image,
                            img,
                            (config['tile_size']/2-self.rad/2,
                             config['tile_size']/2-self.rad/2))
        self.pos = cell
        self.direction = -1
        assert self.image is not None
        self.mask = pygame.mask.from_threshold(self.image,
                                               pygame.Color('yellow'),
                                               (1, 1, 1, 255))
        self.can_change = True
        self.distance = 0
        self.dt = config['dt'][config['level']]
        self.target = (target[0]-1, target[1]-1)
        self.current_target = self.target
        self.path: list[int] = []
        self.eatable = False
        self.eaten = False
        self.path_changed = False
        Ghost._ghosts.append(self)

    def init(self,
             color: str,
             radius: float,
             pos: Vector2,
             cell: tuple[int, int],
             target: tuple[int, int],
             name: str,
             dt: int = 2) -> None:
        "reproduces the __init__ method"
        assert self.rect is not None
        self.rad = radius
        self.radius = radius/2.1
        config = self.config
        self.name = name
        img = pygame.transform.scale(
            pygame.image.load(f'ghosts/{name}_left_1.png'),
            (radius, radius))
        img.set_colorkey('black')
        img.convert_alpha()
        self.color = color
        self.rect.x = int(pos.x)
        self.rect.y = int(pos.y)
        pygame.Surface.blit(self.image,
                            img,
                            (config['tile_size']/2-self.rad/2,
                             config['tile_size']/2-self.rad/2))
        self.pos = cell
        self.direction = -1
        assert self.image is not None
        self.mask = pygame.mask.from_threshold(self.image,
                                               pygame.Color('yellow'),
                                               (1, 1, 1, 255))
        self.can_change = True
        self.distance = 0
        self.dt = dt
        self.target = (target[0]-1, target[1]-1)
        self.current_target = self.target
        self.eatable = False
        self.eaten = False
        self.path_changed = False
        self.last_dir = 0

    def animate(self, config: dict[str, Any], timer: float) -> None:
        "changes the displayed sprite for a character to animate it"
        dir = ['up', 'right', 'down', 'left']
        tile_size = self.config['tile_size']
        f = 1 if self.distance % (tile_size/4) < tile_size/8 else 2
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        name = f'{self.name}_{dir[self.direction]}_{f}'
        if self.eatable and not self.eaten and timer >= 7:
            f = 1 if self.distance % (tile_size/2) < tile_size/8 else 2
            f = f if self.distance % (tile_size/2) < tile_size/4 else 3
            f = f if self.distance % (tile_size/2) < 3*tile_size/8 else 4
        if self.eatable and not self.eaten:
            name = f'eatable_{f}'
        elif self.eatable and self.eaten:
            name = f'eyes_{dir[self.direction]}'
        img = pygame.transform.scale(pygame.image.load(
            f'ghosts/{name}.png'),
                                     (self.rad, self.rad))
        img.set_colorkey('black')
        img.convert_alpha()
        pygame.Surface.blit(self.image, img, (tile_size/2-self.rad/2,
                                              tile_size/2-self.rad/2))

    @classmethod
    def ghosts(cls) -> list[Sprite]:
        "returns a list of existing ghosts"
        return cls._ghosts

    @classmethod
    def clear_ghosts(cls) -> None:
        "clears the list of existing ghosts"
        cls._ghosts.clear()

    def ghost_move(self,
                   maze: list[list[int]],
                   old_maze: list[list[int]],
                   pacman: Pacman) -> None:
        """method determining where a ghost should go and how he moves
        according to his corodinates and pixel position"""
        assert self.rect is not None
        config = self.config
        tile_size = config['tile_size']
        if self.distance >= tile_size:
            self.distance = 0
            self.can_change = True
        if self.can_change:
            self.rect.x = int(self.pos[0]*tile_size)
            self.rect.y = int(self.pos[1]*tile_size + 120)
            walls = dec_to_bin(old_maze[self.pos[1]-1][self.pos[0]-1])
            self.cell = walls
            if self.eatable:
                self.flee(old_maze)
            else:
                self.where_to_go(pacman, old_maze, walls)
            x_axis = [0, 1, 0, -1]
            y_axis = [-1, 0, 1, 0]
            if self.direction != -1:
                self.pos = (self.pos[0]+x_axis[self.direction],
                            self.pos[1]+y_axis[self.direction])
            self.can_change = False
        move = self.direction
        max_w = 660 - self.rad
        max_h = 990 - self.rad - 128
        if move == 1 and self.rect.x < max_w and self.cell[1] == 0:
            self.rect.x += self.dt
        elif move == 3 and self.rect.x > 0 and self.cell[3] == 0:
            self.rect.x -= self.dt
        elif move == 2 and self.rect.y < max_h and self.cell[2] == 0:
            self.rect.y += self.dt
        elif move == 0 and self.rect.y > 0 and self.cell[0] == 0:
            self.rect.y -= self.dt
        self.distance += self.dt

    def where_to_go(self, pacman: Pacman,
                    old_maze: list[list[int]],
                    walls: list[int]) -> None:
        "choses randomly a direction the ghost has to take (obsolete)"
        assert self.rect is not None
        self.direction = randint(0, 3)
        while (walls[self.direction] == 1):
            self.direction = randint(0, 3)

    def flee(self, maze: list[list[int]]) -> None:
        "manage the flee state f all ghosts"
        scatter = {'red': (0, 1),
                   'cyan': (len(maze)-1, 1),
                   'orange': (0, len(maze)-2),
                   'pink': (len(maze)-1, len(maze)-2)}
        if self.eatable and not self.path_changed:
            self.path = shortest_path(maze, (self.pos[0]-1, self.pos[1]-1),
                                      scatter[self.color])
            self.path_changed = True
        self.direction = self.path[0] if self.path else -1
        self.path.pop(0) if self.path else 0
        self.last_dir = self.path[0]
