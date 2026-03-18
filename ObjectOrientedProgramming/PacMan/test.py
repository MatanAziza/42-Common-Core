import pygame
from pygame import Vector2
import time
from ghosts import Blinky
from djikstra import shortest_path
from mazegenerator.mazegenerator import MazeGenerator
from sprites import Pacman, Ghost, Walls, maze_side
from manip_json import get_highscores, read_config, register_highscore
from render_generate import main_title_render, main_title_generate
from render_generate import pause_render, pause_generate, g_o_render
from render_generate import g_o_generate, hud_render, hud_generate
from render_generate import l_s_generate, l_s_render
from pacgums import pacgums_gen
# 6, 8/, 10, 11, 12, 15, 16//, 20, 22, 24/, 25/, 30: 660 divisible by these


def quit(state: bool, running: bool) -> tuple[bool, bool]:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (False, False)
    return (state, running)


def back_to_title(tile_size: float,
                  top_offset: int,
                  window_w: int,
                  maze_side: int,
                  player_coord: tuple[int, int]) -> tuple[bool, bool]:
    Ghost.clear_ghosts()
    pacman.init('yellow', radius, player_pos, player_coord)
    red_g.init('red', radius, Vector2(tile_size, top_offset + tile_size),
               (1, 1), player_coord)
    blue_g.init('blue', radius,
                Vector2(window_w - 2 * tile_size, top_offset + tile_size),
                (maze_side, 1), player_coord)
    orange_g.init('orange', radius,
                  Vector2(tile_size, top_offset+(maze_side)*tile_size),
                  (1, maze_side), player_coord)
    pink_g.init('pink', radius,
                Vector2(window_w - 2 * tile_size,
                        top_offset+(maze_side)*tile_size),
                (maze_side, maze_side), player_coord)

    return (False, True)


def reset(tile_size: float,
          top_offset: int,
          window_w: int,
          maze_side: int,
          player_coord: tuple[int, int]) -> None:
    Ghost.clear_ghosts()
    pacman.init('yellow', radius, player_pos, player_coord)
    red_g.init('red', radius, Vector2(tile_size, top_offset + tile_size),
               (1, 1), player_coord)
    blue_g.init('blue', radius,
                Vector2(window_w - 2 * tile_size, top_offset + tile_size),
                (maze_side, 1), player_coord)
    orange_g.init('orange', radius,
                  Vector2(tile_size, top_offset+(maze_side)*tile_size),
                  (1, maze_side), player_coord)
    pink_g.init('pink', radius,
                Vector2(window_w - 2 * tile_size,
                        top_offset+(maze_side)*tile_size),
                (maze_side, maze_side), player_coord)


def maze_gen(maze: list[list[int]], walls_name: list[str]) -> list[Walls]:
    walls: list[Walls] = []
    for y in range(maze_side+2):
        for x in range(maze_side+2):
            cell = Walls(walls_name[maze[y][x]])
            cell.rect.x = int(x * tile_size)
            cell.rect.y = int(y * tile_size + top_offset)
            walls.append(cell)
    return walls


def between_42(maze: list[list[int]], i: int, j: int) -> bool:
    a = maze[j][i] == 15
    b = maze[j][i+1] == 15
    c = maze[j][i+2] == 15
    d = maze[j][i+3] != 15
    e = maze[j][i+4] == 15
    f = maze[j][i+5] == 15
    g = maze[j][i+6] == 15
    return a and b and c and d and e and f and g


