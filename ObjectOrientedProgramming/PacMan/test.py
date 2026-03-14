import pygame
from pygame import Vector2
from random import randint
import time
from mazegenerator.mazegenerator import MazeGenerator
from manip_json import get_highscores, read_config, register_highscore

maze_width=15
maze_height=15
gen = MazeGenerator(size=(maze_width, maze_height),seed=42)
maze = gen.maze
pygame.init()
window_w, window_h = 64*len(maze), 64*len(maze[0])
screen = pygame.display.set_mode((window_w, window_h))
clock = pygame.time.Clock()
running, main_title, pause, game_over = True, True, False, False
dt = 2
radius = 64
player_pos = Vector2(32 * len(maze) - 32, 32 * len(maze[0]) - 32)
red_pos = Vector2(0, 0)
blue_pos = Vector2(window_w - radius , 0)
orange_pos = Vector2(0, window_h - radius)
pink_pos = Vector2(window_w - radius, window_h - radius)
tick = 60
walls_name = [
    'no_walls',
    'north',
    'east',
    'northeast',
    'south',
    'northsouth',
    'southeast',
    'northsoutheast',
    'west',
    'northwest',
    'eastwest',
    'northeastwest',
    'southwest',
    'northsouthwest',
    'southeastwest',
    'all'
]

start_time = time.time()

def dec_to_bin(cell: int) -> str:
    res = ''
    while cell > 0:
        res = str(cell%2)+res
        cell//=2
    while len(res) != 4:
        res = '0'+res
    return res

class Walls(pygame.sprite.Sprite):
    def __init__(self, sprite):
        super().__init__()
        self.image = pygame.image.load(f'sprites/{sprite}.png')
        self.image.set_colorkey('purple')
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, radius):
        super().__init__()
        self.image = pygame.Surface([radius, radius])
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        pygame.draw.circle(self.image, color, (radius/2, radius/2), radius/2)
        self.rect = self.image.get_rect()

