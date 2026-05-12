from srcs.parser import config_parser
from srcs.structs import Graph
import sys
from colorama import Fore
from pynput import keyboard
from pynput.keyboard import Key


def on_key_release(key: Key) -> int:
    if key == Key.down:
        return 1
    elif key == Key.up:
        return -1
    return 0


def main() -> None:
    if len(sys.argv) < 1:
        print("Too much arguments.\nRun only python3 fly_in.py.")
        sys.exit(1)
    all_files = [
                 "easy/01_linear_path.txt",
                 "easy/02_simple_fork.txt",
                 "easy/03_basic_capacity.txt",
                 "medium/01_dead_end_trap.txt",
                 "medium/02_circular_loop.txt",
                 "medium/03_priority_puzzle.txt",
                 "hard/01_maze_nightmare.txt",
                 "hard/02_capacity_hell.txt",
                 "hard/03_ultimate_challenge.txt",
                 "challenger/01_the_impossible_dream.txt",
                 "custom/easy2.txt",
                 "custom/easy3.txt",
                 "custom/hard1.txt",
                 "custom/perso.txt"]
    highlight = 0
    to_use = -1
    while True:
        print("\033[2J")
        print(Fore.GREEN + "Available drone networks:" + Fore.WHITE)
        for file in all_files:
            print(Fore.BLUE, end="") if all_files[highlight] == file else 0
            print(file[file.index('/')+1:file.index('.')], end="")
            print(" <==", end="") if all_files[highlight] == file else 0
            print(Fore.WHITE)
        while True:
            if is_pressed("down arrow") and highlight < len(all_files):
                highlight += 1
                break
            elif is_pressed("up arrow"):
                highlight -= 1
                break
            elif is_pressed("enter"):
                to_use = highlight
                break
        if to_use != -1:
            break
    path_to_file = f"maps/maps/{all_files[to_use]}"
    graph, infos, couple = config_parser(path_to_file)
    network = Graph(graph, infos, couple)
    nb_turns = network.solve_network()
    print(f"Number of turns: {nb_turns}")


if __name__ == "__main__":
    main()
