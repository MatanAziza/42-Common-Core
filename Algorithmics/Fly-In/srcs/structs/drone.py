class Drone:
    """Drone Docstring
    """
    drones: list["Drone"] = []
    max_paths: dict[str, tuple[int, int]] = dict()
    max_hubs: dict[str, tuple[int, int]] = dict()

    def __init__(self, number: int, start: str):
        """A Drone numbered, and with its start position

        Args:
            number (int): _description_
            start (str): _description_
        """
        self.number: int = number
        self.path: list[str] = [start]
        self.restricted = False
        self.turns: int = 0
        Drone.drones.append(self)

    def move(self) -> None:
        from srcs.structs import Graph, NextHubInfos
        if self.path[-1] == Graph.goal:
            return
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
        if current_hub.zone.value == 1:
            self.restricted = not self.restricted
        if self.number == Graph.get_node(self.path[0]).max_drones - 1:
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
        # return self.path + better_paths[0]
        turns_better = path_turns(better_paths[0]) - self.turns
        drone_index = self.get_drone_index(basic_path)
        #FINISH GET INDEX
        if drone_index + path_turns(basic_path[len(self.path):]) >= turns_better:
            return self.path + better_paths[0]
        return basic_path

    def get_drone_index(self, basic_path: list[str]) -> int:
        from srcs.structs import Graph
        return 0
