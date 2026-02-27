from os import system


def loading_screen(percentage: int, str_wait: str) -> str:
    system("clear")
    new_str = str_wait[: str_wait.index("\n") + 1] + percentage * "#"
    str_wait = new_str + f" {percentage - 1}%"
    print(str_wait)
    return str_wait


def display(
    maze: list[list[list[int]]],
    width: int,
    height: int,
    start: tuple[int, int],
    path: list[int],
) -> str:
    system("clear")
    color = [
        "\033[1;37m",
        "\033[1;30m",
        "\033[0;32m",
        "\033[0;36m",
        "\033[0;31m"]
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
                new_maze[y*2+1+y_axis[d]][x*2+1+x_axis[d]] = maze[y][x][d]
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
        maze_str += "".join([color[x] + "█" for x in line]) + "\n"
    return maze_str
