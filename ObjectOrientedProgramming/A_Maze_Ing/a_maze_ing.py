from get_config import get_config
from maze_generator import MazeGenerator
from create_output_file import generate_output
from djikstra import shortest_path
from checker import checker
from display import display
import sys
from random import seed as seeding, randint, choice
from typing import Any


def a_maze_ing(config: dict[str, Any]) -> tuple[str, list]:
    width = config["width"]
    height = config["height"]
    maze_entry = config["entry"]
    maze_exit = config["exit"]
    perfect = config["perfect"]
    old_maze = MazeGenerator().blank_maze(width, height)
    maze = MazeGenerator().generate_maze(width, height, old_maze, perfect)
    checker(maze, config)
    path = shortest_path(maze, maze_entry, maze_exit)
    final_maze = display(maze, config, path)
    return final_maze, maze


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
    seeding(seed)
    config["show"] = False
    config["wall"] = "\033[1;30m"
    final_maze, maze = a_maze_ing(config)
    print(final_maze)
    print(f"\033[1;37mSeed: {seed}")
    while True:
        generate_output(maze, file)
        print("=== A_MAZE_ING ===")
        print("1. Re-generate a new maze")
        print("2. Regenerate a new maze with user-inputed seed")
        print("3. Show/Hide path from entry to exit")
        print("4. Change maze walls colors")
        print("5. Change maze dimensions")
        print("6. Change maze entry/exit")
        print("7. Quit")
        x = input("Choice? (1-7): ")
        if x == "1" or x == "2":
            if x == "1":
                seeding()
                seed = str(randint(10, 99))
            else:
                seed = input("What seed would you like to try: ")
            seeding(seed)
            final_maze, _ = a_maze_ing(config)
            print(final_maze)
            print(f"\033[1;37mSeed: {seed}")
        elif x == "3":
            seeding(seed)
            if config["show"] is False:
                config["show"] = True
            else:
                config["show"] = False
            final_maze, _ = a_maze_ing(config)
            print(final_maze)
            print(f"\033[1;37mSeed: {seed}")
        elif x == "4":
            seeding()
            colors = ["0;30", "0;33", "0;34", "0;35"]
            config["wall"] = f"\033[{choice(colors)}m"
            seeding(seed)
            final_maze, maze = a_maze_ing(config)
            print(final_maze)
            print(f"\033[1;37mSeed: {seed}")
        elif x == "5":
            while True:
                try:
                    width: int = int(input("Provide maze width: "))
                    height: int = int(input("Provide maze height: "))
                    while width < 0:
                        print("Width can't be negative")
                        width = int(input("Provide maze width: "))
                    while height < 0:
                        print("Height can't be negative")
                        height = int(input("Provide maze height: "))
                    config["width"] = width
                    config["height"] = height
                    seeding()
                    seed = str(randint(10, 99))
                    seeding(seed)
                    final_maze, _ = a_maze_ing(config)
                    print(final_maze)
                    print(f"\033[1;37mSeed: {seed}")
                    break
                except ValueError:
                    print(
                        "Dimensions value can't be strings. Please provide"
                        " integer values.\n"
                    )
        elif x == "6":
            extremity = input(
                "Which extremity would you like to change ? (entry/exit): ")
            while extremity != "entry" and extremity != "exit":
                extremity = input("Wrong extremity provided. Please try again")
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
                    config[extremity] = (x_coord, y_coord)
                    seeding()
                    seeding(seed)
                    final_maze, _ = a_maze_ing(config)
                    print(final_maze)
                    print(f"\033[1;37mSeed: {seed}")
                    break
                except ValueError:
                    print(
                        "Coordinates can't be strings. Please provide"
                        " integer values.\n"
                    )

        elif x == "7":
            sys.exit(0)
        else:
            print("Invalid Command")
