from srcs.parser import config_parser, graph_cleaner, graph_find_useless
from srcs.structs import Graph
from srcs.path_finder import path_finding, path_priorities
from functools import partial

def main() -> None:
    path_to_files = "maps/maps/hard/"
    graph, infos = config_parser(f"{path_to_files}01_maze_nightmare.txt")
    start: str = [n for n in graph if "start" in n][0]
    goal: str = [n for n in graph if "goal" in n][0]
    to_remove = graph_find_useless(start, goal, graph, infos)
    graph, infos = graph_cleaner(start, goal, graph, infos, to_remove)
    g = Graph(graph, infos)
    paths = path_finding([start], goal, graph)
    print([len(lst) for lst in paths])
    std = sorted(paths, key=path_priorities)
    print([len(lst) for lst in std])

if __name__ == "__main__":
    main()