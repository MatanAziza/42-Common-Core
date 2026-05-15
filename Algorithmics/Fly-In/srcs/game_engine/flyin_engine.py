import pygame
from abc import ABC, abstractmethod


class GameEngine:
    screen: pygame.Surface
    status: str = "title"
    infos: dict[str, dict[str, str]] = dict()

    def __init__(self, width: int, height: int) -> None:
        pygame.init()
        pygame.display.set_caption("Fly-In")
        self.clock = pygame.time.Clock()
        self.status = "title"
        GameEngine.screen = pygame.display.set_mode((width, height))

    def game_loop(self) -> None:
        running = True
        group = GameEngine.MenuScene()
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                if GameEngine.status != "load":
                    self.screen.fill((50, 50, 151))
                    group.update()
                    group.draw(self.screen)
                    pygame.display.flip()
                if GameEngine.status == "load":
                    group = GameEngine.LevelScene(GameEngine.infos)
                    GameEngine.status = "level"
        pygame.quit()

    class GameHub(pygame.sprite.Sprite):

        def __init__(self, coord: tuple[int, int],
                        max_coord: tuple[int, int], color: str):
            super().__init__()
            self.colors: dict[str, tuple[int, int, int]] = {
                "green": (0, 128, 0),
                "blue": (0, 0, 255),
                "red": (255, 0, 0),
                "yellow": (255, 255, 0),
                "orange": (255, 165, 0),
                "cyan": (0, 255, 255),
                "purple": (128, 0, 128),
                "magenta": (255, 0, 255),
                "lime": (0, 255, 0),
                "brown": (165, 42, 42),
                "gold": (255, 215, 0),
                "white": (255, 255, 255),
                "black": (0, 0, 0),
                "maroon": (128, 0, 0),
                "dark red": (139, 0, 0),
                "violet": (238, 130, 238),
                "crimson": (220, 20, 60)
                }
            self.image = pygame.Surface((50, 50))
            self.image.set_colorkey('black')
            self.image.convert_alpha()
            self.image.fill((0, 0, 0))
            nb_abs = (max_coord[0] - coord[0]) + 1
            nb_ord =(max_coord[1] - coord[1]) + 1
            x = coord[0] * 1720 * nb_abs / (max_coord[0]+1)
            y = coord[1] * 880 * nb_ord / (max_coord[1]+1)
            self.rect = self.image.get_rect(topleft=(x, y))
            pygame.draw.circle(self.image, self.colors[color], (x+25, y+25),
                            25)
            print(self.rect)

    class Scene(ABC):
        def __init__(self):
            pass

        @abstractmethod
        def update(self):
            pass

    class LevelScene(Scene):
        x_offset, y_offset = 100, 100

        def __init__(self, infos: dict[str, dict[str, str]]):
            coordinates = [key["coordinates"] for key in infos.values()]
            max_x = max([int(coord[0]) for coord in coordinates])
            max_y = max([int(coord[1]) for coord in coordinates])
            list_hubs: list[GameEngine.GameHub] = []
            for value in infos.values():
                str_coord = value["coordinates"]
                coords = (int(str_coord[0]), int(str_coord[1]))
                list_hubs.append(GameEngine.GameHub(coords, (max_x, max_y), value["color"]))
            self.group = pygame.sprite.Group(list_hubs)

        def update(self):
            self.group.update()

        def draw(self, screen: pygame.Surface):
            self.group.draw(screen)

    class MenuScene(Scene):
        def __init__(self):
            self.group = pygame.sprite.Group([
            GameEngine.LevelTitle(180, 300, 250, 70, "easy/01_linear_path.txt"),
            GameEngine.LevelTitle(180, 435, 250, 70, "easy/02_simple_fork.txt"),
            GameEngine.LevelTitle(180, 570, 250, 70, "easy/03_basic_capacity.txt"),
            GameEngine.LevelTitle(510, 300, 250, 70, "medium/01_dead_end_trap.txt"),
            GameEngine.LevelTitle(510, 435, 250, 70, "medium/02_circular_loop.txt"),
            GameEngine.LevelTitle(510, 570, 250, 70, "medium/03_priority_puzzle.txt"),
            GameEngine.LevelTitle(840, 300, 250, 70, "hard/01_maze_nightmare.txt"),
            GameEngine.LevelTitle(840, 435, 250, 70, "hard/02_capacity_hell.txt"),
            GameEngine.LevelTitle(840, 570, 250, 70, "hard/03_ultimate_challenge.txt"),
            GameEngine.LevelTitle(1170, 300, 250, 70,"challenger/01_the_impossible_dream.txt"),
            GameEngine.LevelTitle(1500, 300, 250, 70,"custom/01_easy_1.txt"),
            GameEngine.LevelTitle(1500, 435, 250, 70,"custom/02_easy_2.txt"),
            GameEngine.LevelTitle(1500, 570, 250, 70,"custom/03_easy_3.txt"),
            GameEngine.LevelTitle(1500, 705, 250, 70,"custom/04_medium_1.txt"),
            GameEngine.LevelTitle(1500, 840, 250, 70,"custom/05_hard_1.txt")
        ])

        def update(self):
            self.group.update()

        def draw(self, screen: pygame.Surface):
            self.group.draw(screen)


    class LevelTitle(pygame.sprite.Sprite):
        def __init__(self,
                     x: int, y: int,
                     width: int, height: int,
                     title: str) -> None:
            super().__init__()
            self.font = pygame.font.SysFont("Comic Sans MS", 30)
            self.text = title
            self.textSurf = self.font.render(
                title[title.index("_") + 1:title.rindex(".")],
                False, (1, 0, 0))
            W, H = self.textSurf.get_width(), self.textSurf.get_height()
            self.image = pygame.Surface((width, height))
            self.image.set_colorkey('black')
            self.image.convert_alpha()
            self.image.fill((0, 0, 0))
            self.enable = False
            self.rect = self.image.get_rect(topleft=(x, y))
            pygame.draw.rect(self.image, (201, 50, 0), self.image.get_rect(),
                             border_radius=20)
            pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect(),
                             2, 5)
            self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])

        def new_network(self) -> None:
            from srcs.parser import config_parser
            from srcs.structs import Graph, Drone
            Graph.full_reset()
            Drone.full_reset()
            path_to_file = f"maps/maps/{self.text}"
            graph, infos, couple = config_parser(path_to_file)
            network = Graph(graph, infos, couple)
            # print("\033c")
            nb_turns = network.solve_network()
            print([v["color"] for v in network.infos().values()])
            print(f"Number of turns: {nb_turns}")
            self.enable = not self.enable
            GameEngine.infos = network.infos()


        def update(self) -> None:
            width, height = self.image.get_width(), self.image.get_height()
            W, H = self.textSurf.get_width(), self.textSurf.get_height()
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0] and not self.enable:
                    self.new_network()
                    GameEngine.status = "load"
                pygame.draw.rect(self.image, (50, 201, 0),
                                 self.image.get_rect(),
                                 border_radius=20)
                pygame.draw.rect(self.image, (1, 0, 0),
                                 self.image.get_rect(),
                                 2, border_radius=20)
                self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])
            else:
                self.enable = False
                pygame.draw.rect(self.image, (201, 50, 0),
                                    self.image.get_rect(),
                                    border_radius=20)
                pygame.draw.rect(self.image, (1, 0, 0),
                                    self.image.get_rect(),
                                    2, border_radius=20)
                self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])
