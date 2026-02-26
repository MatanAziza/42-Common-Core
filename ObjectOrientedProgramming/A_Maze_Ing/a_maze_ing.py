from get_config import get_config
from maze_generator import generate_maze, generate_path, display
from create_output_file import generate_output
from djikstra import shortest_path
from checker import checker
import sys


if __name__ == "__main__":
    file = sys.argv[1]
    config = get_config(file)

    width = config['width']
    height = config['height']
    maze_entry = config['entry']
    maze_exit = config['exit']
    perfect = config['perfect']

    old_maze = generate_maze(width, height)
    maze = generate_path(width, height, old_maze, perfect)
    checker(maze, maze_entry, maze_exit)

    path = shortest_path(maze, maze_entry, maze_exit)
    dis = display(maze, width, height, maze_entry, path)
    print(dis)

    generate_output(maze, file)
