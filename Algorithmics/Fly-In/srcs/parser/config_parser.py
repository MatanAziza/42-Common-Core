from typing import Any


def graph_maker(couples: list[list[str]]) -> dict[str, dict[str, int]]:
    graph: dict[str, dict[str, int]] = dict()
    for line in couples:
        graph.update(
            {line[1][:line[1].index(" ")]: dict()}
                    ) if "hub" in line[0] else 0
    connections = [connection[1]
                   for connection in couples
                   if "connection" in connection[0]]
    for connection in connections:
        data = connection.split(" ")
        data.append("[max_link_capacity=1]") if len(data) == 1 else 0
        nodes = data[0].split("-")
        graph[nodes[0]].update({nodes[1]: int(data[1].split("=")[1][:-1])})
        graph[nodes[1]].update({nodes[0]: int(data[1].split("=")[1][:-1])})
    return graph


def nodes_params(couples: list[list[str]],
                 couple: tuple[str, str]) -> dict[str, dict[str, Any]]:
    infos: dict[str, dict[str, Any]] = dict()
    alpha: dict[str, list[str]] = dict()
    start_drone: int = 1
    for line in couples:
        if line[0] == "nb_drones":
            start_drone = int(line[1])
        alpha.update(
            {line[1][:line[1].index(" ")]:
             line[1][line[1].index(" "):].strip().split(" ")}
                    ) if "hub" in line[0] else 0
    for key, value in alpha.items():
        meta = [v.strip("[]") for v in value[2:]]
        metadata = [(data.split("=")[0], data.split("=")[1]) for data in meta]
        infos[key] = {
            "coordinates": (value[0], value[1]),
                      }
        infos[key].update({k: v for k, v in metadata})
        if key in couple:
            infos[key].update({"max_drones": start_drone})
        if infos[key].get("color", "error") == "error":
            infos[key].update({"color": "white"})
    return infos


def start_end(couples: list[list[str]]) -> tuple[str, str]:
    start: str = "start"
    goal: str = "goal"
    for line in couples:
        if line[0] == "start_hub":
            start = line[1].split(" ")[0]
        if line[0] == "end_hub":
            goal = line[1].split(" ")[0]
    return (start, goal)


def config_parser(filename: str) -> tuple[
                                          dict[str, dict[str, int]],
                                          dict[str, dict[str, Any]],
                                          tuple[str, str]]:
    graph: dict[str, dict[str, int]] = dict()
    infos: dict[str, dict[str, Any]] = dict()

    with open(filename, "r") as file:
        lines = file.read().split("\n")
        couples = [line.split(": ")
                   for line in lines
                   if not line.startswith("#") and line]
        graph = graph_maker(couples)
        couple = start_end(couples)
        infos = nodes_params(couples, couple)
    return (graph, infos, couple)


if __name__ == "__main__":
    config_parser("maps/maps/hard/03_ultimate_challenge.txt")
