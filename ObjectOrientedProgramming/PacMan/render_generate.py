import pygame
from pygame.event import Event
from typing import Any
import pygame_textinput as py_text  # type: ignore[import-untyped]


def create_fonts() -> tuple[pygame.font.Font,
                            pygame.font.Font,
                            pygame.font.Font]:
    main_font = pygame.font.SysFont('Nimbus Mono PS', 70)
    reduced_font = pygame.font.SysFont('Nimbus Mono PS', 30)
    hs_font = pygame.font.SysFont('Nimbus Mono PS', 20)

    return (main_font, reduced_font, hs_font)


def main_title_render(highscores: list[list[Any]]
                      ) -> tuple[pygame.surface.Surface,
                                 pygame.surface.Surface,
                                 pygame.surface.Surface,
                                 list[pygame.surface.Surface],
                                 list[pygame.surface.Surface]]:
    main_font, reduced_font, hs_font = create_fonts()

    names: list[str] = []
    scores: list[int] = []
    for x in highscores:
        names.append(x[0])
        scores.append(x[1])

    mt_text = main_font.render('PAC-MAN', False, (255, 255, 0))
    play_text = reduced_font.render('Press SPACE to play', False,
                                    (255, 255, 0))
    leaderboard_text = reduced_font.render('Leaderboard', False, (255, 255, 0))

    name_0 = hs_font.render(names[0], False, (255, 255, 0))
    name_1 = hs_font.render(names[1], False, (255, 255, 0))
    name_2 = hs_font.render(names[2], False, (255, 255, 0))
    name_3 = hs_font.render(names[3], False, (255, 255, 0))
    name_4 = hs_font.render(names[4], False, (255, 255, 0))
    name_5 = hs_font.render(names[5], False, (255, 255, 0))
    name_6 = hs_font.render(names[6], False, (255, 255, 0))
    name_7 = hs_font.render(names[7], False, (255, 255, 0))
    name_8 = hs_font.render(names[8], False, (255, 255, 0))
    name_9 = hs_font.render(names[9], False, (255, 255, 0))

    score_0 = hs_font.render(str(scores[0]), False, (255, 255, 0))
    score_1 = hs_font.render(str(scores[1]), False, (255, 255, 0))
    score_2 = hs_font.render(str(scores[2]), False, (255, 255, 0))
    score_3 = hs_font.render(str(scores[3]), False, (255, 255, 0))
    score_4 = hs_font.render(str(scores[4]), False, (255, 255, 0))
    score_5 = hs_font.render(str(scores[5]), False, (255, 255, 0))
    score_6 = hs_font.render(str(scores[6]), False, (255, 255, 0))
    score_7 = hs_font.render(str(scores[7]), False, (255, 255, 0))
    score_8 = hs_font.render(str(scores[8]), False, (255, 255, 0))
    score_9 = hs_font.render(str(scores[9]), False, (255, 255, 0))

    list_names_text: list[Any] = []
    list_names_text.append(name_0)
    list_names_text.append(name_1)
    list_names_text.append(name_2)
    list_names_text.append(name_3)
    list_names_text.append(name_4)
    list_names_text.append(name_5)
    list_names_text.append(name_6)
    list_names_text.append(name_7)
    list_names_text.append(name_8)
    list_names_text.append(name_9)

    list_scores_text: list[Any] = []
    list_scores_text.append(score_0)
    list_scores_text.append(score_1)
    list_scores_text.append(score_2)
    list_scores_text.append(score_3)
    list_scores_text.append(score_4)
    list_scores_text.append(score_5)
    list_scores_text.append(score_6)
    list_scores_text.append(score_7)
    list_scores_text.append(score_8)
    list_scores_text.append(score_9)

    return (mt_text, play_text, leaderboard_text,
            list_names_text, list_scores_text)


