import pygame
from pygame import Vector2
from random import randint
import time
from mazegenerator.mazegenerator import MazeGenerator
from manip_json import get_highscores, read_config, register_highscore
# 6, 8/, 10, 11, 12, 15, 16//, 20, 22, 24/, 25/, 30, 33, 44: 660 divisible by these
config = read_config('config.json')
maze_side=12
pygame.init()
gen = MazeGenerator(size=(maze_side, maze_side),seed=42)
maze = gen.maze
window_w, window_h = 660, 990
screen = pygame.display.set_mode((window_w, window_h))
clock = pygame.time.Clock()
running, main_title, pause, game_over = True, True, False, False
dt = 1
radius = 480/maze_side
tile_size = 660/maze_side
player_pos = Vector2((maze_side//2)*tile_size, (maze_side//2)*tile_size + 180)
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
    'northsoutheastwest'
]

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
        # self.image = pygame.image.load(f'sprites/{sprite}.png')
        # self.image = pygame.transform.scale(self.image, (tile_size, tile_size))
        self.image = pygame.Surface((int(tile_size), int(tile_size)))
        if 'north' in sprite:
            pygame.draw.line(self.image, 'white', (0, 0), (tile_size-2, 0), 2)
        if 'south' in sprite:
            pygame.draw.line(self.image, 'white', (0, tile_size-2), (tile_size-2, tile_size-2), 2)
        if 'east' in sprite:
            pygame.draw.line(self.image, 'white', (tile_size-2, 0), (tile_size-2, tile_size-2), 2)
        if 'west' in sprite:
            pygame.draw.line(self.image, 'white', (0, 0), (0, tile_size), 2)
        pygame.draw.circle(self.image, 'white', (0, 0), 2)
        pygame.draw.circle(self.image, 'white', (0, tile_size), 2)
        pygame.draw.circle(self.image, 'white', (tile_size, 0), 2)
        pygame.draw.circle(self.image, 'white', (tile_size, tile_size), 2)
        self.image.set_colorkey('purple')
        self.image.convert_alpha()
        self.rect = self.image.get_rect()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, radius):
        super().__init__()
        self.image = pygame.Surface([tile_size, tile_size])
        self.image.set_colorkey('black')
        self.image.convert_alpha()
        pygame.draw.circle(self.image, color, (tile_size/2, tile_size/2), radius/2)
        self.rect = self.image.get_rect()

