def graph_cleaner(start: str,
                  end: str,
                  nodes: dict[str, dict[str, int]],
                  to_remove: set[str] = set()
                  ) -> dict[str, set[str]]:
    nodes = nodes.copy()
    graph = dict({key: set(value.keys()) for key, value in nodes.items()})
    for node in to_remove:
        graph.pop(node)
    for key, value in graph.items():
        graph.update({key: set(value)-to_remove})
    while True:
        removed = set([node for node in graph if (len(graph[node]) < 2
                                                  and node != start
                                                  and node != end)])
        if removed == set():
            break
        for node in graph:
            graph.update({node: set(graph[node]) - removed})
        for node in removed:
            graph.pop(node)
    return graph


def graph_find_useless(start: str,
                       goal: str,
                       graph: dict[str, dict[str, int]]) -> set[str]:
    useless: list[str] = []
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
    return set(useless)-set([start])
