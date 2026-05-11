from srcs.parser import config_parser
from srcs.structs import Graph


def main() -> None:
    path_to_files = "maps/custom.txt"
    graph, infos, couple = config_parser(path_to_files)
    network = Graph(graph, infos, couple)
    nb_turns = network.solve_network()
    print(f"Number of turns: {nb_turns}")


if __name__ == "__main__":
    main()
