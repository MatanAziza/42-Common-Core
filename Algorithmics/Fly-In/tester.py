from srcs.parser import config_parser, graph_cleaner, graph_find_useless
from srcs.structs import Graph
from srcs.path_finder import path_finding, path_priorities, path_time
from functools import partial
import random

def main() -> None:
    path_to_files = "maps/maps/medium/"
    graph, infos = config_parser(f"{path_to_files}03_priority_puzzle.txt")
    start: str = [n for n in graph if "start" in n][0]
    goal: str = [n for n in graph if "goal" in n][0]
    to_remove = graph_find_useless(start, goal, graph, infos)
    graph, infos = graph_cleaner(start, goal, graph, infos, to_remove)
    g = Graph(graph, infos)
    paths = path_finding([start], goal, graph)
    paths.sort(key=path_priorities, reverse=True)
    paths.sort(key=path_time)
    print([lst for lst in paths])

if __name__ == "__main__":
    main()