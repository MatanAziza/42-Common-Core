import random
import time
import pygame
import sys
from typing import Any
from pygame import Vector2
from pygame.event import Event
from pygame.key import ScancodeWrapper
from ghosts import Blinky, Clyde, Pinky
from mazegenerator.mazegenerator import MazeGenerator  # type: ignore
from sprites import Pacman, Ghost, Walls
from manip_json import get_highscores, read_config, register_highscore
from render_generate import main_title_render, main_title_generate
from render_generate import ready_generate, ready_render
from render_generate import pause_render, pause_generate, g_o_render
from render_generate import g_o_generate, hud_render, hud_generate
from render_generate import l_s_generate, l_s_render, won_render
from render_generate import instructions_render, instructions_generate
from pacgums import pacgums_gen, SuperPacgum
from utils import dec_to_bin
from pygame.mixer import Sound


def quit(state: bool, running: bool) -> tuple[bool, bool]:
    "checks if a quitting event has occured, and returns the game state."
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return (False, False)
    return (state, running)


def level_changer(keys: ScancodeWrapper) -> int:
    "changes the level in cheat mode if a number is pressed"
    if keys[pygame.K_KP_0] or keys[pygame.K_0]:
        return 0
    elif keys[pygame.K_KP_1] or keys[pygame.K_1]:
        return 1
    elif keys[pygame.K_KP_2] or keys[pygame.K_2]:
        return 2
    elif keys[pygame.K_KP_3] or keys[pygame.K_3]:
        return 3
    elif keys[pygame.K_KP_4] or keys[pygame.K_4]:
        return 4
    elif keys[pygame.K_KP_5] or keys[pygame.K_5]:
        return 5
    elif keys[pygame.K_KP_6] or keys[pygame.K_6]:
        return 6
    elif keys[pygame.K_KP_7] or keys[pygame.K_7]:
        return 7
    elif keys[pygame.K_KP_8] or keys[pygame.K_8]:
        return 8
    elif keys[pygame.K_KP_9] or keys[pygame.K_9]:
        return 9
    else:
        return -1


def back_to_title(config: dict[str, Any],
                  side: int,
                  player_coord: tuple[int, int]) -> tuple[bool, bool]:
    "resets the game by setting all characters value to default"
    Ghost.clear_ghosts()
    tile_size = config['tile_size']
    top_offset = config['top_offset']
    pacman.init('yellow', config['radius'], player_pos, player_coord)
    red_g.init('red',
               config['radius'],
               Vector2(tile_size, top_offset + 2*tile_size),
               (1, 2),
               player_coord,
               'blinky',
               config['dt'][config['level']])
    blue_g.init('cyan',
                config['radius'],
                Vector2(660 - 2 * tile_size, top_offset + 2*tile_size),
                (side, 2),
                player_coord,
                'inky',
                config['dt'][config['level']])
    orange_g.init('orange',
                  config['radius'],
                  Vector2(tile_size, top_offset+(side-1)*tile_size),
                  (1, side-1),
                  player_coord,
                  'clyde',
                  config['dt'][config['level']])
    pink_g.init('pink',
                config['radius'],
                Vector2(660 - 2 * tile_size,
                        top_offset+(side-1)*tile_size),
                (side, side-1),
                player_coord,
                'pinky',
                config['dt'][config['level']])

    return (False, True)


def reset(config: dict[str, Any],
          side: int,
          player_coord: tuple[int, int]) -> None:
    "resets the game by setting all characters value to default"
    tile_size = config['tile_size']
    top_offset = config['top_offset']
    pacman.init('yellow', config['radius'], player_pos, player_coord)
    red_g.init('red',
               config['radius'],
               Vector2(tile_size, top_offset + 2*tile_size),
               (1, 2),
               player_coord,
               'blinky',
               config['dt'][config['level']])
    blue_g.init('cyan',
                config['radius'],
                Vector2(660 - 2 * tile_size, top_offset + 2*tile_size),
                (side, 2),
                player_coord,
                'inky',
                config['dt'][config['level']])
    orange_g.init('orange',
                  config['radius'],
                  Vector2(tile_size, top_offset+(side-1)*tile_size),
                  (1, side-1),
                  player_coord,
                  'clyde',
                  config['dt'][config['level']])
    pink_g.init('pink',
                config['radius'],
                Vector2(660 - 2 * tile_size,
                        top_offset+(side-1)*tile_size),
                (side, side-1),
                player_coord,
                'pinky',
                config['dt'][config['level']])


