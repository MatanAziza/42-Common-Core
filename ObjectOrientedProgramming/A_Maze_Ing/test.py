from random import shuffle
from os import system

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

def edit_next_cells(
                    cell: tuple[int, int],
                    maze: list[list[list[int]]],
                    visited_cell: list[tuple[int, int]]
                    ) -> list[list[list[int]]]:
    x, y = cell
    height = len(maze)
    width = len(maze[0])
    if y + 1 < height and (x, y + 1) in visited_cell and (x + y) % 4 == 1:
        maze[y + 1][x][2] = 0 if not maze[y + 1][x][4] else 1
        maze[y][x][0] = 0
    if x + 1 < width and (x + 1, y) in visited_cell and (x + y) % 4 == 2:
        maze[y][x + 1][3] = 0 if not maze[y][x + 1][4] else 1
        maze[y][x][1] = 0
    if y - 1 >= 0 and (x, y - 1) in visited_cell and (x + y) % 4 == 3:
        maze[y - 1][x][0] = 0 if not maze[y - 1][x][4] else 1
        maze[y][x][2] = 0
    if x - 1 >= 0 and (x - 1, y) in visited_cell and (x + y) % 4 == 0:
        maze[y][x - 1][1] = 0 if not maze[y][x - 1][4] else 1
        maze[y][x][3] = 0
    return maze

def add_42(maze: list[list[list[int]]], width: int, height: int
           ) -> list[list[list[int]]]:
    forty_two = [
        [False, False, True, False, True, True, True],
        [False, False, True, False, True, False, False],
        [True, True, True, False, True, True, True],
        [True, False, False, False, False, False, True],
        [True, False, False, False, True, True, True]
                    ]
    x_start = int((width/2)-3)
    y_start = int((height/2)-2)
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
    steps_backtrack = [int(len(seed)//2) * x for x in seed[:int(len(seed)/2)]]
    steps_taken = 0
    steps_index = 0
    tried = set()
    missing_cells = 18 if width > 8 and height > 4 else 0
    str_wait = "Loading Maze, please be patient !\n  0%"
    percentage = 1
    while len(visited_cell) < width * height - missing_cells:
        if len(visited_cell) * 100 / (width * height) >= percentage:
            percentage += 1
            system('clear')
            new_str = str_wait[:str_wait.index('\n') + 1] + percentage * '#'
            str_wait = new_str + f' {percentage - 1}%'
            print(str_wait)
        # Each loop change the direction and the first if checks the next cell
        # to fill it
        dir = seed[seed_index]
        where_to = dir % 4
        tried.add(where_to)
        x_next, y_next = x + x_axis[where_to], y + y_axis[where_to]
        x_check = 0 <= x_next < width
        y_check = 0 <= y_next < height
        is_new = (x_next, y_next) not in visited_cell
        if y_check and x_check and is_new and maze[y_next][x_next][4] is False:
            maze[y][x][where_to] = 0
            maze[y_next][x_next][(where_to+2) % 4] = 0
            visited_cell.append((x_next, y_next))
            x, y = x_next, y_next
            direction.append(dir)
            tried.clear()
            steps_taken += 1
        if len(visited_cell) + missing_cells == width * height:
            break
        # If stuck for too long trying impossible directions, backtrack
        all_ways = 1 in tried and 2 in tried and 3 in tried and 0 in tried
        if all_ways or steps_taken > steps_backtrack[steps_index]:
            maze = edit_next_cells((x, y), maze, visited_cell)
            steps_index += 1
            if steps_index >= len(seed)/2:
                steps_index = 0
            steps_taken = 0
            tried.clear()
            i = 0
            try:
                while not check_neighbors(
                    (x, y),
                    maze,
                    visited_cell) and i + missing_cells <= width * height:
                    x, y = visited_cell[i]
                    i += 1
            except IndexError:
                lst = []
                for y in range(len(maze)):
                    for x in range(len(maze[y])):
                        if maze[y][x] == [1, 1, 1, 1, False]:
                            lst.append((x, y))
                print(f"Missing = {lst}, signaled by 'O'")
                break
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
            for i in range(len(cell) - 1):
                value += 2**i if cell[i] == 1 else 0
            if cell == [1, 1, 1, 1, False]:
                maze_str.append('O')
            elif cell[4]:
                maze_str.append("X")
            else:
                maze_str.append(base2[value])
        maze_str.append('\n')
    str_m = "".join(maze_str)[:-1]
    rows = str_m.split('\n')
    rows.reverse()
    return "\n".join(rows)


x, y = 30, 20
seed = [x for x in range(15)]
shuffle(seed)
r: list = []
for i in range(len(seed)):
    r.append(seed[-i-1])
for s in r:
    seed.append(s)
# seed = [1, 8, 2, 9, 6, 0, 5, 3, 4, 7, 7, 4, 3, 5, 0, 6, 9, 2, 8, 1]
maze = generate_path(x, y, generate_maze(x, y), seed)
print('Maze Generated !')
print(convert_to_hexa(maze))
seed = "".join([str(x) for x in seed])
print(f'Seed: {seed[:len(seed)//2]}')