def main_title_generate(screen: pygame.surface.Surface,
                        list_names: list[pygame.surface.Surface],
                        list_scores: list[pygame.surface.Surface],
                        mt_text: pygame.surface.Surface,
                        play_text: pygame.surface.Surface,
                        leaderboard_text: pygame.surface.Surface) -> None:

    screen.fill('black')

    screen.blit(mt_text, (180, 50))
    screen.blit(play_text, (170, 800))
    screen.blit(leaderboard_text, (230, 150))

    screen.blit(list_names[0], (50, 250))
    screen.blit(list_names[1], (50, 350))
    screen.blit(list_names[2], (50, 450))
    screen.blit(list_names[3], (50, 550))
    screen.blit(list_names[4], (50, 650))

    screen.blit(list_scores[0], (200, 250))
    screen.blit(list_scores[1], (200, 350))
    screen.blit(list_scores[2], (200, 450))
    screen.blit(list_scores[3], (200, 550))
    screen.blit(list_scores[4], (200, 650))

    screen.blit(list_names[5], (400, 250))
    screen.blit(list_names[6], (400, 350))
    screen.blit(list_names[7], (400, 450))
    screen.blit(list_names[8], (400, 550))
    screen.blit(list_names[9], (400, 650))

    screen.blit(list_scores[5], (550, 250))
    screen.blit(list_scores[6], (550, 350))
    screen.blit(list_scores[7], (550, 450))
    screen.blit(list_scores[8], (550, 550))
    screen.blit(list_scores[9], (550, 650))

    pygame.display.flip()


def l_s_render() -> pygame.surface.Surface:
    main_font, _, _ = create_fonts()

    loading_text = main_font.render('Loading', False, (255, 255, 255))

    return loading_text


def l_s_generate(screen: pygame.surface.Surface,
                 loading_text: pygame.surface.Surface) -> None:
    screen.fill('black')
    screen.blit(loading_text, (180, 500))


def ready_render() -> tuple[pygame.surface.Surface,
                            pygame.surface.Surface,
                            pygame.surface.Surface]:
    main_font, _, _ = create_fonts()

    ready_text = main_font.render('Ready ?', False, (255, 255, 255))
    set_text = main_font.render('Set', False, (255, 255, 255))
    go_text = main_font.render('GO !', False, (255, 255, 255))

    return (ready_text, set_text, go_text)


def ready_generate(screen: pygame.surface.Surface,
                   text: pygame.surface.Surface,
                   pos: int) -> None:

    poss = [(187, 400), (270, 400), (260, 400)]
    surface = pygame.Surface((660, 990)).convert_alpha()
    surface.fill((0, 0, 0, 0))
    screen.blit(surface, (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), ((187, 400), (286, 56)))
    screen.blit(text, poss[pos])

    pygame.display.flip()


def pause_render() -> tuple[pygame.surface.Surface,
                            pygame.surface.Surface,
                            pygame.surface.Surface]:
    main_font, reduced_font, hs_font = create_fonts()

    pause_text = main_font.render('Pause', False, (255, 255, 255))
    resume_text = reduced_font.render('Press R to resume', False,
                                      (255, 255, 255))
    back_text = hs_font.render('Press BACKSPACE to go back to main title',
                               False,
                               (255, 255, 255))

    return (pause_text, resume_text, back_text)


def pause_generate(screen: pygame.surface.Surface,
                   pause_text: pygame.surface.Surface,
                   resume_text: pygame.surface.Surface,
                   back_text: pygame.surface.Surface) -> None:

    surface = pygame.Surface((660, 990)).convert_alpha()
    surface.fill((0, 0, 0, 0))
    screen.blit(surface, (0, 0))

    pygame.draw.rect(screen, (0, 0, 0), ((220, 400), (205, 48)))
    screen.blit(pause_text, (220, 400))
    screen.blit(resume_text, (180, 850))
    screen.blit(back_text, (90, 900))

    pygame.display.flip()