class Pacman(Sprite):
    def __init__(self, color: str, radius: int, pos: Vector2, cell: tuple[int, int]):
        super().__init__(color, radius)
        self.color = color
        self.pos = cell
        self.rect.x = pos.x
        self.rect.y = pos.y
        self.can_change = True
        self.distance = 0
        self.direction=0
        self.next_direction = 0

    def player_move(self, radius: int, keys: list[bool]):
        x_axis = [0, 1, 0, -1]
        y_axis = [-1, 0, 1, 0]
        if self.distance == tile_size and not self.can_change:
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
            self.rect.x += dt*x_axis[self.direction] if not self.cell[self.direction] else 0
            self.rect.y += dt*y_axis[self.direction] if not self.cell[self.direction] else 0
            self.distance += dt
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

    def __init__(self, color: str, radius: int, pos: Vector2, cell: tuple[int, int]):
        super().__init__(color, radius)
        self.color = color
        self.rect.x = pos.x
        self.rect.y = pos.y
        self.pos = cell
        Ghost._ghosts.append(self)
        self.direction = -1
        self.can_change = True
        self.distance = 0

    @classmethod
    def ghosts(cls):
        return cls._ghosts

    def ghost_move(self, radius: int):
        if self.distance == tile_size:
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
            self.pos = (self.pos[0]+x_axis[self.direction], self.pos[1]+y_axis[self.direction])
            self.can_change = False
        move = self.direction
        if move == 1 and self.rect.x < window_w - radius and self.cell[1] == 0:
            self.rect.x += dt
        elif move == 3 and self.rect.x > 0 and self.cell[3] == 0:
            self.rect.x -= dt
        elif move == 2 and self.rect.y < window_h - radius - 128 and self.cell[2] == 0:
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
    pacman.__init__('yellow', radius, player_pos, (int(maze_side//2), int(maze_side//2)))
    red_g.__init__('red', radius, Vector2(0, 180), (0, 0))
    blue_g.__init__('blue', radius, Vector2(window_w - tile_size , 180), (maze_side-1, 0))
    orange_g.__init__('orange', radius, Vector2(0, 180+(maze_side-1)*tile_size), (0, maze_side-1))
    pink_g.__init__('pink', radius, Vector2(window_w - tile_size, 180+(maze_side-1)*tile_size), (maze_side-1, maze_side-1))
    # red_g.rect.x, red_g.rect.y = 0, 180
    # red_g.distance, red_g.pos = 0, (0, 0)
    # blue_g.__init__('blue', radius, Vector2(window_w - tile_size, 180), (0, 0))
    # blue_g.rect.x, blue_g.rect.y = window_w - tile_size , 180
    # blue_g.distance, blue_g.pos = 0, (maze_side-1, 0)
    # orange_g.rect.x, orange_g.rect.y = 0, 180+(maze_side-1)*tile_size
    # orange_g.distance, orange_g.pos = 0, (0, maze_side-1)
    # pink_g.rect.x = window_w - tile_size
    # pink_g.rect.y = 180+(maze_side-1)*tile_size
    # pink_g.distance, pink_g.pos = 0, (maze_side-1, maze_side-1)

    return (False, True)

def reset() -> None:
    pacman.__init__('yellow', radius, player_pos, (int(maze_side//2), int(maze_side//2)))
    red_g.__init__('red', radius, Vector2(0, 180), (0, 0))
    blue_g.__init__('blue', radius, Vector2(window_w - tile_size , 180), (maze_side-1, 0))
    orange_g.__init__('orange', radius, Vector2(0, 180+(maze_side-1)*tile_size), (0, maze_side-1))
    pink_g.__init__('pink', radius, Vector2(window_w - tile_size, 180+(maze_side-1)*tile_size), (maze_side-1, maze_side-1))
    # red_g.rect.x, red_g.rect.y = 0, 180
    # red_g.distance, red_g.pos = 0, (0, 0)
    # blue_g.rect.x, blue_g.rect.y = window_w - tile_size , 180
    # blue_g.distance, blue_g.pos = 0, (maze_side-1, 0)
    # orange_g.rect.x, orange_g.rect.y = 0, 180+(maze_side-1)*tile_size
    # orange_g.distance, orange_g.pos = 0, (0, maze_side-1)
    # pink_g.rect.x = window_w - tile_size
    # pink_g.rect.y = 180+(maze_side-1)*tile_size
    # pink_g.distance, pink_g.pos = 0, (maze_side-1, maze_side-1)

def maze_gen(maze: list[list[int]], walls_name: list[str]) -> list[Walls]:
    walls: list[Walls] = []
    for y in range(maze_side):
        for x in range(maze_side):
            cell = Walls(walls_name[maze[y][x]])
            cell.rect.x = x * (tile_size)
            cell.rect.y = y * (tile_size) + 180
            walls.append(cell)
    return walls


walls = maze_gen(maze, walls_name)
pacman = Pacman('yellow', radius, player_pos, (int(maze_side//2), int(maze_side//2)))
red_g = Ghost('red', radius, Vector2(0, 180), (0, 0))
blue_g = Ghost('blue', radius, Vector2(window_w - tile_size , 180), (maze_side-1, 0))
orange_g = Ghost('orange', radius, Vector2(0, 180+(maze_side-1)*tile_size), (0, maze_side-1))
pink_g = Ghost('pink', radius, Vector2(window_w - tile_size, 180+(maze_side-1)*tile_size), (maze_side-1, maze_side-1))

main_font = pygame.font.SysFont('Comic Sans MS', 100)
reduced_font = pygame.font.SysFont('Comic Sans MS', 50)

mt_text = main_font.render('PAC-MAN', False, (255, 255, 0))
play_text = main_font.render('Press SPACE to play', False, (255, 255, 0))

pause_text = main_font.render('Pause', False, (255, 255, 255))
resume_text = reduced_font.render('Press R to resume', False, (255, 255, 255))
back_text = reduced_font.render('Press BACKSPACE to go back to main title', False, (255, 255, 255))

gameover_text = main_font.render('Game Over', False, (0, 0, 0))
gameover_score_text = main_font.render('Score:', False, (0, 0, 0))
gameover_restart_text = reduced_font.render('Then press R to restart', False, (0, 0, 0))
gameover_name = reduced_font.render('Enter your name in terminal', False, (0, 0, 0))

start_time = time.time()

while running:

    if main_title:

        score = 0
        lives = config['lives']
        highscores = get_highscores('highscores.json')
        names = list(highscores.keys())
        scores = list(highscores.values())

        name_0 = reduced_font.render(names[0], False, (0, 0, 0))
        name_1 = reduced_font.render(names[1], False, (0, 0, 0))
        name_2 = reduced_font.render(names[2], False, (0, 0, 0))
        name_3 = reduced_font.render(names[3], False, (0, 0, 0))
        name_4 = reduced_font.render(names[4], False, (0, 0, 0))
        name_5 = reduced_font.render(names[5], False, (0, 0, 0))
        name_6 = reduced_font.render(names[6], False, (0, 0, 0))
        name_7 = reduced_font.render(names[7], False, (0, 0, 0))
        name_8 = reduced_font.render(names[8], False, (0, 0, 0))
        name_9 = reduced_font.render(names[9], False, (0, 0, 0))

        score_0 = reduced_font.render(str(scores[0]), False, (0, 0, 0))
        score_1 = reduced_font.render(str(scores[1]), False, (0, 0, 0))
        score_2 = reduced_font.render(str(scores[2]), False, (0, 0, 0))
        score_3 = reduced_font.render(str(scores[3]), False, (0, 0, 0))
        score_4 = reduced_font.render(str(scores[4]), False, (0, 0, 0))
        score_5 = reduced_font.render(str(scores[5]), False, (0, 0, 0))
        score_6 = reduced_font.render(str(scores[6]), False, (0, 0, 0))
        score_7 = reduced_font.render(str(scores[7]), False, (0, 0, 0))
        score_8 = reduced_font.render(str(scores[8]), False, (0, 0, 0))
        score_9 = reduced_font.render(str(scores[9]), False, (0, 0, 0))

    while main_title:

        main_title, running = quit(main_title, running)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            main_title = False
            start_timer = time.time()

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
        timer = start_timer - actual_timer
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
        screen.fill('red')
        screen.blit(gameover_text, (285, 100))
        screen.blit(gameover_score_text, (200, 300))
        screen.blit(score_text, (600, 300))
        screen.blit(gameover_name, (250, 600))
        screen.blit(gameover_restart_text, (300, 800))

        pygame.display.flip()
        name = input('Enter your name: ')
        while len(name) > 10:
            name = input('Max 10 characters: ')
        while len(name) == 0:
            name = input('Please input a name: ')
        register_highscore('highscores.json', name, score)
        print('You can go back to the game')

    while game_over:
        game_over, running = quit(game_over, running)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over, main_title = back_to_title()
        clock.tick(tick)

    _, running = quit(True, running)
    actual_timer = time.time()

    sprites_list = pygame.sprite.Group()
    for cell in walls:
        sprites_list.add(cell)
    sprites_list.update()
    # Player
    sprites_list.add(pacman)
    # Ghosts
    sprites_list.add(red_g)
    sprites_list.add(blue_g)
    sprites_list.add(orange_g)
    sprites_list.add(pink_g)


    screen.fill('purple')

    sprites_list.draw(screen)

    hud_bar = pygame.draw.rect(screen, 'black', ((0, maze_side * 64), (maze_side * 64, 128)))
    score_text = main_font.render('Score: ' + str(score), False, (255, 255, 255))
    lives_text = main_font.render('Lives: ' + str(lives), False, (255, 255, 255))
    timer_text = main_font.render('Timer: ' + str(config['level_max_time'] - int(actual_timer - start_timer)), False, (255, 255, 255))
    screen.blit(score_text, (20, maze_side * 64 + 40))
    screen.blit(lives_text, (maze_side * 64 - 280, maze_side * 64 + 40))
    screen.blit(timer_text, (330, maze_side * 64 + 40))

    keys = pygame.key.get_pressed()
    pacman.player_move(radius, keys)
    if keys[pygame.K_p]:
        pause = True
    if keys[pygame.K_KP_PLUS]:
        score += 100
    actual_time = time.time()
    if actual_time - start_time >= 0.0125:
        for ghost in Ghost.ghosts():
            ghost.ghost_move(radius)
        start_time = time.time()

    ghosts = Ghost.ghosts()
    if pacman.rect.collidelist(ghosts) >= 0:
        lives -= 1
        reset()
        start_timer = time.time()
        if lives == 0:
            game_over = True

    if config['level_max_time'] - int(actual_timer - start_timer) <= 0:
        lives -= 1
        reset()
        start_timer = time.time()
        if lives == 0:
            game_over = True

    pygame.display.flip()
    clock.tick(tick)

pygame.quit()
