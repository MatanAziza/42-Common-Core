#!/usr/bin/env python3

def test_error_types():
    """
    Tries differents error types to showcase the function garden_operation
    """
    try:
        print("Testing ValueError...")
        garden_operations("int", "abc")
    except ValueError as e:
        print(f"Caught ValueError: {e}\n")
    try:
        print("Testing ZeroDivisionError...")
        garden_operations("zero", "0")
    except ZeroDivisionError as e:
        print(f"Caught ZeroDivisionError: {e}\n")
    try:
        print("Testing FileNotFoundError...")
        garden_operations("file", "missing.txt")
    except FileNotFoundError as e:
        print(f"Caught FileNotFoundError: {e}\n")
    try:
        print("Testing KeyError...")
        garden_operations("dict", "hehe")
    except KeyError as e:
        print(f"Caught KeyError: {e}\n")
    try:
        print("Testing multiples errors ...")
        garden_operations("zero", "0")
    except (ValueError, ZeroDivisionError):
        print("Caught an error, but the program continues...\n")
    print("All error types testes successfully!")


def garden_operations(error, elem):
    """Tries different operations leading to errors voluntarily"""
    if error == "zero" or error == "int":
        a = 0
        a = int(elem)
        if error == "zero":
            a = 1/a
    if error == "file":
        o = open(elem, "r")
        o.close()
    if error == "dict":
        notadict = {"houhou": "hihi"}
        notadict[elem]


if __name__ == "__main__":
    print("=== Garden Error Types Demo ===")
    try:
        print("Testing user input...")
        garden_operations(input("Error test: "), input("User input: "))
    except (ValueError, ZeroDivisionError, FileNotFoundError, KeyError) as e:
        print(f"Caught {str(type(e))[8:-2]}: {e}")
    print()
    test_error_types()
