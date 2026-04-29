from typing import TextIO

def graph_maker(couples: list[list[str]]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = dict()
    for line in couples:
        graph.update(
            {line[1][:line[1].index(" ")]: set()}
                    ) if "hub" in line[0] else 0
    connections = [connection[1]
                for connection in couples
                if "connection" in connection[0]]
    for connection in connections:
        nodes = connection.split("-")
        graph.update(
            {nodes[0]: graph[nodes[0]] | {nodes[1]},
            nodes[1]: graph[nodes[1]] | {nodes[0]}}
                        )
    return graph
            
def nodes_params(couples: list[list[str]]) -> dict[str, dict[str, any]]:
    infos: dict[str, dict[str, any]] = dict()
    alpha: dict[str, list[str]] = dict()
    for line in couples:
        alpha.update(
            {line[1][:line[1].index(" ")]:
             line[1][line[1].index(" "):].strip().split(" ")}
                    ) if "hub" in line[0] else 0
    for key, value in alpha.items():
        meta = value[2].strip("[]").split(" ")
        metadata = [(data.split("=")[0], data.split("=")[1]) for data in meta]
        infos[key] = {
            "coordinates": (value[0], value[1]),
                      }
        infos[key].update({k: v for k, v in metadata})
    return infos

def config_parser(filename: str) -> tuple[
                                        dict[str, set[str]],
                                        dict[str, dict[str, any]]]:
    graph: dict[str, set[str]] = dict()
    infos: dict[str, dict[str, any]] = dict()

    with open(filename, "r") as file:
        lines = file.read().split("\n")
        couples = [line.split(": ")
                   for line in lines
                   if not line.startswith("#") and line]
        graph = graph_maker(couples)
        infos = nodes_params(couples)
    return (graph, infos)

if __name__ == "__main__":
    graph, infos = config_parser("01_linear_path.txt")
    # graph, infos = config_parser("03_ultimate_challenge.txt")
    from graph_operations import graph_cleaner, graph_find_useless
    to_remove = graph_find_useless("start", "goal", graph)
    final = graph_cleaner("start", "goal", graph, to_remove)
    print(f"Useless paths: {set(graph.keys()) - set(final.keys()) != set()}")
