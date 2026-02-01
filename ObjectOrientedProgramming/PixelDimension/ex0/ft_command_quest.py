#!/usr/bin/env python3

import sys

if __name__ == "__main__":
    print("=== Command Quest ===")
    nb_args = len(sys.argv)
    if nb_args == 1:
        print("No arguments provided!")
    print(f"Programm name: {sys.argv[0]}")
    if (nb_args > 1):
        print(f"Arguments received: {nb_args - 1}")
        for i in range(nb_args - 1):
            print(f"Argument {i+1}: {sys.argv[i+1]}")
    print(f"Total arguments: {nb_args}")