def g_o_render(score: int) -> tuple[pygame.surface.Surface,
                                    pygame.surface.Surface,
                                    pygame.surface.Surface,
                                    pygame.surface.Surface,
                                    py_text.TextInputVisualizer]:
    main_font, reduced_font, _ = create_fonts()

    g_o_text = main_font.render('Game Over', False, (255, 0, 0))
    g_o_score_text = main_font.render('Score', False, (255, 0, 0))
    g_o_score = main_font.render(str(score), False, (255, 0, 0))
    g_o_name = reduced_font.render('Enter your name (max 10 characters)',
                                   False,
                                   (255, 0, 0))
    text_input = py_text.TextInputVisualizer()
    text_input.cursor_color = 'red'
    text_input.font_color = (255, 0, 0)
    return (g_o_text, g_o_score_text, g_o_score, g_o_name, text_input)


def g_o_generate(screen: pygame.surface.Surface,
                 g_o_text: pygame.surface.Surface,
                 g_o_score_text: pygame.surface.Surface,
                 g_o_score: pygame.surface.Surface,
                 g_o_name: pygame.surface.Surface,
                 g_o_text_input: py_text.pygame_textinput.TextInputVisualizer,
                 events: Event | list[Event]) -> None:

    screen.fill('black')

    screen.blit(g_o_text, (140, 100))
    screen.blit(g_o_score_text, (220, 300))
    screen.blit(g_o_score, (220, 400))
    screen.blit(g_o_name, (20, 600))

    g_o_text_input.update(events)
    screen.blit(g_o_text_input.surface, (250, 650))

    pygame.display.flip()


def won_render(score: int) -> tuple[pygame.surface.Surface,
                                    pygame.surface.Surface,
                                    pygame.surface.Surface,
                                    pygame.surface.Surface,
                                    py_text.TextInputVisualizer]:
    main_font, reduced_font, _ = create_fonts()

    g_o_text = main_font.render('You won !', False, (0, 255, 0))
    g_o_score_text = main_font.render('Score', False, (0, 255, 0))
    g_o_score = main_font.render(str(score), False, (0, 255, 0))
    g_o_name = reduced_font.render('Enter your name (max 10 characters)',
                                   False,
                                   (0, 255, 0))
    text_input = py_text.TextInputVisualizer()
    text_input.cursor_color = 'green'
    text_input.font_color = (0, 255, 0)
    return (g_o_text, g_o_score_text, g_o_score, g_o_name, text_input)


def hud_render(score: int,
               highest_score: int,
               timer: int) -> list[pygame.surface.Surface]:
    _, reduced_font, _ = create_fonts()

    score_text = reduced_font.render('Score', False, (255, 255, 255))
    score_nb = reduced_font.render(str(score), False, (255, 255, 255))

    h_s_text = reduced_font.render('Highscore', False, (255, 255, 255))
    h_s_nb = reduced_font.render(str(highest_score), False, (255, 255, 255))

    timer_text = reduced_font.render('Timer', False, (255, 255, 255))
    timer_nb = reduced_font.render(str(timer), False, (255, 255, 255))

    return [score_text, score_nb, h_s_text, h_s_nb, timer_text, timer_nb]


def hud_generate(screen: pygame.surface.Surface,
                 score_text: pygame.surface.Surface,
                 score_nb: pygame.surface.Surface,
                 h_s_text: pygame.surface.Surface,
                 h_s_nb: pygame.surface.Surface,
                 timer_text: pygame.surface.Surface,
                 timer_nb: pygame.surface.Surface,
                 lives: int) -> None:

    screen.blit(score_text, (500, 20))
    screen.blit(score_nb, (500, 50))
    screen.blit(h_s_text, (50, 20))
    screen.blit(h_s_nb, (50, 50))
    screen.blit(timer_text, (300, 20))
    screen.blit(timer_nb, (300, 50))

    if lives >= 1:
        pygame.draw.circle(screen, "yellow", (30, 820), 20)
    if lives >= 2:
        pygame.draw.circle(screen, "yellow", (80, 820), 20)
    if lives == 3:
        pygame.draw.circle(screen, "yellow", (130, 820), 20)
