import pygame
import random
from pygame import Vector2
from pygame.event import Event
import time
from ghosts import Blinky, Clyde
from mazegenerator.mazegenerator import MazeGenerator  # type: ignore
from sprites import Pacman, Ghost, Walls, maze_side
from manip_json import get_highscores, read_config, register_highscore
from render_generate import main_title_render, main_title_generate
from render_generate import pause_render, pause_generate, g_o_render
from render_generate import g_o_generate, hud_render, hud_generate
from render_generate import l_s_generate, l_s_render
from pacgums import Pacgum, pacgums_gen, SuperPacgum
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
    red_g.init('red', radius, Vector2(tile_size, top_offset + 2*tile_size),
               (1, 2), player_coord, 'blinky')
    blue_g.init('cyan', radius,
                Vector2(window_w - 2 * tile_size, top_offset + tile_size),
                (maze_side, 2), player_coord, 'inky')
    orange_g.init('orange', radius,
                  Vector2(tile_size, top_offset+(maze_side)*tile_size),
                  (1, maze_side-1), player_coord, 'clyde')
    pink_g.init('pink', radius,
                Vector2(window_w - 2 * tile_size,
                        top_offset+(maze_side)*tile_size),
                (maze_side, maze_side-1), player_coord, 'pinky')

    return (False, True)


def reset(tile_size: float,
          top_offset: int,
          window_w: int,
          maze_side: int,
          player_coord: tuple[int, int]) -> None:
    Ghost.clear_ghosts()
    pacman.init('yellow', radius, player_pos, player_coord)
    red_g.init('red', radius, Vector2(tile_size, top_offset + 2*tile_size),
               (1, 2), player_coord, 'blinky')
    blue_g.init('cyan', radius,
                Vector2(window_w - 2 * tile_size, top_offset + 2*tile_size),
                (maze_side, 2), player_coord, 'inky')
    orange_g.init('orange', radius,
                  Vector2(tile_size, top_offset+(maze_side-1)*tile_size),
                  (1, maze_side-1), player_coord, 'clyde')
    pink_g.init('pink', radius,
                Vector2(window_w - 2 * tile_size,
                        top_offset+(maze_side-1)*tile_size),
                (maze_side, maze_side-1), player_coord, 'pinky')


