from typing import Any


def graph_find_useless(start: str,
                       goal: str,
                       graph: dict[str, dict[str, int]],
                       infos: dict[str, dict[str, Any]]) -> set[str]:
    """Returns all useless hubs (not leading to the goal)

    Args:
        start (str): _description_
        goal (str): _description_
        graph (dict[str, dict[str, int]]): _description_
        infos (dict[str, dict[str, Any]]): _description_

    Returns:
        set[str]: _description_
    """
    useless: list[str] = []
    if not graph:
        return set()
    for node in graph[start]:
        points = set(graph[node])
        while True:
            news: set[str] = set()
            for point in points:
                news.update(graph[point]) if point != start else 0
            if not news - points:
                if goal not in points:
                    useless.extend(points)
                break
            points |= news
    blocked: set[str] = {node for node in graph
                         if infos[node].get("zone", "error") == "blocked"}
    return ((set(useless)-set([start])) | blocked)


def graph_cleaner(start: str,
                  end: str,
                  nodes: dict[str, dict[str, int]],
                  infos: dict[str, dict[str, Any]],
                  to_remove: set[str] = set()
                  ) -> tuple[dict[str, dict[str, int]],
                             dict[str, dict[str, Any]]]:
    """Cleans the graph of all useless hubs (dead ends, hubs not
    leading to the goal)

    Args:
        start (str): _description_
        end (str): _description_
        nodes (dict[str, dict[str, int]]): _description_
        infos (dict[str, dict[str, Any]]): _description_
        to_remove (set[str], optional): _description_. Defaults to set().

    Returns:
        tuple[dict[str, dict[str, int]], dict[str, dict[str, Any]]]:
    """
    nodes = nodes.copy()
    graph = dict({key: {link: nodes[key][link]
                        for link in value.keys()}
                  for key, value in nodes.items()})
    for node in to_remove:
        graph.pop(node)
    for key, value in graph.items():
        for elem in to_remove:
            value.pop(elem) if elem in value else 0
        graph.update({key: value})
    while True:
        removed = {node: value
                   for node, value in graph.items()
                   if (len(graph[node]) < 2
                       and node != start
                       and node != end)}
        if removed == dict():
            break
        for key, value in graph.items():
            for elem in removed:
                value.pop(elem) if elem in value else 0
        for node in removed:
            graph.pop(node)
        infos = {key: value
                 for key, value in infos.copy().items()
                 if key in graph.keys()}
    return graph, infos
