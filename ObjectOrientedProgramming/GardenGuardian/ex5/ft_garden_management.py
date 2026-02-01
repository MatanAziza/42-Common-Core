#!/usr/bin/env python3


class GardenError(Exception):
    """Manages all types of garden errors"""


class PlantError(GardenError):
    """Sends an error message if a plant error is raised"""


class WaterError(GardenError):
    """Sends an error message if a water error is raised"""


class Garden:
    """
    Garden Class that can store multiple plants
    """
    def __init__(self):
        """
        initiates the garden with an empty list of plant and a water tank
        """
        self.garden = []
        self.tank = 22

    def add_plant(self, elem):
        """Add a plant to the garden"""
        try:
            elem.check_name()
            self.garden.append(elem)
            print(f"Added {elem.name} successfully")
        except PlantError as e:
            print(e)
        finally:
            return self

    def water_plants(self):
        """Water all plants in the garden, emptying the tank"""
        print("Opening watering system")
        elem = None
        try:
            for elem in self.garden:
                self.tank -= 1
                if self.tank < 0:
                    raise WaterError(f"Error: Cannot water {elem.name}")
                print(f"Watering {elem.name} - success")
        except WaterError as e:
            print(f"{e} - tank empty")
        finally:
            print("Closing watering system (cleanup)")

    def check_tank_capacity(self):
        """Checks if the tank has enough water to water the plants"""
        if self.tank <= 20:
            raise WaterError("Not enough water in the tanks!")

    def check_garden_health(self):
        """Checks all garden plants stats"""
        for plant in self.garden:
            try:
                plant.check_plant_health()
            except PlantError as e:
                print(e)


class Plant:
    """
    Plant class that allow plants to be created
    with some actions to be applied to them
    """
    def __init__(self, name, water, sun):
        """
        Initiates a plant with some datas(name, water and sun hours
        """
        self.name = name
        self.water = water
        self.sun = sun

    def check_name(self):
        """Checks if the plant has a valid name"""
        if self.name == "" or self.name is None:
            raise PlantError("Error adding plant : Plant name canot be empty!")

    def check_plant_health(self):
        """Checks if one plant is healthy or has a parameter off"""
        if 1 <= self.water <= 10 and 2 <= self.sun <= 12:
            print(f"{self.name}: healthy (water: {self.water}", end="")
            print(f", sun: {self.sun})")
        else:
            print(f"Error checking {self.name}: ", end="")
            if 1 > self.water:
                raise PlantError(f"Water level {self.water} too low (min 1)")
            elif self.water > 10:
                raise PlantError(f"Water level {self.water} too high (max 10)")
            elif 2 > self.sun:
                raise PlantError(f"Sunlight time {self.sun} too low (min 2)")
            elif self.sun > 12:
                raise PlantError(f"Sunlight time {self.sun} too high (max 12)")


if __name__ == "__main__":
    print("=== Garden Management System ===\n")
    print("Adding plants to garden...")
    tomato = Plant("tomato", 4, 8)
    lettuce = Plant("lettuce", 15, 6)
    not_valid = Plant("", 7, 7)
    garden = Garden()
    garden.add_plant(tomato).add_plant(lettuce).add_plant(not_valid)
    print("\nWatering plants...")
    garden.water_plants()
    print("\nChecking plant health...")
    garden.check_garden_health()
    print("\nTesting error recovery...")
    try:
        garden.check_tank_capacity()
    except GardenError as e:
        print(f"Caught GardenError: {e}")
    finally:
        print("System recovered and continuing...")
    print("\nGarden management system test complete!")
