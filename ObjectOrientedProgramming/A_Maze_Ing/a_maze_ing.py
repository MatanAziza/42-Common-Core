from get_config import get_config
from mazegen.mazegen.maze_generator import MazeGenerator
from create_output_file import generate_output
from djikstra import shortest_path
from checker import checker
from display import display
import sys
from random import seed as seeding, randint, choice
from typing import Any
from os import system


def a_maze_ing(config: dict[str, Any], seed: str
               ) -> tuple[str, str, list[list[list[int]]]]:
    width = config["width"]
    height = config["height"]
    maze_entry = config["entry"]
    maze_exit = config["exit"]
    old_maze = MazeGenerator().blank_maze(width, height)
    maze = MazeGenerator().generate_maze(old_maze, config, seed)
    checker(maze, config)
    path = shortest_path(maze, maze_entry, maze_exit)
    final_maze = display(maze, config, path)
    config['show'] = not config['show']
    final_maze_2 = display(maze, config, path)
    config['show'] = not config['show']
    return final_maze, final_maze_2, maze


def user_interface() -> str:
    print("=== A_MAZE_ING ===")
    print("1. Re-generate a new maze")
    print("2. Regenerate a new maze with user-inputed seed")
    print("3. Show/Hide path from entry to exit")
    print("4. Change maze walls colors")
    print("5. Change maze dimensions")
    print("6. Change maze entry/exit")
    print("7. Change 'Perfect' maze status")
    print("8. Quit")
    return input("Choice? (1-8): ")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(
            "Missing config file. Please provide "
            "this file named 'config.txt' and run with:\n"
            "make run\nor\npython3 a_maze_ing.py config.txt"
        )
        sys.exit(1)
    elif len(sys.argv) > 2:
        print(
            "Too much arguments provided. Please run with:\n"
            "make run\nor\npython3 a_maze_ing.py config.txt"
        )
        sys.exit(1)
    file = sys.argv[1]
    try:
        config = get_config(file)
    except Exception:
        print(
            "Wrong config file syntax. Please provide one with "
            "such syntax:\nKEY1=VALUE1\nKEY2=VALUE2\netc"
        )
        sys.exit(1)
    if not config["seed"]:
        seed = str(randint(10, 99))
    else:
        seed = config["seed"][:-1]
    config["show"] = False
    config["wall"] = "\033[1;30m"
    x: str | None = ""
    final_maze: str = ""
    final_maze_2: str = ""
    maze: list[list[list[int]]] = [[[0]]]
    while True:
        if x is not None:
            final_maze, final_maze_2, maze = a_maze_ing(config, seed)
            generate_output(maze, config)
        print(final_maze)
        print(
            f"\033[1;37mSeed: {seed}\n"
            f"Maze dimensions: {config['width']} by {config['height']}\n"
            "Maze entry (blue) and exit (red):"
            f"{config['entry']}, {config['exit']}\n"
                )
        x = user_interface()
        if x == "1" or x == "2":
            if x == "1":
                seeding()
                seed = str(randint(10, 99))
            else:
                seed = input("What seed would you like to try: ")
            config['show'] = False
        elif x == "3":
            temp = final_maze_2
            final_maze_2 = final_maze
            final_maze = temp
            config['show'] = not config['show']
            x = None
            system('clear')
        elif x == "4":
            seeding()
            colors = ["0;30", "0;33", "0;34", "0;35"]
            config["wall"] = f"\033[{choice(colors)}m"
            seeding(seed)
            path = shortest_path(maze, config['entry'], config['exit'])
            final_maze = display(maze, config, path)
            config['show'] = not config['show']
            final_maze_2 = display(maze, config, path)
            config['show'] = not config['show']
            x = None
        elif x == "5":
            while True:
                try:
                    width: int = int(input("Provide maze width: "))
                    height: int = int(input("Provide maze height: "))
                    while width <= 0:
                        print("Width can't be negative or zero")
                        width = int(input("Provide maze width: "))
                    while height <= 0:
                        print("Height can't be negative or zero")
                        height = int(input("Provide maze height: "))
                    while height == width and width == 1:
                        print("Maze can'y be 1 by 1, it is already solved")
                        width = int(input("Provide maze width: "))
                        height = int(input("Provide maze height: "))
                    config["width"] = width
                    config["height"] = height
                    config['entry'] = (0, 0)
                    config['exit'] = (width - 1, height - 1)
                    config['show'] = False
                    seeding()
                    seed = str(randint(10, 99))
                    break
                except ValueError:
                    print(
                        "Dimensions value can't be strings. Please provide"
                        " integer values.\n"
                    )
        elif x == "6":
            extremity = input(
                "Which extremity would you like to change ?"
                "\nEntry: 1, Exit: 2: ")
            while extremity != "1" and extremity != "2":
                extremity = input(
                    "Wrong extremity provided. Please try again: ")
            extremity = 'entry' if extremity == '1' else 'exit'
            while True:
                try:
                    x_coord: int = int(input(
                        f"Provide {extremity} x coordinate: "))
                    y_coord: int = int(input(
                        f"Provide {extremity} y coordinate: "))
                    while x_coord < 0 or x_coord >= config['width']:
                        print(
                            "X Coordinate can't be outside of the maze width")
                        x_coord = int(input(
                            f"Provide {extremity} x coordinate: "))
                    while y_coord < 0 or y_coord >= config['height']:
                        print(
                            "Y Coordinate can't be outside of the maze height")
                        y_coord = int(input(
                            f"Provide {extremity} y coordinate: "))
                    if maze[y_coord][x_coord][4]:
                        raise ConnectionError
                    config[extremity] = (x_coord, y_coord)
                    break
                except ValueError:
                    print(
                        "Coordinates can't be strings. Please provide"
                        " integer values.\n"
                    )
                except ConnectionError:
                    print(
                        f"Maze {extremity} can't be in the 42 logo."
                        "Please try again")
        elif x == '7':
            config['perfect'] = not config['perfect']
            config['show'] = not config['show']
        elif x == "8":
            sys.exit(0)
        else:
            print("Invalid Command")
            x = None
