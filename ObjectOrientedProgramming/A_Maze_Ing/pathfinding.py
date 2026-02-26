import sys


def shortest_path(entry_maze: tuple[int, int],
                  exit_maze: tuple[int, int],
                  maze: list[list[list[int]]],
                  seed: list[int]) -> list[str]:
    shortest_path: list[str] = []

    x, y = entry_maze
    end_x, end_y = exit_maze

    x_axis = [0, 1, 0, -1]
    y_axis = [1, 0, -1, 0]
    direction = ['N', 'E', 'S', 'W']

    visited_cell: list[tuple[int, int]] = [(x, y)]
    previous_cell: list[tuple[int, int]] = [(x, y)]

    seed_index = 0
    tried: set[int] = set()

    height = len(maze)
    width = len(maze[0])

    '''Verifie si les points d'entree et de sortie ne sont pas hors limites'''
    try:
        if (x < 0 or y < 0 or x >= width or y >= height):
            raise Exception
    except Exception:
        print("Maze entry out of bounds")
        sys.exit(0)
    try:
        if (end_x < 0 or end_y < 0 or end_x >= width or end_y >= height):
            raise Exception
    except Exception:
        print("Maze exit out of bounds")
        sys.exit(0)

    '''Reprends le meme principe que pour generate_path'''
    while x != end_x or y != end_y:
        direc = seed[seed_index]
        where_to = direc % 4

        '''Fais en sorte de ne pas revenir sur ses pas
        (si on vient de l'est on ne peut pas aller a l'ouest)'''
        if (shortest_path != [] and (where_to + 2) % 4 ==
                direction.index(shortest_path[-1])):
            where_to = (where_to + 1) % 4
        tried.add(where_to)

        x_next, y_next = x + x_axis[where_to], y + y_axis[where_to]
        x_check = 0 <= x_next < width
        y_check = 0 <= y_next < height
        is_new = (x_next, y_next) not in visited_cell
        '''Rajoute un check is_possible qui verifie
        s'il y a un mur dans la direction where_to'''
        is_possible = maze[y][x][where_to] == 0
        if x_check and y_check and is_new and is_possible:
            print(f"go {direction[where_to]}")
            previous_cell.append((x, y))
            x, y = x_next, y_next
            print(x, y)
            visited_cell.append((x, y))
            shortest_path.append(direction[where_to])
            tried.clear()

        '''Backtrack a la cellule precedente si
        les trois directions possibles ont ete testees'''
        if shortest_path != [] and len(tried) == 3:
            print("bactrack")
            tried.clear()
            (x, y) = previous_cell[-1]
            print(x, y)
            previous_cell.pop(-1)
            shortest_path.pop(-1)

        seed_index += 1
        if seed_index >= len(seed):
            seed_index = 0

    return shortest_path
