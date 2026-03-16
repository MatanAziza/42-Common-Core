import pygame
from pygame import K_RIGHT, K_LEFT, K_UP, K_DOWN, K_a, K_w, K_s, K_d, Vector2
from utils import dec_to_bin
from random import randint
maze_side = 20
tile_size: float = 660/(maze_side+2)
window_h, window_w = 1280, 660


class Walls(pygame.sprite.Sprite):
    def __init__(self, sprite: str) -> None:
        super().__init__()
        self.image = pygame.Surface((int(tile_size), int(tile_size)))
        if 'north' in sprite:
            pygame.draw.line(self.image, 'navy', (0, 0), (tile_size-2, 0), 4)
        if 'south' in sprite:
            pygame.draw.line(self.image, 'navy', (0, tile_size-2),
                             (tile_size-2, tile_size-2), 4)
        if 'east' in sprite:
            pygame.draw.line(self.image, 'navy', (tile_size-2, 0),
                             (tile_size-2, tile_size-2), 4)
        if 'west' in sprite:
            pygame.draw.line(self.image, 'navy', (0, 0), (0, tile_size), 4)
        pygame.draw.circle(self.image, 'navy', (0, 0), 3)
        pygame.draw.circle(self.image, 'navy', (0, tile_size), 3)
        pygame.draw.circle(self.image, 'navy', (tile_size, 0), 3)
        pygame.draw.circle(self.image, 'navy', (tile_size, tile_size), 3)
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        self.rect = self.image.get_rect()


class Sprite(pygame.sprite.Sprite):
    def __init__(self, color: str, radius: float) -> None:
        super().__init__()
        self.image = pygame.Surface([tile_size, tile_size])
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        pygame.draw.circle(self.image, color,
                           (tile_size/2+1, tile_size/2+1), radius/2)
        self.rect = self.image.get_rect()


class Pacman(Sprite):
    def __init__(self,
                 color: str,
                 radius: float,
                 pos: Vector2,
                 cell: tuple[int, int], dt: int = 1) -> None:
        super().__init__(color, radius)
        self.color = color
        self.pos = cell
        self.rect.x = pos.x
        self.rect.y = pos.y
        self.can_change = True
        self.distance = 0
        self.direction = 1
        self.next_direction = 1
        self.dt = dt

    def player_move(self,
                    radius: int,
                    keys: list[bool], maze: list[list[int]]) -> None:
        x_axis = [0, 1, 0, -1]
        y_axis = [-1, 0, 1, 0]
        if self.distance >= tile_size and not self.can_change:
            self.distance = 0
            self.can_change = True
            self.pos = (self.pos[0]+x_axis[self.direction],
                        self.pos[1]+y_axis[self.direction])
        if self.pos[0] == 22 or self.pos[0] == -1:
            if self.pos[0] == 22:
                self.pos = (0, self.pos[1])
            else:
                self.pos = (21, self.pos[1])
            self.rect.x = 0 if self.pos[0] == 0 else window_w - tile_size
            self.image = pygame.Surface([tile_size, tile_size])
            self.image.set_colorkey('black')
            self.image.convert_alpha()
            pygame.draw.circle(self.image, self.color,
                               (tile_size/2+1, tile_size/2+1), radius/2)
        max_w = window_w - radius
        max_h = window_h - radius - 128
        if self.can_change:
            string = dec_to_bin(maze[self.pos[1]][self.pos[0]])
            walls = [int(x) for x in string]
            walls.reverse()
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
        elif (keys[pygame.K_a] or keys[K_LEFT]) and self.rect.x > 0:
            self.next_direction = 3
        elif (keys[pygame.K_w] or keys[K_UP]) and self.rect.y > 0:
            self.next_direction = 0
        elif (keys[pygame.K_s] or keys[K_DOWN]) and self.rect.y < max_h:
            self.next_direction = 2

    def tp_ltr(self, radius: float) -> None:
        self.image = pygame.Surface([tile_size+window_w, tile_size])
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (tile_size/2+1,
                                                    tile_size/2+1), radius/2)
        pygame.draw.circle(self.image, self.color, (tile_size/2+1+window_w,
                                                    tile_size/2+1), radius/2)
        self.is_tping = True

    def tp_rtl(self, radius: float) -> None:
        self.image = pygame.Surface([tile_size+window_w, tile_size])
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        self.rect.x = self.distance - tile_size
        pygame.draw.circle(self.image, self.color, (tile_size/2+1,
                                                    tile_size/2+1), radius/2)
        pygame.draw.circle(self.image, self.color, (tile_size/2+1 + window_w,
                                                    tile_size/2+1), radius/2)
        self.is_tping = True


class Ghost(Sprite):
    _ghosts: list[Sprite] = []

    def __init__(self,
                 color: str,
                 radius: float,
                 pos: Vector2,
                 cell: tuple[int, int],
                 dt: int = 1) -> None:
        super().__init__(color, radius)
        self.color = color
        self.rect.x = pos.x
        self.rect.y = pos.y
        self.pos = cell
        Ghost._ghosts.append(self)
        self.direction = -1
        self.can_change = True
        self.distance = 0
        self.dt = dt

    @classmethod
    def ghosts(cls) -> list[Sprite]:
        return cls._ghosts

    @classmethod
    def clear_ghosts(cls) -> None:
        cls._ghosts.clear()

    def ghost_move(self, radius: int, maze: list[list[int]]) -> None:
        if self.distance >= tile_size:
            self.distance = 0
            self.can_change = True
        if self.can_change:
            string = dec_to_bin(maze[self.pos[1]][self.pos[0]])
            walls = [int(x) for x in string]
            walls.reverse()
            self.cell = walls
            self.direction = randint(0, 3)
            while (walls[self.direction] == 1):
                self.direction = randint(0, 3)
            x_axis = [0, 1, 0, -1]
            y_axis = [-1, 0, 1, 0]
            self.pos = (self.pos[0]+x_axis[self.direction],
                        self.pos[1]+y_axis[self.direction])
            self.can_change = False
        move = self.direction
        max_w = window_w - radius
        max_h = window_h - radius - 128
        if move == 1 and self.rect.x < max_w and self.cell[1] == 0:
            self.rect.x += self.dt
        elif move == 3 and self.rect.x > 0 and self.cell[3] == 0:
            self.rect.x -= self.dt
        elif move == 2 and self.rect.y < max_h and self.cell[2] == 0:
            self.rect.y += self.dt
        elif move == 0 and self.rect.y > 0 and self.cell[0] == 0:
            self.rect.y -= self.dt
        self.distance += self.dt
