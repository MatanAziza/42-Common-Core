from random import shuffle


def check_neighbors(cell: tuple[int, int],
                    maze: list[list[list[int]]],
                    visited_cell: list[tuple[int, int]]) -> bool:
    x, y = cell
    height = len(maze)
    width = len(maze[0])
    if y + 1 < height and (x, y + 1) not in visited_cell:
        return not maze[y + 1][x][4]
    elif x + 1 < width and (x + 1, y) not in visited_cell:
        return not maze[y][x + 1][4]
    elif y - 1 >= 0 and (x, y - 1) not in visited_cell:
        return not maze[y - 1][x][4]
    elif x - 1 >= 0 and (x - 1, y) not in visited_cell:
        return not maze[y][x - 1][4]
    return False


def generate_maze(width: int, height: int) -> list[list[list[int]]]:
    maze: list[list[list[int]]] = []
    for _ in range(0, height):
        row: list[list[int]] = []
        for _ in range(0, width):
            row.append([1, 1, 1, 1, False])
        maze.append(row)
    return maze


def generate_path(width: int,
                  height: int,
                  maze: list[list[list[int]]],
                  seed: list[int]) -> list[list[list[int]]]:
    x, y = 0, 0
    visited_cell: list[tuple[int, int]] = [(x, y)]
    direction: list[int] = []
    seed_index = 0
    x_axis = [0, 1, 0, -1]
    y_axis = [1, 0, -1, 0]
    tried = set()
    while len(visited_cell) < width * height:
        # Each loop change the direction and the first if checks the next cell
        # to fill it
        dir = seed[seed_index]
        where_to = dir % 4
        tried.add(where_to)
        y_check = 0 <= y + y_axis[where_to] < height
        x_check = 0 <= x + x_axis[where_to] < width
        x_next, y_next = x + x_axis[where_to], y + y_axis[where_to]
        if y_check and x_check and (x_next, y_next) not in visited_cell:
            maze[y][x][where_to] = 0
            maze[y_next][x_next][(where_to+2) % 4] = 0
            visited_cell.append((x_next, y_next))
            x, y = x_next, y_next
            direction.append(dir)
            tried.clear()
        # If stuck for too long trying impossible directions, backtrack
        if 1 in tried and 2 in tried and 3 in tried and 0 in tried:
            tried.clear()
            i = 0
            while not check_neighbors((x, y), maze, visited_cell):
                i += 1
                x, y = visited_cell[-i]
        seed_index += 1
        if seed_index >= len(seed):
            seed_index = 0

    return maze


def convert_to_hexa(maze: list[list[list[int]]]) -> str:
    base2 = '┼┬┤┐┴─┘╴├┌│╷└╶╵'
    maze_str = []
    for row in maze:
        for cell in row:
            value = 0
            for i in range(len(cell)):
                value += 2**i if cell[i] == 1 else 0
            maze_str.append(base2[value])
        maze_str.append('\n')
    str_m = "".join(maze_str)[:-1]
    rows = str_m.split('\n')
    rows.reverse()
    return "\n".join(rows)


x, y = 80, 40
seeds = [x for x in range(10)]
shuffle(seeds)
r: list = []
for i in range(len(seeds)):
    r.append(seeds[-i-1])
for s in r:
    seeds.append(s)
seed = [1, 8, 2, 9, 6, 0, 5, 3, 4, 7, 7, 4, 3, 5, 0, 6, 9, 2, 8, 1]
maze = generate_path(x, y, generate_maze(x, y), seed)
print(convert_to_hexa(maze))
#print("".join([str(x) for x in seeds]))
print(seed)
