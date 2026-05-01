def path_finding(start: str, goal: str, graph: dict[str, dict[str, int]]) -> list[list[str]]:
    paths: list[list[str]] = [[start]]
    for i in range(1, len(graph)):
        new_paths: list[list[str]] = []
        for path in paths:
            for next in graph[path[-1]]:
                new_set = path + [next] if next not in path else []
                new_paths.append(new_set) if new_set not in new_paths and new_set else 0
        paths += new_paths.copy()
        paths = [path for path in paths if len(path) > i or goal in path]
    return [path for path in paths if goal in path]