#!/usr/bin/env python3


def check_plant_health(plant_name, water_level, sunlight_hours):
    """Tests a plant parameter and return the appropriate error if needed"""
    if water_level == '':
        water_level = 0
    if sunlight_hours == '':
        sunlight_hours = 0
    water_level = int(water_level)
    sunlight_hours = int(sunlight_hours)
    if plant_name == "" or None:
        raise ValueError("Error: Plant name cannot be empty")
    elif 1 > water_level:
        raise ValueError("Error: Water level is too low (min 1)")
    elif water_level > 10:
        raise ValueError("Error: Water level is too high (max 10)")
    elif 2 > sunlight_hours:
        raise ValueError("Error: Sunlight hours is too low (min 2)")
    elif sunlight_hours > 12:
        raise ValueError("Error: Sunlight hours is too high (max 12)")
    else:
        print(f"Plant '{plant_name}' is healthy!")


def test_plant_check():
    """Test differents parameters on Check Plant Health"""
    try:
        print("\nTesting good values...")
        check_plant_health("tomato", 7, 7)
    except ValueError as e:
        print(e)
    try:
        print("\nTesting empty plant name...")
        check_plant_health("", 7, 7)
    except ValueError as e:
        print(e)
    try:
        print("\nTesting bad water level...")
        check_plant_health("tomato", 15, 7)
    except ValueError as e:
        print(e)
    try:
        print("\nTesting bad sunlight hours...")
        check_plant_health("tomato", 7, 1)
    except ValueError as e:
        print(e)
    finally:
        print("\nAll errors raising tests completed!")


if __name__ == "__main__":
    print("=== Garden Plant Health Checker ===")
    try:
        check_plant_health(
                            input(
                                "Provide a plant name, its water"
                                " level and its sunlight hours\n"
                                "Plant name: "
                                ),
                            input("Plant water level: "),
                            input("Plant sunlight hours: ")
                            )
    except ValueError as e:
        print(e)
    test_plant_check()
