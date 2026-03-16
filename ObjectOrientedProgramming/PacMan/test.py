import pygame
from pygame import Vector2
import time
from mazegenerator.mazegenerator import MazeGenerator
from sprites import Pacman, Ghost, Walls, maze_side
from manip_json import get_highscores, read_config, register_highscore
# 6, 8/, 10, 11, 12, 15, 16//, 20, 22, 24/, 25/, 30: 660 divisible by these
config = read_config('config.json')
top_offset = 120
player_coord: tuple[int, int] = (0, 0)
pygame.init()
window_w, window_h = 660, 990
maze: list[list[int]] = [[0]*(maze_side+2)]*(maze_side+2)
screen = pygame.display.set_mode((window_w, window_h))
clock = pygame.time.Clock()
running, main_title, pause, game_over = True, True, False, False
dt = 1
radius = 480/(maze_side+2)
tile_size = 660/(maze_side+2)
player_coord = (int(maze_side//2 +1), int(maze_side//2 +1))
player_pos = Vector2((maze_side//2 +1)*tile_size, (maze_side//2 +1)*tile_size + top_offset)
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

def quit(state: bool, running: bool) -> tuple[bool, bool]:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (False, False)
    return (state, running)

def back_to_title() -> tuple[bool, bool]:
    Ghost.clear_ghosts()
    pacman.__init__('yellow', radius, player_pos, player_coord)
    red_g.__init__('red', radius, Vector2(tile_size, top_offset + tile_size), (1, 1))
    blue_g.__init__('blue', radius, Vector2(window_w - 2 * tile_size , top_offset + tile_size), (maze_side-2, 1))
    orange_g.__init__('orange', radius, Vector2(tile_size, top_offset+(maze_side-2)*tile_size), (1, maze_side-2))
    pink_g.__init__('pink', radius, Vector2(window_w - 2 * tile_size, top_offset+(maze_side-2)*tile_size), (maze_side-2, maze_side-2))

    return (False, True)

def reset() -> None:
    Ghost.clear_ghosts()
    pacman.__init__('yellow', radius, player_pos, player_coord)
    red_g.__init__('red', radius, Vector2(tile_size, top_offset + tile_size), (1, 1))
    blue_g.__init__('blue', radius, Vector2(window_w - 2 * tile_size , top_offset + tile_size), (maze_side-2, 1))
    orange_g.__init__('orange', radius, Vector2(tile_size, top_offset+(maze_side-2)*tile_size), (1, maze_side-2))
    pink_g.__init__('pink', radius, Vector2(window_w - 2 * tile_size, top_offset+(maze_side-2)*tile_size), (maze_side-2, maze_side-2))

def maze_gen(maze: list[list[int]], walls_name: list[str]) -> list[Walls]:
    walls: list[Walls] = []
    for y in range(maze_side):
        for x in range(maze_side):
            cell = Walls(walls_name[maze[y][x]])
            cell.rect.x = x * tile_size
            cell.rect.y = y * tile_size + top_offset
            walls.append(cell)
    return walls


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
        pygame.display.flip()
        clock.tick(tick)

    while main_title:

        main_title, running = quit(main_title, running)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            main_title = False
            start_timer = time.time()
            gen = MazeGenerator(size=(maze_side, maze_side),seed=42)
            maze = gen.maze
            new_maze = [[15]*(maze_side+2)]*(maze_side+2)
            for i in range(1, maze_side + 1):
                new_row = maze[i-1]
                new_row.insert(0, 15 if i != maze_side//2+1 else 5)
                new_row.insert(len(new_row), 15 if i != maze_side//2+1 else 5)
                new_row[1] -= 8 if new_row[0] == 5 else 0
                new_row[maze_side] -= 2 if new_row[maze_side+1] == 5 else 0
                new_maze[i] = new_row
            maze_side += 2
            maze = new_maze
            walls = maze_gen(maze, walls_name)
            if maze_side>=17:
                old = player_coord
                for row in maze:
                    for i in range(maze_side-6):
                        if row[i] == 15 and row[i+1] == 15 and row[i+2] == 15 and row[i+3] == 0 and row[i+4] == 15 and row[i+5] == 15 and row[i+6] == 15:
                            player_pos = Vector2((i+3)*tile_size, (maze_side//2)*tile_size + top_offset)
                            player_coord = (i+3, int(maze_side//2))
                            break
                    if player_coord != old:
                        break
            pacman = Pacman('yellow', radius, player_pos, player_coord)
            red_g = Ghost('red', radius, Vector2(tile_size, top_offset + tile_size), (1, 1))
            blue_g = Ghost('blue', radius, Vector2(window_w - 2 * tile_size , top_offset + tile_size), (maze_side-2, 1))
            orange_g = Ghost('orange', radius, Vector2(tile_size, top_offset+(maze_side-2)*tile_size), (1, maze_side-2))
            pink_g = Ghost('pink', radius, Vector2(window_w - 2 * tile_size, top_offset+(maze_side-2)*tile_size), (maze_side-2, maze_side-2))

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


    screen.fill('black')

    sprites_list.draw(screen)

    # hud_bar = pygame.draw.rect(screen, 'black', ((0, maze_side * 64), (maze_side * 64, 128)))
    # score_text = main_font.render('Score: ' + str(score), False, (255, 255, 255))
    # lives_text = main_font.render('Lives: ' + str(lives), False, (255, 255, 255))
    # timer_text = main_font.render('Timer: ' + str(config['level_max_time'] - int(actual_timer - start_timer)), False, (255, 255, 255))
    # screen.blit(score_text, (20, maze_side * 64 + 40))
    # screen.blit(lives_text, (maze_side * 64 - 280, maze_side * 64 + 40))
    # screen.blit(timer_text, (330, maze_side * 64 + 40))

    keys = pygame.key.get_pressed()
    pacman.player_move(radius, keys, maze)
    if keys[pygame.K_p]:
        pause = True
    if keys[pygame.K_KP_PLUS]:
        score += 100
    actual_time = time.time()
    if actual_time - start_time >= 0.0125:
        for ghost in Ghost.ghosts():
            ghost.ghost_move(radius, maze)
        start_time = time.time()

    ghosts = Ghost.ghosts()
    if pacman.rect.collidelist(ghosts) >= 0:
        lives -= 1
        reset()
        sprites_list.add(pacman)
        sprites_list.add(red_g)
        sprites_list.add(blue_g)
        sprites_list.add(orange_g)
        sprites_list.add(pink_g)
        screen.fill('black')
        sprites_list.draw(screen)
        pygame.display.flip()
        clock.tick(tick)
        start_timer = time.time()
        actual_time = time.time()
        while actual_time - start_timer < 5:
            actual_time = time.time()
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
