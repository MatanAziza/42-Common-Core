from srcs.structs import Graph, Hub, Zones

def path_finding(start: list[str],
                 goal: str,
                 graph: dict[str, dict[str, int]]) -> list[list[str]]:
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
    return [path for path in paths if goal in path]

def path_priorities(path: list[str]) -> int:
    nb_priorities: int = len([h for h in path if Graph.get_node(h).zone.value == "priority"])
    return nb_priorities

def path_time(path: list[str]) -> float:
    time: float = 0
    for hub in path:
        pass
    return 0