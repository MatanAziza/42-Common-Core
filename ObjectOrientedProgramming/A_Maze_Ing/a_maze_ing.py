from get_config import get_config
from maze_generator import generate_maze, generate_path
from create_output_file import generate_output
from djikstra import shortest_path
from checker import checker
from display import display
import sys
from random import seed as seeding, randint

def a_maze_ing() -> str:
    file = sys.argv[1]
    config = get_config(file)

    width = config["width"]
    height = config["height"]
    maze_entry = config["entry"]
    maze_exit = config["exit"]
    perfect = config["perfect"]

    clean_maze = generate_maze(width, height)
    maze = generate_path(width, height, clean_maze, perfect)
    checker(maze, maze_entry, maze_exit)

    path = shortest_path(maze, maze_entry, maze_exit)
    dis = display(maze, width, height, maze_entry, path)
    generate_output(maze, file)
    return dis

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Missing configuration file. Please execute "
            "with command:\npython3 a_maze_ing.py config.txt")
        sys.exit(1)
    elif len(sys.argv) >= 3:
        print("Too much arguments to execute program. Please execute "
            "with command:\npython3 a_maze_ing.py config.txt")
        sys.exit(1)
    seed = randint(10, 99)
    # seed = "".join(config["seed"][:-1])
    seeding(int(seed))
    maze = a_maze_ing()
    print(maze)
    print(f"\033[1;37mSeed: {seed}")
