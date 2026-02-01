#!/usr/bin/env python3

import sys
import math


def distance(elem1, elem2):
    """Calculates the distance between 2 sets of coordinates"""
    x_1, y_1, z_1 = tuple(elem1)
    x_2, y_2, z_2 = tuple(elem2)
    final = math.sqrt((x_2 - x_1)**2 + (y_2 - y_1)**2 + (z_2 - z_1)**2)
    return round(final, 2)


def parse(coordinates: str):
    """Parse an input and reacts if the given string can't be parsed ..."""
    c1 = []
    try:
        for i in range(len(coordinates)):
            if coordinates[i] == " ":
                raise Exception(
                                "Space character found in coordinates."
                                "\nPlease enter coordinates following "
                                "this format: 'x,y,z'"
                                )
    except Exception as e:
        print(f"Error parsing coordinates: {e}")
        print(
            f"Error details - Type: ParsingError, Args: ({e})"
        )
        return "error", "error", "error"
    try:
        c1 = coordinates.split(",")
        if len(c1) != 3:
            raise ValueError(
                            "Error: missing coordinates.\nPlease enter"
                            " coordinate following this format: "
                            "'x,y,z'"
                            )
        new_c1 = []
        for elem in c1:
            new_c1.append(int(elem))
        print(f"Parsed position: ({c1[0]}, {c1[1]}, {c1[2]})")
        return new_c1[0], new_c1[1], new_c1[2]
    except ValueError as e:
        print(f"Error parsing coordinates: {e}")
        print(
            f"Error details - Type: ValueError, Args: ({e})\n"
        )
        return "error", "error", "error"


def test_coordinates():
    """Tests all sort of coordinates"""
    c1 = 10, 20, 5
    c2 = 0, 0, 0
    print(f"\nPosition created: {tuple(c1)}")
    print(
        f"Distance between {tuple(c1)} and {tuple(c2)}"
        f": {distance(c1, c2)}\n"
        )
    c1 = "3,4,0"
    print(f'Parsing coordinates: "{c1}"')
    try:
        c1 = parse(c1)
        print(
            f"Distance between {tuple(c1)} and {tuple(c2)}"
            f": {distance(c1, c2)}\n"
            )
    except (Exception, ValueError):
        pass
    c1 = "abc,def,ghi"
    print(f'Parsing invalid coordinates: "{c1}"')
    try:
        c1 = parse("abc,def,ghi")
        print(
            f"Distance between {tuple(c1)} and {tuple(c2)}"
            f": {distance(c1, c2)}\n"
            )
    except (Exception, ValueError):
        pass
    c1 = 3, 4, 0
    print("Unpacking demonstration:")
    x, y, z = tuple(c1)
    print(f"Player at x={x}, y={y}, z={z}")
    print(f"Coordinates: X={x}, Y={y}, Z={z}\n")


if __name__ == "__main__":
    print("=== Game Coordinate System ===")
    test_coordinates()
    if len(sys.argv) < 2:
        print("No coordinates given. Try again!")
    elif len(sys.argv) > 2:
        print("More than 1 set of coordinates were given. Try again!")
    else:
        print(f'Parsing coordinates: "{sys.argv[1]}"')
        try:
            c1 = parse(sys.argv[1])
            c2 = 0, 0, 0
            print(
                f"Distance between {tuple(c1)} and {tuple(c2)}"
                f": {distance(c1, c2)}"
                )
        except (Exception, ValueError):
            pass
