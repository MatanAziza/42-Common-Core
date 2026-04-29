from hub import Hub, Zones
from config_parser import config_parser
from graph_operations import graph_cleaner, graph_find_useless

class Graph:
    def __init__(self,
                 graph: dict[str, set[str]],
                 infos: dict[str, dict[str, any]]):
        self.nodes: list[Hub] = self._create_hubs(graph)
        for node in self.nodes:
            print(node.name)

    def _create_hubs(self, graph: dict[str, set[str]]) -> list[Hub]:
        nodes: list[Hub] = []
        for key, value in graph.items():
            typ: Zones = Zones.NORMAL
            for zone in Zones:
                if value["zone"] == zone.value["type"]:
                    typ = zone
                    break
            nodes.append(Hub(key, typ, value["color"], value["max_drones"]))
        return nodes
    
if __name__ == "__main__":
    graph, infos = config_parser("01_linear_path.txt")
    # graph, infos = config_parser("03_ultimate_challenge.txt")
    from graph_operations import graph_cleaner, graph_find_useless
    to_remove = graph_find_useless("start", "goal", graph)
    final = graph_cleaner("start", "goal", graph, to_remove)
    print(f"Useless paths: {set(graph.keys()) - set(final.keys()) != set()}")