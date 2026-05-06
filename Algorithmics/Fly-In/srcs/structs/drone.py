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

    def move(self, to_avoid: list[str] = []) -> None:
        from srcs.structs import Graph, NextHubInfos
        if Graph.goal == self.path[-1]:
            return
        current_path = Graph.get_paths(self.path, to_avoid)[0]
        current_hub = Graph.get_node(self.path[-1])
        next_index = current_path.index(self.path[-1]) + 1
        next_hub = Graph.get_node(current_path[next_index])
        next: NextHubInfos = current_hub.next_hubs[next_hub.name]
        lesser_drone = [next.max_drones, next.max_link_capacity]
        couple_linked: str = f"{current_hub.name}-{next_hub.name}"
        old_path = Drone.max_paths.get(couple_linked, (0, min(lesser_drone)))
        old_hub = Drone.max_hubs.get(next_hub.name, (0, next.max_drones))
        current_tuple = Drone.max_hubs.get(current_hub.name,
                                           (len(current_hub.drones),
                                            current_hub.max_drones))
        real_next = current_hub.next_hubs.copy()
        for hub in self.path:
            if hub in real_next.keys():
                real_next.pop(hub)
        if ((old_hub[0] >= old_hub[1] or
           old_path[0] >= old_path[1] or
           len(next_hub.drones) >= next_hub.max_drones) and
           len(real_next) > len(to_avoid) + 1 and
           next_hub.name != Graph.goal):
            self.move(to_avoid + [next_hub.name])
            return
        if (old_hub[0] < old_hub[1] and
           old_path[0] < old_path[1] and
           not self.restricted):
            self.turns += 2 if next.zone == 1 else 1
            Drone.max_paths.update({couple_linked: (old_path[0] + 1,
                                                    old_path[1])})
            Drone.max_hubs.update({next_hub.name: (current_tuple[0] - 1,
                                                   current_tuple[1])})
            next_hub.drones.append(self)
            current_hub.drones.remove(self)
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

    def worth_changing_path(self,
                            current_path: list[str],
                            nexts: list[str]) -> str:
        from srcs.structs import Graph
        from srcs.path_finder import path_turns, path_avg_drone
        paths = Graph.get_paths(self.path, nexts)
        better_path = paths[0]
        turns_left = path_turns(better_path) - self.turns
        last_drone = Drone.drones[-1].number
        gap_drone = (last_drone - self.number)
        gap_drone *= int(self.turns / (int(path_avg_drone(self.path) + 1)))
        turns_last_drone = path_turns(current_path)
        if turns_last_drone + gap_drone >= turns_left:
            return better_path[len(current_path):][0]
        return ""
