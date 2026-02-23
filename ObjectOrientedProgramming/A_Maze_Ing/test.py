import random


def check_neighbors(cell: tuple[int, int], maze: list[list[list[int]]], visited_cell: list[tuple[int, int]]) -> bool:
    x, y = cell
    height = len(maze)
    width = len(maze[0])
    if y + 1 < height and (x, y + 1) not in visited_cell and maze[y + 1][x][4] is False:
        return True
    elif x + 1 < width and (x + 1, y) not in visited_cell and maze[y][x + 1][4] is False:
        return True
    elif y - 1 >= 0 and (x, y - 1) not in visited_cell and maze[y - 1][x][4] is False:
        return True
    elif x - 1 >= 0 and (x - 1, y) not in visited_cell and maze[y][x - 1][4] is False:
        return True
    return False


def generate_maze(width: int, height: int) -> list[list[list[int]]]:
    maze: list[list[list[int]]] = []
    for _ in range(0, height):
        row: list[list[int]] = []
        for _ in range(0, width):
            row.append([1, 1, 1, 1, False])
        maze.append(row)
    return maze


def generate_path(width: int, height: int, maze: list[list[list[int]]], seed: list[int]) -> list[list[list[int]]]:
    x, y = 0, 0
    visited_cell : list[tuple[int, int]] = []
    visited_cell.append((x, y))

    direction : list[int] = []
    seed_index = 0
    modif = 0
    while len(visited_cell) < width * height:
        if seed[seed_index] % 4 == 0:
            modif += 1
            if y + 1 < height and (x, y + 1) not in visited_cell:
                maze[y][x][0] = 0
                maze[y + 1][x][2] = 0
                visited_cell.append((x, y + 1))
                y += 1
                direction.append(seed[seed_index])
                modif = 0

        elif seed[seed_index] % 4 == 1:
            modif += 1
            if x + 1 < width and (x + 1, y) not in visited_cell:
                maze[y][x][1] = 0
                maze[y][x + 1][3] = 0
                visited_cell.append((x + 1, y))
                x += 1
                direction.append(seed[seed_index])
                modif = 0

        elif seed[seed_index] % 4 == 2:
            modif += 1
            if y - 1 >= 0 and (x, y - 1) not in visited_cell:
                maze[y][x][2] = 0
                maze[y - 1][x][0] = 0
                visited_cell.append((x, y - 1))
                y -= 1
                direction.append(seed[seed_index])
                modif = 0

        elif seed[seed_index] % 4 == 3:
            modif += 1
            if x - 1 >= 0 and (x - 1, y) not in visited_cell:
                maze[y][x][3] = 0
                maze[y][x - 1][1] = 0
                visited_cell.append((x - 1, y))
                x -= 1
                direction.append(seed[seed_index])
                modif = 0

        if modif > 3:
            modif = 0
            i = 0
            while not check_neighbors((x, y), maze, visited_cell):
                i += 1
                x, y = visited_cell[-i]
            seed_index = seed.index(direction[-i])

        seed_index += 1
        if seed_index > len(seed) - 1:
            print(seed_index)
            seed_index = 0

    return maze


def convert_to_hexa(maze: list[list[list[int]]]) -> str:
    base = 'FEDCBA9876543210'
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

x, y = 20, 20
lst = [x for x in range(8)]
random.shuffle(lst)
print(lst)
maze = generate_path(x, y, generate_maze(x, y), lst)
print(convert_to_hexa(maze))

