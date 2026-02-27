import sys
from typing import Any


def checker(
    maze: list[list[list[int]]],
    config: dict[str, Any]
            ) -> None:
    width = config['width']
    height = config['height']
    maze_entry = config['entry']
    maze_exit = config['exit']
    x_entry, y_entry = maze_entry
    x_exit, y_exit = maze_exit
    perfect = config['perfect']
    output = config['output_file']
    try:
        if height <= 0 or width <= 0:
            raise Exception
    except Exception:
        print(
            "Maze dimensions need to be positive. They may not be provided "
            "in the config file.")
        sys.exit(1)
    try:
        if x_entry == x_exit and y_entry == y_exit:
            raise Exception
    except Exception:
        print(
            "Entry and exit are the same. They may not be provided "
            "in the config file.")
        sys.exit(0)
    try:
        if x_entry < 0 or y_entry < 0 or x_entry >= width or y_entry >= height:
            raise Exception
    except Exception:
        print(
            "Maze entry out of bounds. It may not be provided "
            "in the config file.")

        sys.exit(0)
    try:
        if x_exit < 0 or y_exit < 0 or x_exit >= width or y_exit >= height:
            raise Exception
    except Exception:
        print(
            "Maze exit out of bounds. It may not be provided "
            "in the config file.")

        sys.exit(0)
    try:
        if maze[y_entry][x_entry][4]:
            raise Exception
    except Exception:
        print("Maze entry cannot be in the 42 logo")
        sys.exit(0)
    try:
        if maze[y_exit][x_exit][4]:
            raise Exception
    except Exception:
        print("Maze exit cannot be in the 42 logo")
        sys.exit(0)
    try:
        if output is None:
            raise Exception
    except Exception:
        print("Missing output_file key in config file.")
    try:
        if perfect is None:
            raise Exception
    except Exception:
        print("Missing perfect key in config file.")
