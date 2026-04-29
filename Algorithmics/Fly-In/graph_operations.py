def graph_cleaner(start: str,
                  end: str,
                  nodes: dict[str, set[str]],
                  to_remove: set[str] = set()
                  ) -> dict[str, set[str]]:
    nodes = nodes.copy()
    for node in to_remove:
        nodes.pop(node)
    for key, value in nodes.items():
        nodes.update({key: set(value)-to_remove})
    while True:
        removed = set([node for node in nodes if (len(nodes[node]) < 2
                                                  and node != start
                                                  and node != end)])
        if removed == set():
            break
        for node in nodes:
            nodes.update({node: set(nodes[node]) - removed})
        for node in removed:
            nodes.pop(node)
    return nodes


def graph_find_useless(start: str,
                       goal: str,
                       graph: dict[str, set[str]]) -> set[str]:
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
    "A": {"B", "D"},
    "B": {"A", "C"},
    "C": {"B", "H"},
    "D": {"A", "E", "F"},
    "E": {"D", "G"},
    "F": {"D", "G"},
    "G": {"E", "F"},
    "H": {"B", "C"}
    }
    to_remove = graph_find_useless("A", "G", graph)
    print(to_remove)
    print(graph_cleaner("A", "G", graph, to_remove))
