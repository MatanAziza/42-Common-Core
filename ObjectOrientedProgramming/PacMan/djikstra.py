from heapq import heapify, heappop, heappush
from utils import dec_to_bin


class Graph:
    def __init__(self,
                 graph: dict[tuple[int, int], dict[tuple[int, int], int]]
                 ) -> None:
        self.graph = graph
        # Cree un lien entre un noeud (coordonnees) et un autre

    def add_edge(self,
                 node1: tuple[int, int],
                 node2: tuple[int, int]
                 ) -> None:
        if node1 not in self.graph:
            self.graph[node1] = {}
        self.graph[node1][node2] = 1

    def shortest_distances(self,
                           source: tuple[int, int]
                           ) -> (tuple[dict[tuple[int, int], float],
                                 dict[tuple[int, int],
                                 tuple[int, int]]]):
        # Met toutes les distances a l'infini et la distance
        # au noeud de depart a 0
        distances = {node: float('inf') for node in self.graph}
        distances[source] = 0
        # Cree un file d'attente prioritaire
        queue = [(0, source)]
        heapify(queue)
        # Cree un set des noeuds visites
        visited = set()
        while queue:  # Tant qu'il y a des element das la file d'attente
            current_distance, current_node = heappop(queue)
            if current_node in visited:
                continue  # Si le noeud a deja ete visite on passe
            visited.add(current_node)  # Sinon on l'ajoute au noeuds visites
            # Calcule la distance entre un noeud et ses voisins et la remplace
            # si elle est plus petite que la distance deja calculee
            # (ou si c'est infini)
            for neighbor, weight in self.graph[current_node].items():
                tentative_distance = current_distance + weight
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    heappush(queue, (tentative_distance, neighbor))
                    # On ajoute a la file d'attente les voisins dont la
                    # distance est plus courte
        # On refait le chemin a partir de la fin et on cherche
        # a chaque fois la distance la plus courte
        predecessors: dict[tuple[int, int], tuple[int, int]] = {}
        for node, distance in distances.items():
            for neighbor, weight in self.graph[node].items():
                if distances[neighbor] == distance + weight:
                    predecessors[neighbor] = node
        return distances, predecessors


def shortest_path(maze: list[list[int]],
                  entry_maze: tuple[int, int],
                  exit_maze: tuple[int, int]
                  ) -> list[int]:
    # Cree le graphe
    # Les cellules sont ajoutees comme voisines que s'il n'y a pas
    # de mur entre elles
    graph: dict[tuple[int, int], dict[tuple[int, int], int]] = {}
    G = Graph(graph)
    for y, row in enumerate(maze):
        for x, old_cell in enumerate(row):
            cell = dec_to_bin(old_cell)
            if cell[0] == 0:
                G.add_edge((x, y), (x, y - 1))
            if cell[1] == 0:
                G.add_edge((x, y), (x + 1, y))
            if cell[2] == 0:
                G.add_edge((x, y), (x, y + 1))
            if cell[3] == 0:
                G.add_edge((x, y), (x - 1, y))

    _, predecessors = G.shortest_distances(entry_maze)
    # Tant que l'on est pas revenu au point d'entree, on ajoute les coordonnees
    # en partant de la fin
    predecessor = exit_maze
    path: list[tuple[int, int]] = [exit_maze]
    while predecessor != entry_maze:
        predecessor = predecessors[predecessor]
        path.append(predecessor)
        # On inverse la liste pour avoir le chemin a l'endroit
    path.reverse()
    # On transforme la liste en liste de directions
    # ('N', 'E', 'S', 'W') = (0, 1, 2, 3)
    path_str: list[int] = []
    i = 0
    while i < len(path) - 1:
        x, y = path[i]
        x_next, y_next = path[i + 1]
        if y_next == y - 1:
            path_str.append(0)
        elif x_next == x + 1:
            path_str.append(1)
        elif y_next == y + 1:
            path_str.append(2)
        elif x_next == x - 1:
            path_str.append(3)
        i += 1
    return path_str
