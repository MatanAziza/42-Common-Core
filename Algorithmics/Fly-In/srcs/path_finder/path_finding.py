from typing import Callable
from srcs.structs import Graph, NextHubInfos
from math import sqrt
from functools import partial


def path_cost(way: list[str]) -> int:
    """Returns a binary translated number based on whether a zone
    is prioritary, normal or restricted""

    Args:
        max_length (int):
        way (list[str]):

    Returns:
        int: _description_
    """
    nb_priorities: int = 0
    for i in range(len(way) - 1):
        is_res: bool = Graph.get_node(way[i + 1]).zone.value == 1 # Restricted
        nb_priorities += is_res * 2 + (not is_res) * 1
    print(nb_priorities, way)
    return nb_priorities


def path_priorities(max_length: int, way: list[str]) -> int:
    """Returns a binary translated number based on whether a zone
    is prioritary, normal or restricted""

    Args:
        max_length (int):
        way (list[str]):

    Returns:
        int: _description_
    """
    nb_priorities: int = 0
    for i in range(len(way)):
        is_prio: bool = Graph.get_node(way[i]).zone.value == 3 # Priority zone
        nb_priorities += is_prio * 2 ** (max_length - i)
    print(nb_priorities, way)
    return nb_priorities


def path_time(path: list[str]) -> float:
    """Returns a value based on variance and
    mean value of drones travelling through the path,
    higher number meaning better path

    Args:
        path (list[str]):

    Returns:
        float:
    """
    mean: float
    variance: float
    lesser_capacity: list[int] = []
    for i in range(0, len(path) - 1):
        hub = Graph.get_node(path[i])
        next: NextHubInfos = hub.next_hubs[path[i+1]]
        lesser_drone = min([next.max_drones, next.max_link_capacity])
        lesser_capacity.append(lesser_drone)
    mean = sum(lesser_capacity)/len(lesser_capacity)
    list_apart: list[float] = []
    for lesser in lesser_capacity:
        list_apart.append(abs(lesser - mean))
    variance = sum(list_apart)/len(list_apart)
    print(mean, variance, path)
    return (abs(mean-sqrt(variance))//0.01)/100


def paths_sorter(key1: Callable[[list[str]], int],
                 key2: Callable[[list[str]], int],
                 key3: Callable[[list[str]], float],
                 ) -> Callable[[list[str]], tuple[int, int, float]]:
    """Creates a sorter function that returns
    a tuple of both upper sort functions.

    Args:
        key1 (Callable[[list[str]], int]):
        key2 (Callable[[list[str]], float]):

    Returns:
        Callable[[list[str]], tuple[int, float]]:
    """
    def new_sorter(path: list[str]) -> tuple[int, int, float]:
        """Returns a tuple of each sorter function returns

        Args:
            path (list[str]): _description_

        Returns:
            tuple[int, int, float]: _description_
        """
        values: tuple[int, int, float] = (key1(path), key2(path), key3(path))
        return values
    return new_sorter


def path_finding(start: list[str],
                 goal: str,
                 graph: dict[str, dict[str, int]]) -> list[list[str]]:
    """Returns a list of all possible path sorted by priority order
    and

    Args:
        start (list[str]): _description_
        goal (str): _description_
        graph (dict[str, dict[str, int]]): _description_

    Returns:
        list[list[str]]: _description_
    """
    paths: list[list[str]] = [start]
    for i in range(1, len(graph) - len(start) + 1):
        new_paths: list[list[str]] = []
        for path in paths:
            for next in graph[path[-1]]:
                dic = path + [next] if next not in path else []
                new_paths.append(dic) if dic not in new_paths and dic else 0
        paths += new_paths.copy()
        paths = [path for path in paths
                 if len(path) >= len(start) + i or goal in path]
    path_prio = partial(path_priorities, max([len(path) for path in paths]))
    sorter = paths_sorter(path_prio, path_cost, path_time)
    paths.sort(key=path_time, reverse=True)
    print(paths, '\n')
    paths.sort(key=path_prio, reverse=True)
    print(paths, '\n')
    paths.sort(key=path_cost)
    return [path for path in paths if goal in path]