def maze_gen(maze: list[list[int]], walls_name: list[str]) -> list[Walls]:
    walls: list[Walls] = []
    for y in range(maze_side+2):
        for x in range(maze_side+2):
            cell = Walls(walls_name[maze[y][x]])
            assert cell.rect is not None
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
    eatable_start: float = 0
    eatable_timer: float = 0
    refresh_rate = 0.0125
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
            next_level = False

        while main_title or next_level:

            main_title, running = quit(main_title, running)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE] or next_level:
                l_s_generate(screen, l_s_render())
                pygame.display.flip()
                main_title = False
                start = True
                ghost_eatable = False
                gen = MazeGenerator(size=(maze_side, maze_side), seed=random.randint(1, 99))
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
                pacgums = pacgums_gen(maze_side,
                                      maze_side * maze_side,
                                      config['points_per_pacgum'],
                                      config['points_per_super_pacgum'],
                                      maze,
                                      player_coord)
                pacman = Pacman('yellow', radius, player_pos, player_coord)
                red_g = Blinky('red', radius,
                               Vector2(tile_size, top_offset + 2*tile_size),
                               (1, 2), player_coord, 'blinky')
                blue_g = Blinky('cyan', radius,
                                Vector2(window_w - 2 * tile_size,
                                        top_offset + 2*tile_size),
                                (maze_side, 2), player_coord, 'inky')
                orange_g = Clyde('orange', radius,
                                 Vector2(tile_size,
                                         top_offset+(maze_side-1)*tile_size),
                                 (1, maze_side-1), player_coord, 'clyde')
                pink_g = Blinky('pink', radius,
                                Vector2(window_w - 2 * tile_size,
                                        top_offset+(maze_side-1)*tile_size),
                                (maze_side, maze_side-1),
                                player_coord, 'pinky')
                start_time = time.time()
                start_timer = time.time()
            else:
                main_title_generate(screen, names_text,
                                    scores_text, mt_text,
                                    play_text, leaderboard_text)
            clock.tick(tick)
            next_level = False
            nb_of_pg_eaten = 0

        _, running = quit(True, running)
        actual_timer = time.time()
        timer = int(last_timer - actual_timer + start_timer) + 1

        sprites_list = pygame.sprite.Group(pacman,
                                           red_g,
                                           blue_g,
                                           orange_g,
                                           pink_g)

        walls_sprites: pygame.sprite.Group[Walls] = pygame.sprite.Group()
        for cell in walls:
            walls_sprites.add(cell)

        pacgums_sprites: pygame.sprite.Group[Pacgum] = pygame.sprite.Group()
        for pacgum in pacgums:
            pacgums_sprites.add(pacgum)

        pacgums_sprites.update()
        walls_sprites.update()
        sprites_list.update()

        screen.fill('black')
        if not game_over and not pause:
            walls_sprites.draw(screen)
            pacgums_sprites.draw(screen)
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
        if (keys[pygame.K_e] or
           ghost_eatable) and eatable_timer - eatable_start <= 0:
            eatable_start = time.time()
            for ghost in Ghost.ghosts():
                ghost.eatable = not ghost.eatable
            refresh_rate = 0.0175
        if eatable_start != 0:
            eatable_timer = time.time()

        if eatable_timer - eatable_start >= 5:
            eatable_timer = 0
            eatable_start = 0
            ghost_eatable = False
            for ghost in Ghost.ghosts():
                ghost.eatable = not ghost.eatable
                ghost.eaten = False
                ghost.dt = 1
                ghost.path_changed = False
            refresh_rate = 0.0125

        for pacgum in pacgums_sprites:
            if (pygame.sprite.collide_circle(pacman, pacgum) and
                    not pacgum.eaten):
                score += pacgum.score
                pacgum.radius = 0
                pacgum.score = 0
                pacgum.eaten = True
                nb_of_pg_eaten += 1
                pygame.draw.rect(pacgum.image, 'black',
                                 ((0, 0), (tile_size, tile_size)))
                pygame.display.flip()
                if isinstance(pacgum, SuperPacgum):
                    ghost_eatable = True

        pacman.player_move(int(radius), keys, maze)
        pacman.animate(0)
        assert pacman.rect is not None
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
        if actual_time - start_time >= refresh_rate:
            for ghost in Ghost.ghosts():
                ghost.ghost_move(int(radius), maze,
                                 old_maze, pacman)
                ghost.animate(eatable_timer - eatable_start)
            start_time = time.time()

        ghosts = Ghost.ghosts()
        # if pygame.sprite.spritecollideany(pacman,
        #   ghosts, pygame.sprite.collide_mask):
        lst = []
        eaten = []
        for ghost in ghosts:
            if pygame.sprite.collide_circle(pacman, ghost) and ghost.eatable:
                eaten.append(ghost)
            elif (pygame.sprite.collide_circle(pacman, ghost) and
                    not ghost.eatable):
                lst.append(True)
            else:
                lst.append(False)
        for ghost in eaten:
            ghost.eaten = True
            ghost.dt = 10
        if True in lst:
            lives -= 1
            refresh_rate = 0.0125
            reset(tile_size, top_offset, window_w, maze_side, player_coord)
            sprites_list.add(pacman)
            sprites_list.add(red_g)
            sprites_list.add(blue_g)
            sprites_list.add(orange_g)
            sprites_list.add(pink_g)
            screen.fill('black')
            walls_sprites.draw(screen)
            pacgums_sprites.draw(screen)
            sprites_list.draw(screen)
            clock.tick(tick)
            actual_time = time.time()
            start_timer = time.time()
            txt = hud_render(score, highest_score, 90)
            score_text, score_nb, h_s_text, h_s_nb, timer_text, timer_nb = txt
            while actual_time - start_timer < 3 and lives != 0:
                actual_time = time.time()
                hud_generate(screen, score_text,
                             score_nb, h_s_text,
                             h_s_nb, timer_text,
                             timer_nb, lives)
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

        if nb_of_pg_eaten == len(pacgums_sprites):
            next_level = True

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
            events: list[Event] = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    game_over, running = False, False
            g_o_generate(screen, g_o_text,
                         g_o_score_text, g_o_score,
                         g_o_name, text_input, events)
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_RETURN] and
                    len(text_input.value) < 10 and
                    len(text_input.value) > 0):
                name = text_input.value
                register_highscore('highscores.json', name, score)
                game_over, main_title = back_to_title(tile_size,
                                                      top_offset,
                                                      window_w,
                                                      maze_side,
                                                      player_coord)
            clock.tick(tick)

    pygame.quit()