def maze_gen(config: dict[str, Any],
             maze: list[list[int]],
             walls_name: list[str]) -> list[Walls]:
    "create a matrix of walls tiles to display for the entire game"
    walls: list[Walls] = []
    for y in range(config['side'][config['level']]+2):
        for x in range(config['side'][config['level']]+2):
            cell = Walls(config, walls_name[maze[y][x]])
            assert cell.rect is not None
            cell.rect.x = int(x * config['tile_size'])
            cell.rect.y = int(y * config['tile_size'] + config['top_offset'])
            walls.append(cell)
    return walls


def between_42(maze: list[list[int]], i: int, j: int) -> bool:
    "checks for the between 42 tile to put the player there is possible"
    a = maze[j][i] == 15
    b = maze[j][i+1] == 15
    c = maze[j][i+2] == 15
    d = maze[j][i+3] != 15
    e = maze[j][i+4] == 15
    f = maze[j][i+5] == 15
    g = maze[j][i+6] == 15
    return a and b and c and d and e and f and g


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(
            "Missing config file. Please provide "
            "this file named 'config.json' and run with:\n"
            "make run\nor\npython3 pacman.py config.json"
        )
        sys.exit(1)
    elif len(sys.argv) > 2:
        print(
            "Too much arguments provided. Please run with:\n"
            "make run\nor\npython3 pacman.py config.json"
        )
        sys.exit(1)
    file = sys.argv[1]
    config = read_config(file)
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.pre_init()
    window_w, window_h = 660, 990
    screen = pygame.display.set_mode((window_w, window_h))
    clock = pygame.time.Clock()
    next_level = False
    nb_of_pg_eaten = 0
    ready, set_txt, go = ready_render()
    running, main_title, pause, game_over, won = (True,
                                                  True,
                                                  False,
                                                  False,
                                                  False)
    refresh_rate = 0.0125
    flee = Sound('sounds/flee.mp3')
    chase = Sound('sounds/purchase.mp3')
    eat = Sound('sounds/eat.mp3')

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
            highest_score = highscores[0][1]
            z = main_title_render(highscores)
            (mt_text,
             play_text,
             quit_text,
             leaderboard_text,
             names_text,
             scores_text) = z
            score = 0
            lives = config['lives']
            last_timer = config['level_max_time']
            next_level = False
            cheat_mode = False
            can_move = True
            instructions = True
            eatable_start: float = 0
            eatable_timer: float = 0
            config.update({'level': 0})
            config.update({'tick': 60})

        while main_title or next_level:

            main_title, running = quit(main_title, running)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_q]:
                sys.exit(0)
            if keys[pygame.K_SPACE] or next_level:
                l_s_generate(screen, l_s_render())
                pygame.display.flip()
                config.update({'top_offset': 120})
                config.update({'radius':
                               480/(config['side'][config['level']]+2)})
                config.update({'tile_size':
                               660/(config['side'][config['level']]+2)})
                main_title = False
                start = True
                ghost_eatable = False
                player_coord = (int(config['side'][config['level']]//2+1),
                                int(config['side'][config['level']]//2+1))
                player_pos = Vector2(((config['side'][config['level']]//2+2) *
                                      config['tile_size']),
                                     ((config['side'][config['level']]//2+2) *
                                      config['tile_size'] +
                                      config['top_offset']))
                gen = MazeGenerator(size=(config['side'][config['level']],
                                          config['side'][config['level']]),
                                    seed=random.randint(1, 99))
                maze = gen.maze
                old_maze = [[nb for nb in row] for row in maze]
                new_maze = ([([15] *
                              (config['side'][config['level']]+2))] *
                            (config['side'][config['level']]+2))
                for i in range(1, config['side'][config['level']] + 1):
                    row = maze[i-1]
                    row.insert(0, 15 if i != (config['side'][config['level']]
                                              // 2 + 1)
                               else 5)
                    row.insert(len(row), 15
                               if i != (config['side'][config['level']]
                                        // 2 + 1)
                               else 5)
                    row[1] -= 8 if row[0] == 5 else 0
                    row[config['side']
                        [config['level']]] -= (2 if
                                               row[config['side']
                                                   [config['level']]+1]
                                               == 5
                                               else 0)
                    new_maze[i] = row
                maze = new_maze
                if config['side'][config['level']] >= 14:
                    old = player_coord
                    for j in range(len(maze)):
                        for i in range(config['side'][config['level']]-4):
                            if between_42(maze, i, j):
                                player_pos = Vector2(
                                    (i+3)*config['tile_size'],
                                    j*config['tile_size']+config['top_offset'])
                                player_coord = (i+3, j)
                                break
                        if player_coord != old:
                            break
                walls = maze_gen(config, maze, walls_name)
                pacgums = pacgums_gen(config, config['side'][config['level']],
                                      config['points_per_pacgum'],
                                      config['points_per_super_pacgum'],
                                      maze,
                                      player_coord,
                                      config['top_offset'],
                                      walls_name)
                pacman = Pacman(config,
                                'yellow',
                                config['radius'],
                                player_pos,
                                player_coord,
                                config['dt'][config['level']])
                while dec_to_bin(maze[player_coord[1]]
                                 [player_coord[0]])[pacman.direction] == 0:
                    pacman.direction = (pacman.direction+1) % 4
                    pacman.next_direction = pacman.direction
                Ghost.clear_ghosts()
                red_g = Blinky(config,
                               'red',
                               config['radius'],
                               Vector2(config['tile_size'],
                                       (config['top_offset']+2 *
                                        config['tile_size'])),
                               (1, 2),
                               player_coord,
                               'blinky')
                blue_g = Blinky(config,
                                'cyan',
                                config['radius'],
                                Vector2(window_w-2*config['tile_size'],
                                        (config['top_offset']+2 *
                                         config['tile_size'])),
                                (config['side'][config['level']], 2),
                                player_coord,
                                'inky')
                orange_g = Clyde(config,
                                 'orange',
                                 config['radius'],
                                 Vector2(config['tile_size'],
                                         (config['top_offset'] +
                                          (config['side'][config['level']]-1) *
                                          config['tile_size'])),
                                 (1, config['side'][config['level']]-1),
                                 player_coord,
                                 'clyde')
                pink_g = Pinky(config,
                               'pink',
                               config['radius'],
                               Vector2(window_w - 2 * config['tile_size'],
                                       (config['top_offset'] +
                                        (config['side'][config['level']]-1) *
                                        config['tile_size'])),
                               (config['side'][config['level']],
                                config['side'][config['level']]-1),
                               player_coord,
                               'pinky')
                nb_of_pg_eaten = 0
                next_level = False
                s_time = time.time()
                start_time = time.time()
                start_timer = time.time()
            else:
                main_title_generate(screen, names_text,
                                    scores_text, mt_text,
                                    play_text, quit_text, leaderboard_text)
            clock.tick(config['tick'])

        if instructions and running:
            temp = instructions_render()
            wasd_arrows, press_text, or_text, tomove_text, press_return = temp
            screen.fill('black')
            instructions_generate(screen,
                                  wasd_arrows,
                                  press_text,
                                  or_text,
                                  tomove_text,
                                  press_return)
            pygame.display.flip()
        while instructions and running:
            instructions, running = quit(instructions, running)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                instructions = False
                start_time = time.time()
                s_time = time.time()
                start_timer = time.time()

        _, running = quit(True, running)
        actual_timer = time.time()
        timer = int(last_timer - actual_timer + start_timer) + 1

        sprites_list = pygame.sprite.Group(pacman,
                                           red_g,
                                           blue_g,
                                           orange_g,
                                           pink_g)

        walls_sprites = pygame.sprite.Group(walls[0])
        for cell in walls[1:]:
            walls_sprites.add(cell)

        pacgums_sprites = pygame.sprite.Group(pacgums[0])
        for pacgum in pacgums[1:]:
            pacgums_sprites.add(pacgum)

        pacgums_sprites.update()
        walls_sprites.update()
        sprites_list.update()

        screen.fill('black')
        if not game_over and not pause and running:
            walls_sprites.draw(screen)
            pacgums_sprites.draw(screen)
            sprites_list.draw(screen)

            x = hud_render(score, highest_score, timer, config['level'] + 1)
            score_text = x[0]
            score_nb = x[1]
            h_s_text = x[2]
            h_s_nb = x[3]
            timer_text = x[4]
            timer_nb = x[5]
            level_text = x[6]
            level_nb = x[7]
            live_pacman = x[8]
            hud_generate(screen, lives,
                         score_text, score_nb,
                         h_s_text, h_s_nb,
                         timer_text, timer_nb,
                         level_text, level_nb,
                         live_pacman)

        actual_time = time.time()
        if start and running:
            pygame.mixer.music.load('sounds/intro.mp3')
            pygame.mixer.music.play()

        while start and running and actual_time - start_time < 4:
            start, running = quit(start, running)
            actual_time = time.time()
            actual_timer = time.time()
            start_timer = time.time()
            if actual_time - start_time < 2.2:
                ready_generate(screen, ready, 0)
            elif actual_time - start_time < 3.4:
                ready_generate(screen, set_txt, 1)
            else:
                ready_generate(screen, go, 2)
            pygame.display.flip()
        start = False

        keys = pygame.key.get_pressed()
        if ((keys[pygame.K_e] and cheat_mode) or
                ghost_eatable) and eatable_timer - eatable_start <= 0:
            eatable_start = time.time()
            for ghost in Ghost.ghosts():
                ghost.eatable = True
            refresh_rate = 0.0175
        if eatable_start != 0:
            eatable_timer = time.time()

        if eatable_timer - eatable_start >= 10:
            eatable_timer = 0
            eatable_start = 0
            ghost_eatable = False
            for ghost in Ghost.ghosts():
                ghost.eatable = False
                ghost.eaten = False
                ghost.dt = ghost.config['dt'][config['level']]
                ghost.path_changed = False
            refresh_rate = 0.0125

        pacman.player_move(keys, maze)
        pacman.animate(config, 0)
        assert pacman.rect is not None
        if pacman.rect.x < 0:
            pacman.tp_ltr(config['radius'])
        elif pacman.rect.x > window_w - config['tile_size']:
            pacman.tp_rtl(config['radius'])
        if keys[pygame.K_p] and not main_title:
            pause = True
        if keys[pygame.K_KP_MINUS] and cheat_mode:
            game_over = True
            lives = 0
        if keys[pygame.K_g] and cheat_mode:
            won = True
        if keys[pygame.K_c]:
            cheat_mode = True
        if keys[pygame.K_c] and keys[pygame.K_LCTRL]:
            cheat_mode = False
        if keys[pygame.K_m] and cheat_mode:
            can_move = False
        if keys[pygame.K_m] and cheat_mode and keys[pygame.K_LCTRL]:
            can_move = True

        sound_time = time.time()
        if sound_time - s_time >= 0.39:
            if pink_g.eatable:
                flee.play()
            else:
                chase.play()
            s_time = time.time()

        actual_time = time.time()
        if actual_time - start_time >= refresh_rate:
            for ghost in Ghost.ghosts():
                if can_move:
                    ghost.ghost_move(maze,
                                     old_maze, pacman)
                ghost.animate(config, eatable_timer - eatable_start)
            start_time = time.time()

        ghosts = Ghost.ghosts()
        lst = []
        eaten = []
        for ghost in ghosts:
            if pygame.sprite.collide_circle(pacman, ghost) and ghost.eatable:
                eaten.append(ghost)
            elif (pygame.sprite.collide_circle(pacman, ghost) and
                    not ghost.eatable) and not cheat_mode:
                lst.append(True)
            else:
                lst.append(False)
        for ghost in eaten:
            ghost.eaten = True
            ghost.dt = 10
        if True in lst:
            lives -= 1
            refresh_rate = 0.0125
            reset(config,
                  config['side'][config['level']],
                  player_coord)
            screen.fill('black')
            walls_sprites.draw(screen)
            pacgums_sprites.draw(screen)
            sprites_list.draw(screen)
            clock.tick(config['tick'])
            actual_time = time.time()
            start_timer = time.time()
            txt = hud_render(score, highest_score, timer, config['level'] + 1)
            (score_text,
             score_nb,
             h_s_text,
             h_s_nb,
             timer_text,
             timer_nb,
             level_text,
             level_nb,
             live_pacman) = txt
            while running and actual_time - start_timer < 4 and lives != 0:
                actual_time = time.time()
                _, running = quit(False, running)
                hud_generate(screen, lives,
                             score_text, score_nb,
                             h_s_text, h_s_nb,
                             timer_text, timer_nb,
                             level_text, level_nb,
                             live_pacman)
                if actual_time - start_timer < 2.2:
                    ready_generate(screen, ready, 0)
                elif actual_time - start_timer < 3.4:
                    ready_generate(screen, set_txt, 1)
                else:
                    ready_generate(screen, go, 2)
                pygame.display.flip()
            last_timer = config['level_max_time']
            start_timer = time.time()

        for pacgum in pacgums_sprites:
            if (pygame.sprite.collide_circle(pacman, pacgum) and
                    not pacgum.eaten):
                eat.play()
                score += pacgum.score
                pacgum.radius = 0
                pacgum.score = 0
                pacgum.eaten = True
                nb_of_pg_eaten += 1
                pygame.draw.rect(pacgum.image,
                                 'black',
                                 ((0, 0),
                                  (config['tile_size'],
                                   config['tile_size'])))
                pygame.display.flip()
                if isinstance(pacgum, SuperPacgum):
                    ghost_eatable = True
                    eatable_timer = time.time()
                    eatable_start = time.time()

        if lives == 0:
            game_over = True
        if timer <= 0:
            start = True
            lives -= 1
            reset(config,
                  config['side'][config['level']],
                  player_coord)
            start_timer = time.time()
            if lives <= 0:
                game_over = True
        pygame.display.flip()
        clock.tick(config['tick'])

        if nb_of_pg_eaten == len(pacgums_sprites):
            if config['level'] == 9:
                won = True
            else:
                next_level = True
                nb_of_pg_eaten = 0
                config.update({'level': config['level'] + 1})

        if cheat_mode and level_changer(keys) != -1:
            level_number = level_changer(keys)
            next_level = True
            nb_of_pg_eaten = 0
            config.update({'level': level_number})

        if pause:
            pause_text, resume_text, back_text = pause_render()
            last_timer = last_timer - actual_timer + start_timer

        while pause:
            pause, running = quit(pause, running)
            keys = pygame.key.get_pressed()
            clock.tick(config['tick'])
            if keys[pygame.K_r]:
                pause = False
            elif keys[pygame.K_BACKSPACE]:
                pause, main_title = back_to_title(config,
                                                  (config['side']
                                                   [config['level']]),
                                                  player_coord)
            start_timer = time.time()
            pause_generate(screen, pause_text, resume_text, back_text)

        if game_over:
            y = g_o_render(score)
            g_o_text, g_o_score_text, g_o_score, g_o_name, text_input = y

        if won:
            y = won_render(score)
            g_o_text, g_o_score_text, g_o_score, g_o_name, text_input = y

        while game_over or won:
            events: list[Event] = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    won, game_over, running = False, False, False
            g_o_generate(screen, g_o_text,
                         g_o_score_text, g_o_score,
                         g_o_name, text_input, events)
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_RETURN] and
                    len(text_input.value) < 10 and
                    len(text_input.value) > 0):
                name = text_input.value
                register_highscore('highscores.json', name, score)
                game_over, main_title = back_to_title(config,
                                                      (config['side']
                                                       [config['level']]),
                                                      player_coord)
                won = False
            clock.tick(config['tick'])

    pygame.quit()
