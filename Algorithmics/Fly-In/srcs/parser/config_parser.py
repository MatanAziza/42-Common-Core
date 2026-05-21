from typing import Any


def graph_maker(couples: list[list[str]]) -> dict[str, dict[str, int]]:
    """Create a graph with each hub linked to a list of adjacent hubs
    and the maximum drones capable of being sent to the hub

    Args:
        couples (list[list[str]]): _description_

    Returns:
        dict[str, dict[str, int]]: _description_
    """
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
    """Returns all nodes infos (max drone, color), backing to default
    if missing info

    Args:
        couples (list[list[str]]): _description_
        couple (tuple[str, str]): _description_

    Returns:
        dict[str, dict[str, Any]]: _description_
    """
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
    """Returns the start and goal name

    Args:
        couples (list[list[str]]): _description_

    Returns:
        tuple[str, str]: _description_
    """
    start: str = "start"
    goal: str = "goal"
    for line in couples:
        if line[0] == "start_hub":
            start = line[1].split(" ")[0]
        if line[0] == "end_hub":
            goal = line[1].split(" ")[0]
    return (start, goal)


class ParsingError(Exception):
    """ParsingError custom

    Args:
        Exception (_type_): _description_
    """
    def __init__(self, message: str):
        super().__init__(message)


def config_checker(filename: str) -> bool:
    """Checks all possibles issues that could happen with the config
    file and returns False if one occurs

    Args:
        filename (str): _description_

    Raises:
        ParsingError: _description_
        ParsingError: _description_
        ParsingError: _description_
        ParsingError: _description_
        ParsingError: _description_
        ParsingError: _description_
        ParsingError: _description_
        ParsingError: _description_
        ParsingError: _description_
        ParsingError: _description_
        ParsingError: _description_
        ParsingError: _description_
        ParsingError: _description_
        IndexError: _description_

    Returns:
        bool: _description_
    """
    try:
        with open(filename, "r") as file:
            lines = file.read().split('\n')
            lines = [line for line in lines if not line.startswith("#")]
            if not lines[0].startswith("nb_drones:"):
                raise ParsingError("Config does not start with number"
                                   "of drones.")
            nb_drones = int(lines[0].split(":")[1].strip())
            nb_drones += 0
            st_end = [line for line in lines
                      if line.startswith("start_hub") or
                      line.startswith("end_hub")]
            if len(st_end) < 2:
                raise ParsingError("Missing start/end hub.")
            st_end = [line for line in lines
                      if line.startswith("start_hub")]
            if len(st_end) != 1:
                raise ParsingError("Wrong number of start/end hub.")
            goal = [line for line in lines
                    if line.startswith("end_hub")][0]
            hubs_infos = [line.split(": ")[1]
                          for line in lines[:lines.index(goal) + 1]
                          if "hub:" in line]
            hubs = [hub.split(" ")[0] for hub in hubs_infos]
            coordinates = [hub.split(" ")[1:3] for hub in hubs_infos]
            if len(hubs) != len(set(hubs)):
                raise ParsingError("Hub name doubled. Please provide "
                                   "unique hub names.")
            for coordinate in coordinates:
                if (float(coordinate[0]) != int(float(coordinate[0])) or
                   float(coordinate[1]) != int(float(coordinate[1]))):
                    raise ParsingError("Wrong type of coordinate: Float")
            connections_infos = [line.split(": ")[1]
                                 for line in lines[lines.index(goal) + 1:]
                                 if "connection:" in line]
            connections = [conn.split(" ")[0] for conn in connections_infos]
            for connection in connections:
                elems = connection.split("-")[::-1]
                for elem in elems:
                    if elem not in hubs:
                        raise ParsingError("Hub connection not possible: "
                                           "Hub not mentionned earlier.")
                if "-".join(elems) in connections:
                    raise ParsingError("Connection already mentionned in "
                                       "the list. Please avoid repetitions")
            try:
                meta_hubs = [hub.split(" [")[1].strip("]").split()
                             for hub in hubs_infos]
                for meta in meta_hubs:
                    for data in meta:
                        infos = data.split("=")
                        if (infos[0] not in
                           ["zone", "color", "max_drones"]):
                            raise ParsingError("Wrong metadata syntax.")
                        if (infos[0] == "zone" and infos[1] not in
                           ["normal", "blocked", "restricted", "priority"]):
                            raise ParsingError("Zone metadata not part "
                                               "of authorized zones")
                        colors: list[str] = [
                            "green", "blue", "red", "yellow", "orange", "cyan",
                            "purple", "magenta", "lime", "brown", "gold",
                            "white", "black", "maroon", "darkred", "violet",
                            "crimson", "rainbow"]
                        if (infos[0] == "color" and
                           (len(infos[1].split()) > 1 or
                           infos[1] not in colors)):
                            raise ParsingError("Wrong color value. Please use"
                                               "one word-color in this list:"
                                               f"{", ".join(colors)}")
                        if (infos[0] == "max_drones" and
                           "-" in infos[1]):
                            raise ParsingError("Max drone can't be negative")
                meta_connections = [hub.split(" [")[1].strip("]").split()
                                    for hub in connections_infos]
                for meta in meta_connections:
                    for data in meta:
                        infos = data.split("=")
                        if (infos[0] not in ["max_link_capacity"]):
                            raise ParsingError("Wrong metadata syntax.")
                        if (infos[0] == "max_link_capacity" and
                           "-" in infos[1]):
                            raise ParsingError("Max link capacity can't"
                                               " be negative")
            except IndexError:
                raise IndexError("Missing metadata for 1 or more hubs.")
            return True
    except FileNotFoundError:
        print("File does not exists. Please provide a valid file.")
    except ValueError:
        print("String value given instead of convertible. Please fix.")
    except (ParsingError, IndexError) as e:
        print(e)
    return False


def config_parser(filename: str) -> tuple[
                                          dict[str, dict[str, int]],
                                          dict[str, dict[str, Any]],
                                          tuple[str, str]]:
    """Parses the given file, checking if its valid and extracting
    all needed infos

    Args:
        filename (str):

    Returns:
        tuple[ dict[str, dict[str, int]], dict[str, dict[str, Any]],
        tuple[str, str]]:
    """
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
