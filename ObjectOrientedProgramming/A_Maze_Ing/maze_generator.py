from random import choice as ch, randint
from os import system


def check_neighbors(
    cell: tuple[int, int],
    maze: list[list[list[int]]],
    visited_cell: list[tuple[int, int]],
) -> bool:
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


def edit_next_cells(
    cell: tuple[int, int],
    maze: list[list[list[int]]],
    visited_cell: list[tuple[int, int]],
) -> list[list[list[int]]]:
    x, y = cell
    height = len(maze)
    width = len(maze[0])
    if y + 1 < height and (x, y + 1) in visited_cell and maze[y][x][0]:
        maze[y + 1][x][2] = 0 if not maze[y + 1][x][4] else 1
        maze[y][x][0] = 0
    elif x + 1 < width and (x + 1, y) in visited_cell and maze[y][x][1]:
        maze[y][x + 1][3] = 0 if not maze[y][x + 1][4] else 1
        maze[y][x][1] = 0
    elif y - 1 >= 0 and (x, y - 1) in visited_cell and maze[y][x][2]:
        maze[y - 1][x][0] = 0 if not maze[y - 1][x][4] else 1
        maze[y][x][2] = 0
    elif x - 1 >= 0 and (x - 1, y) in visited_cell and maze[y][x][3]:
        maze[y][x - 1][1] = 0 if not maze[y][x - 1][4] else 1
        maze[y][x][3] = 0
    return maze


def add_42(
    maze: list[list[list[int]]], width: int, height: int
) -> list[list[list[int]]]:
    forty_two = [
        [False, False, True, False, True, True, True],
        [False, False, True, False, True, False, False],
        [True, True, True, False, True, True, True],
        [True, False, False, False, False, False, True],
        [True, False, False, False, True, True, True],
    ]
    x_start = int((width / 2) - 3)
    y_start = int((height / 2) - 2)
    for y in range(5):
        for x in range(7):
            maze[y + y_start][x + x_start][4] = forty_two[y][x]
    return maze


def generate_maze(width: int, height: int) -> list[list[list[int]]]:
    maze: list[list[list[int]]] = []
    for _ in range(0, height):
        row: list[list[int]] = []
        for _ in range(0, width):
            row.append([1, 1, 1, 1, False])
        maze.append(row)
    if width >= 9 and height >= 7:
        maze = add_42(maze, width, height)
    return maze


def loading_screen(percentage: int, str_wait: str) -> str:
    system("clear")
    new_str = str_wait[: str_wait.index("\n") + 1] + percentage * "#"
    str_wait = new_str + f" {percentage - 1}%"
    print(str_wait)
    return str_wait


def generate_path(
    width: int, height: int, maze: list[list[list[int]]], perfect: bool
) -> list[list[list[int]]]:
    x, y = 0, 0
    visited_cell: list[tuple[int, int]] = [(x, y)]
    x_axis, y_axis = [0, 1, 0, -1], [1, 0, -1, 0]
    tried: set[int] = set()
    missing_cells = 18 if width > 8 and height > 4 else 0
    str_wait = "Loading Maze, please be patient !\n  0%"
    percentage = 1
    random_backtrack = randint((width * height) // 20, (width * height) // 2 + 1)
    steps_taken = 0
    while len(visited_cell) < width * height - missing_cells:
        if len(visited_cell) * 100 / (width * height) >= percentage:
            percentage += 1
            str_wait = loading_screen(percentage, str_wait)
        # Each loop change the direction and the first if checks the next cell
        # to fill it
        where_to = randint(0, 3)
        tried.add(where_to)
        x_next, y_next = x + x_axis[where_to], y + y_axis[where_to]
        x_check = 0 <= x_next < width
        y_check = 0 <= y_next < height
        is_new = (x_next, y_next) not in visited_cell
        if y_check and x_check and is_new and not maze[y_next][x_next][4]:
            maze[y][x][where_to] = 0
            maze[y_next][x_next][(where_to + 2) % 4] = 0
            visited_cell.append((x_next, y_next))
            x, y = x_next, y_next
            tried.clear()
            steps_taken += 1
        if len(visited_cell) + missing_cells == width * height:
            break
        # If stuck for too long trying impossible directions, backtrack
        all_ways = 1 in tried and 2 in tried and 3 in tried and 0 in tried
        if all_ways or steps_taken >= random_backtrack:
            if not perfect:
                maze = edit_next_cells((x, y), maze, visited_cell)
            steps_taken = 0
            tried.clear()
            i = 0
            # to fix later in prod (missing inside two)
            try:
                while (
                    not check_neighbors((x, y), maze, visited_cell)
                    and i + missing_cells <= width * height
                ):
                    x, y = visited_cell[i]
                    i += 1
            except IndexError:
                a, b = 0, 0
                for y in range(len(maze)):
                    for x in range(len(maze[y])):
                        if maze[y][x] == [1, 1, 1, 1, False]:
                            a, b = x, y
                if maze[b][a - 1][4]:
                    maze[b][a] = [1, 0, 1, 1, False]
                    maze[b][a + 1] = [1, 0, 1, 0, False]
                else:
                    maze[b][a] = [1, 1, 1, 0, False]
                    maze[b][a - 1] = [1, 0, 1, 0, False]
                break
    system("clear")
    return maze


def display(
    maze: list[list[list[int]]],
    width: int,
    height: int,
    start: tuple[int, int],
    path: list[int],
) -> str:
    # base2 = '┼┬┤┐┴─┘╴├┌│╷└╶╵ '
    base = "█████"
    color = ["\033[1;37m", "\033[1;30m", "\033[0;32m", "\033[0;36m", "\033[0;31m"]
    x_axis = [0, 1, 0, -1]
    y_axis = [1, 0, -1, 0]
    new_maze: list[list[int]] = []
    for y in range(0, height * 2 + 1):
        row: list[int] = []
        for x in range(0, width * 2 + 1):
            index = y % 2 + x % 2
            row.append(0 if index == 2 else 1)
        new_maze.append(row)
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            for d in range(4):
                new_maze[y * 2 + 1 + y_axis[d]][x * 2 + 1 + x_axis[d]] = maze[y][x][d]
    for y in range(1, len(new_maze) - 2):
        for x in range(1, len(new_maze[y]) - 2):
            if (
                new_maze[y][x - 1] == 0
                and new_maze[y][x + 1] == 0
                and new_maze[y - 1][x] == 0
                and new_maze[y + 1][x] == 0
            ):
                new_maze[y][x] = 0
    x_path, y_path = start
    for i in range(len(path)):
        new_maze[2 * y_path + 1][2 * x_path + 1] = 2
        a, b = x_axis[path[i]], y_axis[path[i]]
        new_maze[2 * y_path + 1 + b][2 * x_path + 1 + a] = 2
        x_path += x_axis[path[i]]
        y_path += y_axis[path[i]]
    new_maze[2 * y_path + 1][2 * x_path + 1] = 4
    new_maze[2 * start[1] + 1][2 * start[0] + 1] = 3
    new_maze.reverse()
    maze_str = ""
    for line in new_maze:
        maze_str += "".join([color[x] + base[x] for x in line]) + "\n"
    return maze_str
