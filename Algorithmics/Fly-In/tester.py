from srcs.parser import config_parser, graph_cleaner, graph_find_useless
from srcs.structs import Graph

if __name__ == "__main__":
    # graph, infos = config_parser("01_linear_path.txt")
    graph, infos = config_parser("03_ultimate_challenge.txt")
    to_remove = graph_find_useless("start", "goal", graph)
    final = graph_cleaner("start", "goal", graph, to_remove)
    print(f"Useless paths: {set(graph.keys()) - set(final.keys()) != set()}")
    g = Graph(graph, infos)
    # for hub in g.nodes:
    #     print(hub.name, hub.zone, hub.next_hubs)
    #     print(graph[hub.name])
