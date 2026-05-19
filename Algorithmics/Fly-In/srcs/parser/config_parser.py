from typing import Any
import sys


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
            "coordinates": (int(float(value[0])), int(float(value[1]))),
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


def config_checker(filename: str) -> bool:
    try:
        with open(filename, "r") as file:
            lines = file.read().split('\n')
            lines = [line for line in lines if not line.startswith("#")]
            if not lines[0].startswith("nb_drones:"):
                raise FileExistsError("Config does not start with number"
                                      "of drones.")
            nb_drones = int(lines[0].split(":")[1].strip())
            nb_drones += 0
            st_end = [line for line in lines
                    if line.startswith("start_hub") or
                    line.startswith("end_hub")]
            if len(st_end) < 2:
                raise FileExistsError("Missing start/end hub.")
            st_end = [line for line in lines
                    if line.startswith("start_hub")]
            if len(st_end) != 1:
                raise FileExistsError("Wrong number of start/end hub.")
            goal = [line for line in lines
                    if line.startswith("end_hub")][0]
            hubs_infos = [line.split(": ")[1]
                          for line in lines[:lines.index(goal) + 1]
                          if "hub:" in line]
            hubs = [hub.split(" ")[0] for hub in hubs_infos]
            coordinates = [hub.split(" ")[1:3] for hub in hubs_infos]
            if len(hubs) != len(set(hubs)):
                raise FileExistsError("Hub name doubled. Please provide "
                                      "unique hub names.")
            for coordinate in coordinates:
                if (float(coordinate[0]) != int(float(coordinate[0])) or
                   float(coordinate[1]) != int(float(coordinate[1]))):
                    raise FileExistsError("Wrong type of coordinate: Float")
            connections_infos = [line.split(": ")[1]
                                 for line in lines[lines.index(goal) + 1:]
                                 if "connection:" in line]
            connections = [conn.split(" ")[0] for conn in connections_infos]
            for connection in connections:
                elems = reversed(connection.split("-"))
                for elem in elems:
                    if elem not in hubs:
                        raise FileExistsError("Hub connection not possible: "
                                              "Hub not mentionned earlier.")
                if "-".join(elems) in connections:
                    raise FileExistsError("Connection already mentionned in "
                                          "the list. Please avoid repetitions")
            return True
    except FileNotFoundError:
        print("File does not exists. Please provide a valid file.")
    except ValueError:
        print("String value given instead of convertible. Please fix.")
    except FileExistsError as e:
        print(e)
    return False


def config_parser(filename: str) -> tuple[
                                          dict[str, dict[str, int]],
                                          dict[str, dict[str, Any]],
                                          tuple[str, str]]:
    graph: dict[str, dict[str, int]] = dict()
    infos: dict[str, dict[str, Any]] = dict()
    is_config_good = config_checker(filename)
    if not is_config_good:
        return ({}, {}, ("", ""))
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
