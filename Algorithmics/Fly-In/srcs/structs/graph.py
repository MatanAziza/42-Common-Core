from typing import Any
from .hub import Hub, Zones


class Graph:
    def __init__(self,
                 graph: dict[str, dict[str, int]],
                 infos: dict[str, dict[str, Any]]):
        self.nodes: list[Hub] = self._create_hubs(infos)
        self._narc_nodes(graph, infos)
        # for node in self.nodes:
        #     print(node.name, node.zone, node.color)

    def _create_hubs(self, graph: dict[str, dict[str, int]]) -> list[Hub]:
        nodes: list[Hub] = []
        for key, value in graph.items():
            typ: Zones = Zones.NORMAL
            for zone in Zones:
                if value.get("zone", "error") == zone.value["type"]:
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
        for node in self.nodes:
            next_hubs: dict[str, dict[str, int | Zones]] = dict()
            connected: dict[str, int] = graph[node.name]
            for name, path in connected.items():
                hub = self.get_node(name)
                next_hubs.update(
                    {name:
                     {"max_drones": hub.max_drones,
                      "max_link_capacity": path,
                      "priority": hub.zone}}
                )
            node.next_hubs = next_hubs

    def get_node(self, name: str) -> Hub:
        return [hub for hub in self.nodes if hub.name == name][0]
