#!/usr/bin/env python3
"""Differents classes created, with some inheriting from their mother class"""


class GardenError(Exception):
    """Manages all types of garden errors"""
    def __init__(self, message):
        """initiate the error message from Exception"""
        super().__init__(message)


class PlantError(GardenError):
    """Sends an error message if a plant error is raised"""
    def __init__(self):
        """initiate the error message from Garden error"""
        super().__init__("The tomato plant if wilting!")


class WaterError(GardenError):
    """Sends an error message if a water error is raised"""
    def __init__(self):
        """initiate the error message from Garden error"""
        super().__init__("Not enough water in the tanks!")


def check_plant_state(plant):
    """Checks if a plant is in good condition"""
    if plant == "rotten":
        raise PlantError()


def check_tank_capacity(tank):
    """Checks if the tank watering the plants has enought water"""
    if tank <= 20:
        raise WaterError()


def multiple_errors(functions, elements):
    """Tests all possible garden errors"""
    for i in range(len(functions)):
        try:
            functions[i](elements[i])
        except GardenError as e:
            print(f"Caught a garden error: {e}")


if __name__ == "__main__":
    print("=== Custom Garden Error Demo ===\n")
    plant_state = "rotten"
    water_tank = 20
    try:
        print("Testing PlantError...")
        check_plant_state(plant_state)
    except PlantError as e:
        print(f"Caught PlantError: {e}\n")
    try:
        print("Testing WaterError...")
        check_tank_capacity(water_tank)
    except WaterError as e:
        print(f"Caught WaterError: {e}\n")
    print("Testing catching all garden errors...")
    l1 = [check_plant_state, check_tank_capacity]
    l2 = [plant_state, water_tank]
    for i in range(2):
        try:
            l1[i](l2[i])
        except GardenError as e:
            print(f"Caught GardenError: {e}")
    print("\nAll custom error types work correctly!")
