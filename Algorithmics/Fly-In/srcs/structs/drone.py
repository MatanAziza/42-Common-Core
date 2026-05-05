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
        self.arrived = False
        Drone.drones.append(self)

    def move(self, valid_paths: list[list[str]]) -> None:
        from srcs.structs import Graph, NextHubInfos
        if "goal" in self.path[-1]:
            self.arrived = True
            return
        current_path = valid_paths[0]
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
        if old_hub[0] < old_hub[1] and old_path[0] < old_path[1]:
            Drone.max_paths.update({couple_linked: (old_path[0] + 1,
                                                    old_path[1])})
            Drone.max_hubs.update({next_hub.name: (current_tuple[0] - 1,
                                                   current_tuple[1])})
            next_hub.drones.append(self)
            current_hub.drones.remove(self)
            self.path.append(next_hub.name)
        if self.number == Graph.get_node(self.path[0]).max_drones - 1:
            for key, value in Drone.max_paths.items():
                Drone.max_paths.update({key: (0, value[1])})
            for key, value in Drone.max_hubs.items():
                hub = Graph.get_node(key)
                Drone.max_hubs.update({key: (len(hub.drones), value[1])})
