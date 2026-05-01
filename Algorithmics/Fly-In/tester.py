from srcs.parser import config_parser, graph_cleaner, graph_find_useless
from srcs.structs import Graph
from srcs.path_finder import path_finding

if __name__ == "__main__":
    path_to_files = "maps/maps/challenger/"
    graph, infos = config_parser(f"{path_to_files}01_the_impossible_dream.txt")
    start: str
    goal: str
    for node in graph:
        start = node if "start" in node else "start"
        goal = node if "goal" in node else "goal"
    print(start, goal)
    to_remove = graph_find_useless(start, goal, graph)
    final = graph_cleaner(start, goal, graph, to_remove)
    print(f"Useless paths: {set(graph.keys()) - set(final.keys()) != set()}")
    g = Graph(graph, infos)
    paths = path_finding(start, goal, graph)
    # print(paths)
    print([len(path) for path in paths])
