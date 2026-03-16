import pygame
from utils import dec_to_bin
from random import randint
from pygame import Vector2
maze_side = 15
tile_size: int = 660/(maze_side+2)
window_h, window_w = 1280, 660

class Walls(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__()
        # self.image = pygame.image.load(f'sprites/{sprite}.png')
        # self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.image = pygame.Surface((int(tile_size), int(tile_size)))
        if 'north' in sprite:
            pygame.draw.line(self.image, 'navy', (0, 0), (tile_size-2, 0), 4)
        if 'south' in sprite:
            pygame.draw.line(self.image, 'navy', (0, tile_size-2), (tile_size-2, tile_size-2), 4)
        if 'east' in sprite:
            pygame.draw.line(self.image, 'navy', (tile_size-2, 0), (tile_size-2, tile_size-2), 4)
        if 'west' in sprite:
            pygame.draw.line(self.image, 'navy', (0, 0), (0, tile_size), 4)
        pygame.draw.circle(self.image, 'navy', (0, 0), 3)
        pygame.draw.circle(self.image, 'navy', (0, tile_size), 3)
        pygame.draw.circle(self.image, 'navy', (tile_size, 0), 3)
        pygame.draw.circle(self.image, 'navy', (tile_size, tile_size), 3)
        self.image.set_colorkey('purple')
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, radius):
        super().__init__()
        self.image = pygame.Surface([tile_size, tile_size])
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        pygame.draw.circle(self.image, color, (tile_size/2+1, tile_size/2+1), radius/2)
        self.rect = self.image.get_rect()

class Pacman(Sprite):
    def __init__(self, color: str, radius: int, pos: Vector2, cell: tuple[int, int], dt: int = 1):
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

    def player_move(self, radius: int, keys: list[bool], maze: list[list[int]]):
        x_axis = [0, 1, 0, -1]
        y_axis = [-1, 0, 1, 0]
        if self.distance >= tile_size and not self.can_change:
            self.distance = 0
            self.can_change = True
            self.pos = (self.pos[0]+x_axis[self.direction], self.pos[1]+y_axis[self.direction])
        if self.can_change:
            string = dec_to_bin(maze[self.pos[1]][self.pos[0]])
            walls = [int(x) for x in string]
            walls.reverse()
            self.cell = walls
            moved = 0
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.x < window_w - radius and self.cell[1] == 0:
                self.direction = 1
                moved = 1
            elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.x > 0 and self.cell[3] == 0:
                self.direction = 3
                moved = 1
            elif (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.y > 0 and self.cell[0] == 0:
                self.direction = 0
                moved = 1
            elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.y < window_h - radius - 128 and self.cell[2] == 0:
                self.direction = 2
                moved = 1
            if self.cell[self.next_direction] == 0:
                moved = 1
                self.direction = self.next_direction
            if moved == 1 or not self.cell[self.direction]:
                self.can_change = False
        if not self.can_change and self.direction >= 0 and not self.cell[self.direction]:
            self.rect.x += self.dt*x_axis[self.direction] if not self.cell[self.direction] else 0
            self.rect.y += self.dt*y_axis[self.direction] if not self.cell[self.direction] else 0
            self.distance += self.dt
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.x < window_w - radius:
            self.next_direction = 1
        elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.x > 0:
            self.next_direction = 3
        elif (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.y > 0:
            self.next_direction = 0
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.y < window_h - radius - 128:
            self.next_direction = 2
        return Vector2(self.rect.x, self.rect.y)

class Ghost(Sprite):
    _ghosts = []

    def __init__(self, color: str, radius: int, pos: Vector2, cell: tuple[int, int], dt: int = 1):
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
    def ghosts(cls):
        return cls._ghosts

    @classmethod
    def clear_ghosts(cls):
        cls._ghosts.clear()

    def ghost_move(self, radius: int, maze: list[list[int]]):
        if self.distance >= tile_size:
            self.distance = 0
            self.can_change = True
        if self.can_change:
            string = dec_to_bin(maze[self.pos[1]][self.pos[0]])
            walls = [int(x) for x in string]
            walls.reverse()
            print(walls, self.pos[0], self.pos[1]) if self.color == 'red' else 0
            self.cell = walls
            self.direction = randint(0, 3)
            while (walls[self.direction] == 1):
                self.direction = randint(0, 3)
            print(self.direction) if self.color == 'red' else 0
            x_axis = [0, 1, 0, -1]
            y_axis = [-1, 0, 1, 0]
            self.pos = (self.pos[0]+x_axis[self.direction], self.pos[1]+y_axis[self.direction])
            self.can_change = False
        move = self.direction
        if move == 1 and self.rect.x < window_w - radius and self.cell[1] == 0:
            self.rect.x += self.dt
        elif move == 3 and self.rect.x > 0 and self.cell[3] == 0:
            self.rect.x -= self.dt
        elif move == 2 and self.rect.y < window_h - radius - 128 and self.cell[2] == 0:
            self.rect.y += self.dt
        elif move == 0 and self.rect.y > 0 and self.cell[0] == 0:
            self.rect.y -= self.dt
        self.distance += self.dt

