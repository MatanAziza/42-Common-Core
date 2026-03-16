import pygame
from pygame import Vector2
import time
from mazegenerator.mazegenerator import MazeGenerator
from sprites import Pacman, Ghost, Walls, maze_side
from manip_json import get_highscores, read_config, register_highscore
from render_generate import main_title_render, main_title_generate, pause_render, pause_generate, gameover_render, gameover_generate, hud_render, hud_generate

# 6, 8/, 10, 11, 12, 15, 16//, 20, 22, 24/, 25/, 30: 660 divisible by these


def quit(state: bool, running: bool) -> tuple[bool, bool]:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (False, False)
    return (state, running)

def back_to_title(radius: float,
                  tile_size: float,
                  top_offset: int,
                  window_w: int,
                  maze_side: int) -> tuple[bool, bool]:
    Ghost.clear_ghosts()
    pacman.__init__('yellow', radius, player_pos, player_coord)
    red_g.__init__('red', radius, Vector2(tile_size, top_offset + tile_size), (1, 1))
    blue_g.__init__('blue', radius, Vector2(window_w - 2 * tile_size , top_offset + tile_size), (maze_side-2, 1))
    orange_g.__init__('orange', radius, Vector2(tile_size, top_offset+(maze_side-2)*tile_size), (1, maze_side-2))
    pink_g.__init__('pink', radius, Vector2(window_w - 2 * tile_size, top_offset+(maze_side-2)*tile_size), (maze_side-2, maze_side-2))

    return (False, True)

def reset(radius: float,
          tile_size: float,
          top_offset: int,
          window_w: int,
          maze_side: int) -> None:
    Ghost.clear_ghosts()
    pacman.__init__('yellow', radius, player_pos, player_coord)
    red_g.__init__('red', radius, Vector2(tile_size, top_offset + tile_size), (1, 1))
    blue_g.__init__('blue', radius, Vector2(window_w - 2 * tile_size , top_offset + tile_size), (maze_side-2, 1))
    orange_g.__init__('orange', radius, Vector2(tile_size, top_offset+(maze_side-2)*tile_size), (1, maze_side-2))
    pink_g.__init__('pink', radius, Vector2(window_w - 2 * tile_size, top_offset+(maze_side-2)*tile_size), (maze_side-2, maze_side-2))

def maze_gen(maze: list[list[int]], walls_name: list[str]) -> list[Walls]:
    walls: list[Walls] = []
    for y in range(maze_side+2):
        for x in range(maze_side+2):
            cell = Walls(walls_name[maze[y][x]])
            cell.rect.x = x * tile_size
            cell.rect.y = y * tile_size + top_offset
            walls.append(cell)
    return walls

if __name__ == "__main__":
    config = read_config('config.json')
    top_offset = 120
    pygame.init()
    window_w, window_h = 660, 990
    maze: list[list[int]] = [[0]*(maze_side+2)]*(maze_side+2)
    screen = pygame.display.set_mode((window_w, window_h))
    clock = pygame.time.Clock()
    running, main_title, pause, game_over = True, True, False, False
    dt = 1
    radius = 480/(maze_side+2)
    tile_size = 660/(maze_side+2)
    player_coord = (int(maze_side//2 +1), int(maze_side//2 + 1))
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
    start_time = time.time()

    while running:

        if main_title:
            highscores = get_highscores('highscores.json')
            highest_score = max(list(highscores.values()))
            mt_text, play_text, leaderboard_text, names_text, scores_text = main_title_render(highscores)
            score = 0
            lives = config['lives']
            last_timer = config['level_max_time']

        while main_title:

            main_title, running = quit(main_title, running)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                main_title = False
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
                maze = new_maze
                walls = maze_gen(maze, walls_name)
                if maze_side>=15:
                    old = player_coord
                    for j in range(len(maze)):
                        for i in range(maze_side-4):
                            if maze[j][i] == 15 and maze[j][i+1] == 15 and maze[j][i+2] == 15 and maze[j][i+3] != 15 and maze[j][i+4] == 15 and maze[j][i+5] == 15 and maze[j][i+6] == 15:
                                player_pos = Vector2((i+3)*tile_size, (j)*tile_size + top_offset)
                                player_coord = (i+3, j)
                                break
                        if player_coord != old:
                            break
                pacman = Pacman('yellow', radius, player_pos, player_coord)
                red_g = Ghost('red', radius, Vector2(tile_size, top_offset + tile_size), (1, 1))
                blue_g = Ghost('blue', radius, Vector2(window_w - 2 * tile_size , top_offset + tile_size), (maze_side, 1))
                orange_g = Ghost('orange', radius, Vector2(tile_size, top_offset+(maze_side)*tile_size), (1, maze_side))
                pink_g = Ghost('pink', radius, Vector2(window_w - 2 * tile_size, top_offset+(maze_side)*tile_size), (maze_side, maze_side))
                start_timer = time.time()

            main_title_generate(screen, names_text, scores_text, mt_text, play_text, leaderboard_text)
            clock.tick(tick)

        _, running = quit(True, running)
        actual_timer = time.time()
        timer = int(last_timer - actual_timer + start_timer) + 1

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
        if not game_over and not pause:
            sprites_list.draw(screen)

            score_text, score_nb, highscore_text, highscore_nb, timer_text, timer_nb = hud_render(score, lives, highest_score, timer)
            hud_generate(screen, score_text, score_nb, highscore_text, highscore_nb, timer_text, timer_nb, lives)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_i]:
            print("hehe")
        pacman.player_move(radius, keys, maze)
        if pacman.rect.x < 0:
            pacman.tp_ltr(radius)
        elif pacman.rect.x > window_w - tile_size:
            pacman.tp_rtl(radius)
        if keys[pygame.K_p] and not main_title:
            pause = True
        if keys[pygame.K_KP_PLUS]:
            score += 100
        if keys[pygame.K_KP_MINUS]:
            game_over = True
            lives = 0

        actual_time = time.time()
        if actual_time - start_time >= 0.0125:
            for ghost in Ghost.ghosts():
                ghost.ghost_move(radius, maze)
            start_time = time.time()

        ghosts = Ghost.ghosts()
        if pacman.rect.collidelist(ghosts) >= 0:
            lives -= 1
            reset(radius, tile_size, top_offset, window_w, maze_side)
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
        if timer <= 0:
            lives -= 1
            reset(radius, tile_size, top_offset, window_w, maze_side)
            start_timer = time.time()
            if lives <= 0:
                game_over = True
        pygame.display.flip()
        clock.tick(tick)

        if pause:
            pause_text, resume_text, back_text = pause_render()
            last_timer = last_timer - actual_timer + start_timer

        while pause:
            pause, running = quit(pause, running)
            keys = pygame.key.get_pressed()
            clock.tick(tick)
            if keys[pygame.K_r]:
                pause = False
            elif keys[pygame.K_BACKSPACE]:
                pause, main_title = back_to_title(radius,
                                                  tile_size,
                                                  top_offset,
                                                  window_w,
                                                  maze_side)
            start_timer = time.time()
            pause_generate(screen, pause_text, resume_text, back_text)

        if game_over:
            gameover_text, gameover_score_text, gameover_score, gameover_name, gameover_restart = gameover_render(score)
            gameover_generate(screen, gameover_text, gameover_score_text, gameover_score, gameover_name, gameover_restart)
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
                game_over, main_title = back_to_title(radius,
                                                      tile_size,
                                                      top_offset,
                                                      window_w,
                                                      maze_side)
            clock.tick(tick)

    pygame.quit()
