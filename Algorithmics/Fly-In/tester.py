from srcs.parser import config_parser
from srcs.structs import Graph, Drone


def main() -> None:
    path_to_files = "maps/maps/medium/"
    graph, infos = config_parser(f"{path_to_files}03_priority_puzzle.txt")
    start: str = [n for n in graph if "start" in n][0]
    goal: str = [n for n in graph if "goal" in n][0]
    g = Graph(graph, infos)
    S = Graph.get_node(start)
    for i in range(S.max_drones):
        S.drones.append(Drone(i, start))
    drones = Drone.drones
    goal_hub = Graph.get_node(goal)
    nb_turns: int = 0
    while len(goal_hub.drones) < goal_hub.max_drones:
        nb_turns += 1
        for drone in drones:
            drone.move(g.get_paths(drone.path))
            print(f"{drone.number}: {drone.path}")
    print(f"Number of turns: {nb_turns}")


if __name__ == "__main__":
    main()
