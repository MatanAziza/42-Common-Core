from typing import Any
from .hub import NextHubInfos, Hub, Zones
from .drone import Drone
from srcs.parser import graph_find_useless, graph_cleaner


class Graph:
    """Create a graph storing all its hubs

    Returns:
        _type_: _description_
    """
    nodes: list[Hub] = []
    paths: list[list[str]] = []
    start: str = ""
    goal: str = ""

    def __init__(self,
                 graph: dict[str, dict[str, int]],
                 infos: dict[str, dict[str, Any]],
                 couple: tuple[str, str]):
        """instantiates a graph

        Args:
            graph (dict[str, dict[str, int]]): _description_
            infos (dict[str, dict[str, Any]]): _description_
            couple (tuple[str, str]): _description_
        """
        from srcs.path_finder import path_finding
        self.start, self.goal = couple
        Graph.start, Graph.goal = couple
        self._true_infos = infos
        self._true_graph = graph
        to_remove = graph_find_useless(self.start, self.goal, graph, infos)
        graph, infos = graph_cleaner(self.start, self.goal,
                                     graph, infos, to_remove)
        Graph.nodes = self._create_hubs(infos)
        self._narc_nodes(graph)
        if graph:
            Graph.paths = path_finding([self.start], self.goal, graph)
            S = Graph.get_node(self.start)
            Drone.drones.clear()
            for i in range(S.max_drones):
                S.drones.append(Drone(i, self.start))
            self._graph = graph
            self._infos = infos

    @classmethod
    def full_reset(cls) -> None:
        """Reset all that is contained in a graph
        """
        cls.nodes.clear()
        cls.paths.clear()
        cls.start = ""
        cls.goal = ""

    def infos(self) -> dict[str, dict[str, Any]]:
        """returns original infos for flyin engine

        Returns:
            dict[str, dict[str, Any]]: _description_
        """
        return self._true_infos.copy()

    def graph(self) -> dict[str, dict[str, int]]:
        """returns original graph for flyin engine

        Returns:
            dict[str, dict[str, int]]: _description_
        """
        return self._true_graph.copy()

    def _create_hubs(self, graph: dict[str, dict[str, int]]) -> list[Hub]:
        """Based on the graph list, creates each Hub and add them to a list

        Args:
            graph (dict[str, dict[str, int]]):

        Returns:
            list[Hub]:
        """
        nodes: list[Hub] = []
        for key, value in graph.items():
            typ: Zones = Zones.NORMAL
            for zone in Zones:
                if value.get("zone", "error") == Zones.zone_name(zone):
                    typ = zone
                    break
            nodes.append(Hub(name=key,
                             zone=typ,
                             color=str(value.get("color", "white")),
                             max_drones=value.get("max_drones", 1))
                         )
        return nodes

    def _narc_nodes(self,
                    graph: dict[str, dict[str, int]]) -> None:
        """For each hub/node, looks for connected noddes infos,
        filling a NextHubInfo class.

        Args:
            graph (dict[str, dict[str, int]]):
            infos (dict[str, dict[str, Any]]):
        """
        for node in Graph.nodes:
            next_hubs: dict[str, NextHubInfos] = dict()
            connected: dict[str, int] = graph[node.name]
            for name, path in connected.items():
                hub = Graph.get_node(name)
                next_hubs.update(
                    {name:
                     NextHubInfos(hub.max_drones,
                                  path,
                                  hub.zone.value)
                     }
                )
            node.next_hubs = next_hubs

    @staticmethod
    def get_node(name: str) -> Hub:
        """Returns a Hub based on its name

        Args:
            name (str)

        Returns:
            Hub:
        """
        return [hub for hub in Graph.nodes if hub.name == name][0]

    @classmethod
    def get_paths(cls, start: list[str]) -> list[list[str]]:
        """returns a list of path starting with start parameter

        Args:
            start (list[str]): _description_

        Returns:
            list[list[str]]: _description_
        """
        valid_paths: list[list[str]] = []
        for path in cls.paths:
            index: int = 0
            is_valid: bool = True
            for i, node in enumerate(start):
                index += 1
                if node != path[i]:
                    is_valid = not is_valid
                    break
            if is_valid:
                valid_paths.append(path)
        return valid_paths.copy()