if __name__ == "__main__":
    config = read_config('config.json')
    top_offset = 120
    pygame.init()
    window_w, window_h = 660, 990
    maze: list[list[int]] = [[0]*(maze_side+2)]*(maze_side+2)
    old_maze: list[list[int]] = [[0]*(maze_side+2)]*(maze_side+2)
    screen = pygame.display.set_mode((window_w, window_h))
    clock = pygame.time.Clock()
    running, main_title, pause, game_over = True, True, False, False
    dt = 1
    radius = 480/(maze_side+2)
    tile_size = 660/(maze_side+2)
    player_coord = (int(maze_side//2 + 1), int(maze_side//2 + 1))
    player_pos = Vector2((maze_side//2 + 1)*tile_size,
                         (maze_side//2 + 1)*tile_size + top_offset)
    tick = 60
    eatable_start = 0
    eatable_timer = 0
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

    while running:

        if main_title:
            highscores = get_highscores('highscores.json')
            highest_score = max(list(highscores.values()))
            z = main_title_render(highscores)
            mt_text, play_text, leaderboard_text, names_text, scores_text = z
            score = 0
            lives = config['lives']
            last_timer = config['level_max_time']

        while main_title:

            main_title, running = quit(main_title, running)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                l_s_generate(screen, l_s_render())
                pygame.display.flip()
                main_title = False
                start = True
                gen = MazeGenerator(size=(maze_side, maze_side), seed=42)
                maze = gen.maze
                old_maze = [[nb for nb in row] for row in maze]
                new_maze = [[15]*(maze_side+2)]*(maze_side+2)
                for i in range(1, maze_side + 1):
                    row = maze[i-1]
                    row.insert(0, 15 if i != maze_side//2+1 else 5)
                    row.insert(len(row), 15 if i != maze_side//2+1 else 5)
                    row[1] -= 8 if row[0] == 5 else 0
                    row[maze_side] -= 2 if row[maze_side+1] == 5 else 0
                    new_maze[i] = row
                maze = new_maze
                walls = maze_gen(maze, walls_name)
                pacgums = pacgums_gen(maze_side, config['pacgum'], config['points_per_pacgum'], config['points_per_super_pacgum'], maze)
                if maze_side >= 15:
                    old = player_coord
                    for j in range(len(maze)):
                        for i in range(maze_side-4):
                            if between_42(maze, i, j):
                                player_pos = Vector2(
                                    (i+3)*tile_size,
                                    (j)*tile_size + top_offset)
                                player_coord = (i+3, j)
                                break
                        if player_coord != old:
                            break
                pacman = Pacman('yellow', radius, player_pos, player_coord)
                red_g = Blinky('red', radius,
                              Vector2(tile_size, top_offset + tile_size),
                              (1, 1), player_coord)
                blue_g = Blinky('blue', radius,
                               Vector2(window_w - 2 * tile_size,
                                       top_offset + tile_size),
                               (maze_side, 1), player_coord)
                orange_g = Blinky('orange', radius,
                                 Vector2(tile_size,
                                         top_offset+(maze_side)*tile_size),
                                 (1, maze_side), player_coord)
                pink_g = Blinky('pink', radius,
                               Vector2(window_w - 2 * tile_size,
                                       top_offset+(maze_side)*tile_size),
                               (maze_side, maze_side), player_coord)
                start_time = time.time()
                start_timer = time.time()
            else:
                main_title_generate(screen, names_text,
                                    scores_text, mt_text,
                                    play_text, leaderboard_text)
            clock.tick(tick)

        _, running = quit(True, running)
        actual_timer = time.time()
        timer = int(last_timer - actual_timer + start_timer) + 1

        sprites_list = pygame.sprite.Group([pacman, red_g,
                                            blue_g, orange_g, pink_g])
        for cell in walls:
            sprites_list.add(cell)

        for pacgum in pacgums:
            sprites_list.add(pacgum)

        sprites_list.update()

        screen.fill('black')
        if not game_over and not pause:
            sprites_list.draw(screen)

            x = hud_render(score, highest_score, timer)
            score_text = x[0]
            score_nb = x[1]
            h_s_text = x[2]
            h_s_nb = x[3]
            timer_text = x[4]
            timer_nb = x[5]
            hud_generate(screen, score_text,
                         score_nb, h_s_text,
                         h_s_nb, timer_text, timer_nb, lives)

        actual_time = time.time()
        while start and actual_time - start_time < 3:
            actual_time = time.time()
            actual_timer = time.time()
            start_timer = time.time()
            pygame.display.flip()

        start = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e] and eatable_timer - eatable_start <= 0:
            eatable_start = time.time()
            for ghost in Ghost.ghosts():
                ghost.eatable = not ghost.eatable
                ghost.dt = 1
        if eatable_start != 0:
            eatable_timer = time.time()
        if eatable_timer - eatable_start >= 5:
            eatable_timer = 0
            eatable_start = 0
            for ghost in Ghost.ghosts():
                ghost.eatable = not ghost.eatable
                ghost.path_changed = False
                ghost.dt = 2
        pacman.player_move(int(radius), keys, maze)
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
        if actual_time - start_time >= 0.025:
            for ghost in Ghost.ghosts():
                ghost.ghost_move(int(radius), maze,
                                 old_maze, pacman)
            start_time = time.time()

        ghosts = Ghost.ghosts()
        # if pygame.sprite.spritecollideany(pacman,
        #   ghosts, pygame.sprite.collide_mask):
        lst = []
        for ghost in ghosts:
            if pygame.sprite.collide_circle(pacman, ghost) and not ghost.eatable:
                lst.append(True)
            else:
                lst.append(False)
        if True in lst:
            lives -= 1
            reset(tile_size, top_offset, window_w, maze_side, player_coord)
            sprites_list.add(pacman)
            sprites_list.add(red_g)
            sprites_list.add(blue_g)
            sprites_list.add(orange_g)
            sprites_list.add(pink_g)
            screen.fill('black')
            sprites_list.draw(screen)
            clock.tick(tick)
            actual_time = time.time()
            start_timer = time.time()
            score_text, score_nb, h_s_text, h_s_nb, timer_text, timer_nb = hud_render(score, highest_score, 90)
            while actual_time - start_timer < 3 and lives != 0:
                actual_time = time.time()
                hud_generate(screen, score_text, score_nb, h_s_text, h_s_nb, timer_text, timer_nb, lives)
                pygame.display.flip()
            last_timer = config['level_max_time']
            start_timer = time.time()
        if lives == 0:
            game_over = True
        if timer <= 0:
            lives -= 1
            reset(tile_size, top_offset, window_w, maze_side, player_coord)
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
                pause, main_title = back_to_title(tile_size,
                                                  top_offset,
                                                  window_w,
                                                  maze_side,
                                                  player_coord)
            start_timer = time.time()
            pause_generate(screen, pause_text, resume_text, back_text)

        if game_over:
            y = g_o_render(score)
            g_o_text, g_o_score_text, g_o_score, g_o_name, text_input = y

        while game_over:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    game_over, running = False, False
            g_o_generate(screen, g_o_text,
                         g_o_score_text, g_o_score,
                         g_o_name, text_input, events)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] and len(text_input.value) < 10 and len(text_input.value) > 0:
                name = text_input.value
                register_highscore('highscores.json', name, score)
                game_over, main_title = back_to_title(tile_size,
                                                      top_offset,
                                                      window_w,
                                                      maze_side,
                                                      player_coord)
            clock.tick(tick)

    pygame.quit()
