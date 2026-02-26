import sys


def checker(
        maze: list[list[list[int]]],
        maze_entry: tuple[int, int],
        maze_exit: tuple[int, int]
            ) -> None:
    height = len(maze)
    width = len(maze[0])
    x_entry, y_entry = maze_entry
    x_exit, y_exit = maze_exit
    try:
        if x_entry == x_exit and y_entry == y_exit:
            raise Exception
    except Exception:
        print("Entry and exit are the same")
        sys.exit(0)
    try:
        if x_entry < 0 or y_entry < 0 or x_entry >= width or y_entry >= height:
            raise Exception
    except Exception:
        print("Maze entry out of bounds")
        sys.exit(0)
    try:
        if x_exit < 0 or y_exit < 0 or x_exit >= width or y_exit >= height:
            raise Exception
    except Exception:
        print("Maze exit out of bounds")
        sys.exit(0)
