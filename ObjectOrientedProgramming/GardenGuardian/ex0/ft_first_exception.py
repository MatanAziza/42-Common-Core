#!/usr/bin/env python3


def check_temperature(temp_str):
    """Checks if temp_str is a number, then if
    a temperature is too high or low for a plant to survive"""
    try:
        i = int(temp_str)
        if i < 0:
            print(f"Error: {i}°C is too cold for plants (min 0°C)")
        elif i > 40:
            print(f"Error: {i}°C is too hot for plants (max 40°C)")
        else:
            print(f"Temperature {i}°C is perfect for plants!")
            return i
    except ValueError:
        print(f"Error: '{temp_str}' is not a valid number")


def test_temperature_input():
    """Tests differents temperatures input"""
    print("\nTesting temperature: 25")
    check_temperature("25")
    print("\nTesting temperature: 'abc'")
    check_temperature("abc")
    print("\nTesting temperature: 100")
    check_temperature("100")
    print("\nTesting temperature: -50")
    check_temperature("-50")
    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    print("=== Garden Temperature Checker ===")
    check_temperature(input("Testing temperature: "))
    test_temperature_input()
