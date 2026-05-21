import time
import pygame
from abc import ABC, abstractmethod
from srcs.structs import Graph
from srcs.structs.drone import Drone


class GameEngine:
    """Fly-In Engine, generate a pygame instance to visualize drone travels

    Returns:
        An instance of GameEngine
    """
    screen: pygame.Surface
    network: Graph
    status: str = "title"
    level: str = ""
    infos: dict[str, dict[str, str]] = dict()
    graph: dict[str, dict[str, int]] = dict()

    def __init__(self, width: int, height: int) -> None:
        """Initiates the GameEngine

        Args:
            width (int):
            height (int):
        """
        pygame.init()
        pygame.display.set_caption("Fly-In")
        self.clock = pygame.time.Clock()
        self.status = "title"
        self.can_solve = True
        self.solved = False
        self.timer_solve: float = 0
        self.turns = 0
        GameEngine.screen = pygame.display.set_mode((width, height))

    def game_loop(self) -> None:
        """Manages the game loop by doing multiple status check and
        updating the screen
        """
        running = True
        group: GameEngine.Scene = GameEngine.MenuScene()
        while running:
            moving = [drone
                      for drone in Drone.drones
                      if drone.has_moved]
            if moving:
                for drone in moving:
                    drone.move(int((time.time() - self.timer_solve)*20))
            events = pygame.event.get()
            keys = pygame.key.get_pressed()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                try:
                    if GameEngine.status == "load":
                        self.new_network()
                        group = GameEngine.LevelScene(GameEngine.infos,
                                                      GameEngine.graph)
                        for drone in Drone.drones:
                            drone.init_image()
                            group.add(drone)
                        group.add(GameEngine.Turns())
                        GameEngine.status = "level"
                except ValueError:
                    print("Config file not valid. Please try another file"
                          " or fix this one.")
                    GameEngine.status = "title"
                if GameEngine.status == "level":
                    if keys[pygame.K_ESCAPE] or self.solved:
                        group = GameEngine.MenuScene()
                        GameEngine.Turns.turn = 0
                        self.solved = False
                        break
                    if time.time() - self.timer_solve >= 1:
                        self.can_solve = not self.can_solve
                        self.timer_solve = 0
                    if keys[pygame.K_SPACE] and self.can_solve:
                        GameEngine.Turns.turn += 1
                        self.solve_turn()
            if GameEngine.status != "load":
                self.screen.fill((50, 50, 101))
                group.update()
                group.draw(self.screen)
                pygame.display.flip()
        pygame.quit()

    def solve_turn(self) -> None:
        """When space is pressed, makes all drones moves (if possible)
        """
        turn_string: str = ""
        for drone in Drone.drones:
            turn_string += drone.best_choice()
        Drone.reset_turn_dicts()
        print(f"{turn_string}")
        if not turn_string:
            self.solved = True
        self.can_solve = not self.can_solve
        self.timer_solve = time.time()

    def new_network(self) -> None:
        """When a level title is clocked, a new graph is created
        """
        from srcs.parser import config_parser
        from srcs.structs import Graph, Drone
        Graph.full_reset()
        Drone.full_reset()
        GameEngine.GameHub.clear_hubs()
        path_to_file = f"maps/maps/{GameEngine.level}"
        graph, infos, couple = config_parser(path_to_file)
        network = Graph(graph, infos, couple)
        GameEngine.network = network
        # print("\033c")
        # nb_turns = network.solve_network()
        # print(f"Number of turns: {nb_turns}")
        # self.enable = not self.enable
        GameEngine.infos = network.infos()
        GameEngine.graph = network.graph()

    class GameConnection(pygame.sprite.Sprite):
        """Pygame sprite representing a connection between 2 vertices

        Args:
            pygame (_type_):
        """
        def __init__(self, hub_1: pygame.Rect, hub_2: pygame.Rect):
            """Initiates a connection sprite

            Args:
                hub_1 (pygame.Rect):_description_
                hub_2 (pygame.Rect):_description_
            """
            super().__init__()
            x = abs(hub_1.x - hub_2.x) + 10
            y = abs(hub_1.y - hub_2.y) + 10
            self.image = pygame.Surface((x, y))
            self.image.set_colorkey('black')
            self.image.convert_alpha()
            self.image.fill((0, 0, 0))
            rec_x = min(hub_1.x, hub_2.x)
            rec_y = min(hub_1.y, hub_2.y)
            self.rect = self.image.get_rect(topleft=(rec_x + 95, rec_y + 20))
            start_x = 0 if hub_1.x < hub_2.x else x - 10
            start_y = 0 if hub_1.y < hub_2.y else y - 10
            end_x = 0 if hub_2.x < hub_1.x else x - 10
            end_y = 0 if hub_2.y < hub_1.y else y - 10
            pygame.draw.line(self.image, (1, 1, 1),
                             (start_x, start_y),
                             (end_x, end_y),
                             10)

    class Turns(pygame.sprite.Sprite):
        """Manages the display of turns passed when drones move

        Args:
            pygame (_type_):
        """
        turn = 0

        def __init__(self) -> None:
            """Initiates the turn display
            """
            super().__init__()
            self.image = pygame.Surface((200, 150))
            self.image.set_colorkey('black')
            self.image.convert_alpha()
            self.image.fill((0, 0, 0))
            self.rect = self.image.get_rect()
            self.font = pygame.font.SysFont("Comic Sans MS", 50)
            self.textSurf = self.font.render(f"Turn: {GameEngine.Turns.turn}",
                                             False, (255, 255, 255))
            W, H = self.textSurf.get_width(), self.textSurf.get_height()
            self.image.blit(self.textSurf, [W/2, H/2])

        def update(self) -> None:
            """Updates the number of turns when space is pressed
            """
            self.image.fill((0, 0, 0))
            self.textSurf = self.font.render(f"Turn: {GameEngine.Turns.turn}",
                                             False, (255, 255, 255))
            W, H = self.textSurf.get_width(), self.textSurf.get_height()
            self.image.blit(self.textSurf, [W/2, H/2])

    class GameHub(pygame.sprite.Sprite):
        """Pygame sprite representing a hub/vertex

        Args:
            pygame (_type_):

        Returns:
            _type_:
        """
        hubs: list["GameEngine.GameHub"] = []

        def __init__(self, coord: tuple[int, int],
                     max_coo: tuple[int, int],
                     min_coo: tuple[int, int],
                     color: str,
                     name: str):
            """Instantiates a vertex

            Args:
                coord (tuple[int, int]):_description_
                max_coo (tuple[int, int]):_description_
                min_coo (tuple[int, int]):_description_
                color (str):_description_
                name (str):_description_
            """
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
                "darkred": (139, 0, 0),
                "violet": (238, 130, 238),
                "crimson": (220, 20, 60),
                "rainbow": (50, 50, 50)
                }
            self.image = pygame.Surface((200, 150))
            self.font = pygame.font.SysFont("Comic Sans MS", 23)
            self.image.set_colorkey('black')
            self.image.convert_alpha()
            self.image.fill((0, 0, 0))
            x = (coord[0]-min_coo[0]) * (1820/((max_coo[0]-min_coo[0])+1))
            y = (coord[1]-min_coo[1]) * (880/((max_coo[1]-min_coo[1])+1))
            self.rect = self.image.get_rect(topleft=(x, y + 75))
            pygame.draw.circle(self.image, self.colors[color], (100, 25), 25)
            if color == "rainbow":
                pygame.draw.circle(self.image, self.colors["red"], (100, 25),
                                   25, draw_top_right=True)
                pygame.draw.circle(self.image, self.colors["cyan"], (100, 25),
                                   25, draw_bottom_right=True)
                pygame.draw.circle(self.image, self.colors["green"], (100, 25),
                                   25, draw_top_left=True)
                pygame.draw.circle(self.image, self.colors["magenta"],
                                   (100, 25), 25, draw_bottom_left=True)
            pygame.draw.circle(self.image, (1, 1, 1), (100, 25), 25, 4)
            self.textSurf = self.font.render(name, False, (255, 255, 255))
            self.name = name
            W, H = self.textSurf.get_width(), self.textSurf.get_height()
            self.image.blit(self.textSurf, [100 - W/2, 75 - H/2])
            GameEngine.GameHub.hubs.append(self)

        @classmethod
        def get_hub(cls, name: str) -> "GameEngine.GameHub":
            """Returns a hub to get its position for drone movements

            Args:
                name (str):

            Returns:
                GameEngine.GameHub:
            """
            lst = []
            for hub in cls.hubs:
                if hub.name == name:
                    lst.append(hub)
            return lst[0]

        @classmethod
        def clear_hubs(cls) -> None:
            """Destroys all hubs existing
            """
            cls.hubs.clear()

    class Scene(ABC):
        def __init__(self) -> None:
            """instantiates a scene
            """
            pass

        @abstractmethod
        def update(self) -> None:
            """abstract
            """
            pass

        @abstractmethod
        def draw(self, screen: pygame.Surface) -> None:
            """abstract

            Args:
                screen (pygame.Surface):_description_
            """
            pass

    class LevelScene(Scene):
        """Manage a scene with all GameConnection and GameHub

        Args:
            Scene (_type_):
        """
        def __init__(self, infos: dict[str, dict[str, str]],
                     graph: dict[str, dict[str, int]]):
            """instantiates a scene

            Args:
                infos (dict[str, dict[str, str]]):
                graph (dict[str, dict[str, int]]):
            """
            coordinates = [key["coordinates"] for key in infos.values()]
            max_x = max([int(coord[0]) for coord in coordinates])
            max_y = max([int(coord[1]) for coord in coordinates])
            min_x = min([int(coord[0]) for coord in coordinates])
            min_y = min([int(coord[1]) for coord in coordinates])
            list_hubs: list[pygame.sprite.Sprite] = []
            for key, value in infos.items():
                str_coord = value["coordinates"]
                coords = (int(str_coord[0]), int(str_coord[1]))
                list_hubs.append(GameEngine.GameHub(coords,
                                                    (max_x, max_y),
                                                    (min_x, min_y),
                                                    value["color"],
                                                    key))
            for key2, value2 in graph.items():
                hub_1 = GameEngine.GameHub.get_hub(key2)
                for hub in value2:
                    hub_2 = GameEngine.GameHub.get_hub(hub)
                    list_hubs.insert(0,
                                     GameEngine.GameConnection(hub_1.rect,
                                                               hub_2.rect))
            self.group = pygame.sprite.Group(list_hubs)  # type: ignore

        def update(self) -> None:
            """update each element of the group
            """
            self.group.update()

        def add(self, args: pygame.sprite.Sprite) -> None:
            """adds one element to the group

            Args:
                args (pygame.sprite.Sprite):
            """
            self.group.add(args)

        def draw(self, screen: pygame.Surface) -> None:
            """draws the groupd on the screen

            Args:
                screen (pygame.Surface):
            """
            self.group.draw(screen)

    class MenuScene(Scene):
        """Manages the Menu scene with all levels clickable buttons

        Args:
            Scene (_type_):
        """
        def __init__(self) -> None:
            """instantiates the menu scene
            """
            self.group = pygame.sprite.Group([
                GameEngine.LevelTitle(
                    180, 300, 250, 70, "easy/01_linear_path.txt"),
                GameEngine.LevelTitle(
                    180, 435, 250, 70, "easy/02_simple_fork.txt"),
                GameEngine.LevelTitle(
                    180, 570, 250, 70, "easy/03_basic_capacity.txt"),
                GameEngine.LevelTitle(
                    510, 300, 250, 70, "medium/01_dead_end_trap.txt"),
                GameEngine.LevelTitle(
                    510, 435, 250, 70, "medium/02_circular_loop.txt"),
                GameEngine.LevelTitle(
                    510, 570, 250, 70, "medium/03_priority_puzzle.txt"),
                GameEngine.LevelTitle(
                    840, 300, 250, 70, "hard/01_maze_nightmare.txt"),
                GameEngine.LevelTitle(
                    840, 435, 250, 70, "hard/02_capacity_hell.txt"),
                GameEngine.LevelTitle(
                    840, 570, 250, 70, "hard/03_ultimate_challenge.txt"),
                GameEngine.LevelTitle(
                    1170, 300, 250, 70,
                    "challenger/01_the_impossible_dream.txt"),
                GameEngine.LevelTitle(
                    1500, 300, 250, 70, "custom/01_easy_1.txt"),
                GameEngine.LevelTitle(
                    1500, 435, 250, 70, "custom/02_easy_2.txt"),
                GameEngine.LevelTitle(
                    1500, 570, 250, 70, "custom/03_easy_3.txt"),
                GameEngine.LevelTitle(
                    1500, 705, 250, 70, "custom/04_medium_1.txt"),
                GameEngine.LevelTitle(
                    1500, 840, 250, 70, "custom/05_hard_1.txt")
                                                ])

        def update(self) -> None:
            """updates the menu if the mouse hover a button
            """
            self.group.update()

        def draw(self, screen: pygame.Surface) -> None:
            """draws the menu on the screen

            Args:
                screen (pygame.Surface):
            """
            self.group.draw(screen)

    class LevelTitle(pygame.sprite.Sprite):
        """A button for one level

        Args:
            pygame (_type_):
        """
        def __init__(self,
                     x: int, y: int,
                     width: int, height: int,
                     title: str) -> None:
            """Instantiates a button

            Args:
                x (int):
                y (int):
                width (int):
                height (int):
                title (str):
            """
            super().__init__()
            self.font = pygame.font.SysFont("Comic Sans MS", 30)
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
            self.text = title
            self.textSurf = self.font.render(
                title[title.index("_") + 1:title.rindex(".")],
                False, (1, 0, 0))
            W, H = self.textSurf.get_width(), self.textSurf.get_height()
            self.image.blit(self.textSurf, [width/2 - W/2, height/2 - H/2])

        def update(self) -> None:
            """Update the button color/action if its hovered.clicked
            """
            width, height = self.image.get_width(), self.image.get_height()
            W, H = self.textSurf.get_width(), self.textSurf.get_height()
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0] and not self.enable:
                    GameEngine.status = "load"
                    GameEngine.level = self.text
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
