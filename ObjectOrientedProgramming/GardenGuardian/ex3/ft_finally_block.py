#!/usr/bin/env python3


def water_plants(plant_list):
    """Water the plants, but stops if an error occurs"""
    print("Opening watering system")
    elem = None
    try:
        for elem in plant_list:
            elem += ""
            print(f"Watering {elem}")
    except (ValueError, TypeError):
        print(f"Error: Cannot water {elem} - invalid plant!")
    finally:
        print("Closing watering system (cleanup)")
        if elem is not None:
            print("Watering completed successfully!\n")
        else:
            print("\nCleanup always happens, even with errors\n")


def test_watering_system():
    """Water differents gardens to show differente reactions"""
    print("Testing normal watering...")
    water_plants(["tomato", "lettuce", "carrots"])
    print("\nTesting with error...")
    water_plants(["tomato", None])


if __name__ == "__main__":
    print("=== Garden Watering System ===\n")
    type_test = ""
    message = "Which test would you try : normal or error ?\n"
    while (type_test != "normal" and type_test != "error"):
        type_test = input(message)
        if type_test != "normal" and type_test != "error":
            message = "Wrong type of test. Try again\n"
    if type_test == "normal":
        water_plants([
                    input("Plant n°1: "),
                    input("Plant n°2: "),
                    input("Plant n°3: ")
                    ])
    else:
        water_plants([
                    input("Plant n°1: "),
                    input("Plant n°2: "),
                    None
                    ])
    test_watering_system()
