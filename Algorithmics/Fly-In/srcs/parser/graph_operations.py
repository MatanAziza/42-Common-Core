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
            news = set()
            for point in points:
                news.update(graph[point]) if point != start else 0
            if not news - points:
                if goal not in points:
                    useless.extend(points)
                break
            points |= news
    return set(useless)-set([start])

if __name__ == "__main__":
    graph = {
        "A": {"B": 1, "D": 1},
    "B": {"A": 1, "C": 1},
    "C": {"B": 1, "H": 1},
    "D": {"A": 1, "E": 1, "F": 1},
    "E": {"D": 1, "G": 1},
    "F": {"D": 1, "G": 1},
    "G": {"E": 1, "F": 1},
    "H": {"B": 1, "C": 1}
    }
    to_remove = graph_find_useless("A", "G", graph)
    print(to_remove)
    print(graph_cleaner("A", "G", graph, to_remove))