class Pacman(Sprite):
    def __init__(self, color: str, radius: int, pos: Vector2):
        super().__init__(color, radius)
        self.color = color
        self.rect.x = pos.x
        self.rect.y = pos.y
        self.can_change = True
        self.distance = 0

    def player_move(self, radius: int, keys: list[bool]):
        if self.distance == 64:
            self.distance = 0
            self.can_change
        if self.can_change:
            up, down, left, right = False, False, False, False
            string = dec_to_bin(maze[int(self.rect.y//64)][int(self.rect.x//64)])
            walls = [int(x) for x in string]
            walls.reverse()
            self.cell = walls
            if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and self.rect.x < window_w - radius and self.cell[1] == 0:
                self.rect.x += dt
            elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and self.rect.x > 0 and self.cell[3] == 0:
                self.rect.x -= dt
            elif (keys[pygame.K_w] or keys[pygame.K_UP]) and self.rect.y > 0 and self.cell[0] == 0:
                self.rect.y -= dt
            elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and self.rect.y < window_h - radius and self.cell[2] == 0:
                self.rect.y += dt
        
        return Vector2(self.rect.x, self.rect.y)

class Ghost(Sprite):
    _ghosts = []

    def __init__(self, color: str, radius: int, pos: Vector2):
        super().__init__(color, radius)
        self.color = color
        self.rect.x = pos.x
        self.rect.y = pos.y
        Ghost._ghosts.append(self)
        self.direction = -1
        self.can_change = True
        self.distance = 0

    @classmethod
    def ghosts(cls):
        return cls._ghosts

    def ghost_move(self, radius: int):
        print(self.rect.x, self.rect.y, self.color)
        if self.distance == 64:
            self.distance = 0
            self.can_change = True
        if self.can_change:
            print(self.rect.x, self.rect.y, self.color)
            string = dec_to_bin(maze[int(self.rect.y//64)][int(self.rect.x//64)])
            walls = [int(x) for x in string]
            walls.reverse()
            self.cell = walls
            self.direction = randint(0, 3)
            while (walls[self.direction] == 1):
                self.direction = randint(0, 3)
            self.can_change = False
        move = self.direction
        if move == 1 and self.rect.x < window_w - radius and self.cell[1] == 0:
            self.rect.x += dt
        elif move == 3 and self.rect.x > 0 and self.cell[3] == 0:
            self.rect.x -= dt
        elif move == 2 and self.rect.y < window_h - radius and self.cell[2] == 0:
            self.rect.y += dt
        elif move == 0 and self.rect.y > 0 and self.cell[0] == 0:
            self.rect.y -= dt
        self.distance += dt

def quit(state: bool, running: bool) -> tuple[bool, bool]:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (False, False)
    return (state, running)

def back_to_title() -> tuple[bool, bool]:
    player_pos.x = 32*len(maze) - 32
    player_pos.y = 32*len(maze[0]) - 32
    red_pos.x = 0
    red_pos.y = 0
    blue_pos.x = window_w - radius
    blue_pos.y = 0
    orange_pos.x = 0
    orange_pos.y = window_h - radius
    pink_pos.x = window_w - radius
    pink_pos.y = window_h - radius
    return (False, True)

def maze_gen(maze: list[list[int]], walls_name: list[str]) -> list[Walls]:
    walls: list[Walls] = []
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            cell = Walls(walls_name[maze[y][x]])
            cell.rect.x = 64 * x
            cell.rect.y = 64 * y
            walls.append(cell)
    return walls


walls = maze_gen(maze, walls_name)
red_g = Ghost('red', radius, Vector2(0, 0))
blue_g = Ghost('blue', radius, Vector2(window_w - radius , 0))
orange_g = Ghost('orange', radius, Vector2(0, window_h - radius))
pink_g = Ghost('pink', radius, Vector2(window_w - radius, window_h - radius))

main_font = pygame.font.SysFont('Comic Sans MS', 100)
hs_font = pygame.font.SysFont('Comic Sans MS', 50)

mt_text = main_font.render('PAC-MAN', False, (255, 255, 0))
play_text = main_font.render('Press SPACE to play', False, (255, 255, 0))

pause_text = main_font.render('Pause', False, (255, 255, 255))
resume_text = hs_font.render('Press R to resume', False, (255, 255, 255))
back_text = hs_font.render('Press BACKSPACE to go back to main title', False, (255, 255, 255))

gameover_text = main_font.render('Game Over', False, (0, 0, 0))
gameover_score_text = main_font.render('Score:', False, (0, 0, 0))
gameover_restart_text = hs_font.render('Press R to restart', False, (0, 0, 0))

while running:
    
    if main_title:
        
        score = 0
        highscores = get_highscores('highscores.json')
        names = list(highscores.keys())
        scores = list(highscores.values())

        name_0 = hs_font.render(names[0], False, (0, 0, 0))
        name_1 = hs_font.render(names[1], False, (0, 0, 0))
        name_2 = hs_font.render(names[2], False, (0, 0, 0))
        name_3 = hs_font.render(names[3], False, (0, 0, 0))
        name_4 = hs_font.render(names[4], False, (0, 0, 0))
        name_5 = hs_font.render(names[5], False, (0, 0, 0))
        name_6 = hs_font.render(names[6], False, (0, 0, 0))
        name_7 = hs_font.render(names[7], False, (0, 0, 0))
        name_8 = hs_font.render(names[8], False, (0, 0, 0))
        name_9 = hs_font.render(names[9], False, (0, 0, 0))
        
        score_0 = hs_font.render(str(scores[0]), False, (0, 0, 0))
        score_1 = hs_font.render(str(scores[1]), False, (0, 0, 0))
        score_2 = hs_font.render(str(scores[2]), False, (0, 0, 0))
        score_3 = hs_font.render(str(scores[3]), False, (0, 0, 0))
        score_4 = hs_font.render(str(scores[4]), False, (0, 0, 0))
        score_5 = hs_font.render(str(scores[5]), False, (0, 0, 0))
        score_6 = hs_font.render(str(scores[6]), False, (0, 0, 0))
        score_7 = hs_font.render(str(scores[7]), False, (0, 0, 0))
        score_8 = hs_font.render(str(scores[8]), False, (0, 0, 0))
        score_9 = hs_font.render(str(scores[9]), False, (0, 0, 0))

    while main_title:

        main_title, running = quit(main_title, running)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            main_title = False

        screen.fill('blue')
        screen.blit(mt_text, (325 ,50))
        screen.blit(play_text, (150, 800))

        screen.blit(name_0, (100, 250))
        screen.blit(name_1, (100, 350))
        screen.blit(name_2, (100, 450))
        screen.blit(name_3, (100, 550))
        screen.blit(name_4, (100, 650))

        screen.blit(score_0, (300, 250))
        screen.blit(score_1, (300, 350))
        screen.blit(score_2, (300, 450))
        screen.blit(score_3, (300, 550))
        screen.blit(score_4, (300, 650))

        screen.blit(name_5, (600, 250))
        screen.blit(name_6, (600, 350))
        screen.blit(name_7, (600, 450))
        screen.blit(name_8, (600, 550))
        screen.blit(name_9, (600, 650))
 
        screen.blit(score_5, (800, 250))
        screen.blit(score_6, (800, 350))
        screen.blit(score_7, (800, 450))
        screen.blit(score_8, (800, 550))
        screen.blit(score_9, (800, 650))

        pygame.display.flip()
        clock.tick(tick)

    while pause:
        pause, running = quit(pause, running)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            pause = False
        elif keys[pygame.K_BACKSPACE]:
            pause, main_title = back_to_title()
        
        screen.fill('black')
        screen.blit(pause_text, (380, 100))
        screen.blit(resume_text, (325, 750))
        screen.blit(back_text, (125, 800))
        
        pygame.display.flip()
        clock.tick(tick)
    
    if game_over:
        score_text = main_font.render(str(score), False, (0, 0, 0))
    
    while game_over:
        game_over, running = quit(game_over, running)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over, main_title = back_to_title()
        
        screen.fill('red')
        screen.blit(gameover_text, (285, 100))
        screen.blit(gameover_score_text, (200, 300))
        screen.blit(score_text, (600, 300))
        screen.blit(gameover_restart_text, (335, 800))
        
        pygame.display.flip()
        clock.tick(tick)

    _, running = quit(True, running)

    sprites_list = pygame.sprite.Group()
    # Player
    pacman = Pacman('yellow', radius, player_pos)
    pacman.rect.x = player_pos.x
    pacman.rect.y = player_pos.y
    sprites_list.add(pacman)
    # Ghosts
    sprites_list.add(red_g)
    sprites_list.add(blue_g)
    sprites_list.add(orange_g)
    sprites_list.add(pink_g)

    for cell in walls:
        sprites_list.add(cell)
    sprites_list.update()

    screen.fill('purple')
    sprites_list.draw(screen)

    keys = pygame.key.get_pressed()
    player_pos = pacman.player_move(radius, keys)
    '''if (keys[pygame.K_w] or keys[pygame.K_UP]) and player_pos.y > 0:
        player_pos.y -= dt * 2
    elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player_pos.y < window_h - radius:
        player_pos.y += dt * 2
    elif (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_pos.x > 0:
        player_pos.x -= dt * 2
    elif (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_pos.x < window_w - radius:
        player_pos.x += dt * 2'''
    if keys[pygame.K_p]:
        pause = True

    actual_time = time.time()
    if actual_time - start_time >= 0.0125:
        for ghost in Ghost.ghosts():
            ghost.ghost_move(radius)
        start_time = time.time()

    ghosts = Ghost.ghosts()
    if pacman.rect.collidelist(ghosts) >= 0:
        game_over = True

    pygame.display.flip()
    clock.tick(tick)

pygame.quit()
