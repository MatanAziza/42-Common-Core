import pygame


class Drone(pygame.sprite.Sprite):
    """Drone Docstring
    """
    drones: list["Drone"] = []
    moving_drones: list["Drone"] = []
    max_paths: dict[str, tuple[int, int]] = dict()
    max_hubs: dict[str, tuple[int, int]] = dict()

    def __init__(self, number: int, start: str):
        """A Drone numbered, and with its start position

        Args:
            number (int): _description_
            start (str): _description_
        """
        super().__init__()
        self.number: int = number
        self.path: list[str] = [start]
        self.restricted = False
        self.turns: int = 0
        self.has_moved = False
        Drone.drones.append(self)

    def init_image(self) -> None:
        from srcs.game_engine import GameEngine
        start = self.path[0]
        self.image = pygame.image.load("srcs/drone.png")
        start_gamehub = GameEngine.GameHub.get_hub(start)
        rect = start_gamehub.rect
        self.rect = (rect[0]+75, rect[1], rect[2], rect[3])
        self.pos = (self.rect[0], self.rect[1])

    @classmethod
    def full_reset(cls) -> None:
        cls.drones.clear()
        cls.max_hubs.clear()
        cls.max_paths.clear()

    def move(self, number: int) -> None:
        from srcs.game_engine.flyin_engine import GameEngine
        previous_hub = GameEngine.GameHub.get_hub(self.path[-2])
        current_hub = GameEngine.GameHub.get_hub(self.path[-1])
        prev_rect = previous_hub.rect
        curr_rect = current_hub.rect
        x = int(self.pos[0] + ((curr_rect[0] - prev_rect[0]) * number) / 30)
        y = int(self.pos[1] + ((curr_rect[1] - prev_rect[1]) * number) / 30)
        self.rect = (x, y, self.rect[2], self.rect[3])
        if number == 30:
            self.has_moved = not self.has_moved
            self.pos = (x, y)

    def best_choice(self) -> str:
        from srcs.structs import Graph, NextHubInfos
        return_string = ""
        if self.path[-1] == Graph.goal:
            return return_string
        better_path = self.better_path()
        next_index = better_path.index(self.path[-1]) + 1

        current_hub = Graph.get_node(self.path[-1])
        next_hub = Graph.get_node(better_path[next_index])
        # Hubs from one to another the drone goes

        next: NextHubInfos = current_hub.next_hubs[next_hub.name]
        lesser_drone = [next.max_drones, next.max_link_capacity]
        key_link: str = f"{current_hub.name}-{next_hub.name}"
        old_path_max = Drone.max_paths.get(key_link, (0, min(lesser_drone)))
        current_hub_max = Drone.max_hubs.get(current_hub.name,
                                             (len(current_hub.drones),
                                              current_hub.max_drones))
        next_hub_max = Drone.max_hubs.get(next_hub.name, (0, next.max_drones))
        # Get actual values of traffic through link and hubs

        if (next_hub_max[0] < next_hub_max[1] and
           old_path_max[0] < old_path_max[1] and
           not self.restricted):
            self.turns += 2 if next.zone == 1 else 1
            Drone.max_paths.update({key_link: (old_path_max[0] + 1,
                                               old_path_max[1])})
            Drone.max_hubs.update({next_hub.name: (next_hub_max[0] + 1,
                                                   next_hub_max[1])})
            Drone.max_hubs.update({current_hub.name: (current_hub_max[0] - 1,
                                                      current_hub_max[1])})
            current_hub.drones.remove(self)
            next_hub.drones.append(self)
            self.path.append(next_hub.name)
            current_hub = next_hub
            return_string += f"D{self.number}-{current_hub.name} "
            self.has_moved = True
        if current_hub.zone.value == 1:
            self.restricted = not self.restricted
        return return_string

    @classmethod
    def moving(cls) -> list["Drone"]:
        return cls.moving_drones

    @classmethod
    def reset_turn_dicts(cls) -> None:
        from srcs.structs import Graph
        for key, value in Drone.max_paths.items():
            Drone.max_paths.update({key: (0, value[1])})
        for key, value in Drone.max_hubs.items():
            new_hub = Graph.get_node(key)
            Drone.max_hubs.update({key: (len(new_hub.drones), value[1])})

    def better_path(self) -> list[str]:
        from srcs.structs import Graph
        from srcs.path_finder import path_turns, path_avg_drone
        from srcs.path_finder import path_priorities
        from functools import partial
        basic_path = Graph.get_paths(self.path)[0]
        current_hub = Graph.get_node(self.path[-1])
        better_paths: list[list[str]] = []
        for next in current_hub.next_hubs.keys():
            if next not in self.path:
                graph = Graph.get_paths(self.path + [next])
                if graph:
                    better_paths.append(graph[0][len(self.path):])
        # All paths starting with self.path
        for path in better_paths.copy():
            link = Drone.max_paths.get(f"{self.path[-1]}-{path[0]}",
                                       (-1, -1))
            hub = Drone.max_hubs.get(path[0], (-1, -1))
            if link == (-1, -1) or hub == (-1, -1):
                continue
            if link[0] >= link[1] or hub[0] >= hub[1]:
                better_paths.remove(path)
        if not better_paths:
            return basic_path
        path_prio = partial(path_priorities,
                            max([len(path) for path in better_paths]))
        better_paths.sort(key=path_avg_drone, reverse=True)
        better_paths.sort(key=path_prio, reverse=True)
        better_paths.sort(key=path_turns)
        turns_better = path_turns(better_paths[0]) - self.turns
        d_index, after = self.get_drone_index(better_paths[0])
        if (d_index + path_turns(basic_path[len(self.path):]) < turns_better
           and after + path_turns(basic_path[len(self.path):]) < turns_better):
            return basic_path
        return self.path + better_paths[0]

    def get_drone_index(self, basic_path: list[str]) -> tuple[int, int]:
        from srcs.structs import Graph
        next_hub = Graph.get_node(basic_path[0])
        incoming_hubs = [connection
                         for connection in Drone.max_paths
                         if next_hub.name in connection
                         and connection.index(next_hub.name) != 0]
        incoming_hubs = [hub[:hub.index("-")] for hub in incoming_hubs]
        if self.path[-1] not in incoming_hubs:
            incoming_hubs.append(self.path[-1])
        incoming_drones: list[int] = []
        for hub in incoming_hubs:
            obj = Graph.get_node(hub)
            incoming_drones.extend([drone.number for drone in obj.drones])
        incoming_drones.extend([drone.number for drone in next_hub.drones])
        if not incoming_drones:
            return 0, 0
        incoming_drones.sort()
        self_index = incoming_drones.index(self.number)
        after_me = len(incoming_drones[self_index+1:])
        return self_index, after_me
