from typing import Any
from .hub import NextHubInfos, Hub, Zones


class Graph:
    nodes: list[Hub] = []

    def __init__(self,
                 graph: dict[str, dict[str, int]],
                 infos: dict[str, dict[str, Any]]):
        Graph.nodes = self._create_hubs(infos)
        self._narc_nodes(graph, infos)
        # for node in self.nodes:
        #     print(node.name, node.zone, node.color)

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
                    graph: dict[str, dict[str, int]],
                    infos: dict[str, dict[str, Any]]) -> None:
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
