#!/usr/bin/env python3


class GardenManager:
    def __init__(self):
        self.gardens = []

    @staticmethod
    def print(string):
        print(string)

    def create_garden_network(self):
        self.gardens = Garden.list_instances()

    def stats(self, value):
        for garden in self.gardens:
            if garden.name == value:
                garden.garden_stats()

    def gen_stats(self):
        check = "True"
        for garden in self.gardens:
            check = garden.height_check()
            if check == "False":
                break
        print(f"Height validation test: {check}")
        print("Garden scores - ", end="")
        for garden in self.gardens:
            print(f"{garden.name}: {garden.stats.score}", end="")
            if garden != self.gardens[-1]:
                print(", ", end="")
        print(f"\nTotal gardens managed : {len(self.gardens)}")

    class GardenStats:
        def __init__(self):
            self.plant = 0
            self.flower = 0
            self.prize = 0
            self.score = 0
            self.growth = 0


class Garden:
    instances = []

    def __init__(self, name):
        self.name = name
        self.__plants = []
        self.stats = GardenManager.GardenStats()
        Garden.instances.append(self)

    def add_plant(self, plant):
        self.__plants.append(plant)
        print(f"Added {plant.name} to {self.name}'s garden")
        if isinstance(plant, PrizeFlower):
            self.stats.prize += 1
            self.stats.score += plant.prize
        elif isinstance(plant, FloweringPlant):
            self.stats.flower += 1
        else:
            self.stats.plant += 1

    def grow_all(self, value):
        if value > 0:
            for plant in self.__plants:
                plant.grow(value)
                self.stats.growth += value
        else:
            print("Error: Negative growth height. Give another growth")

    def height_check(self):
        for plant in self.__plants:
            if plant.get_height() < 0:
                return "False"
        return "True"

    def add_score(self, value):
        self.stats.score += value

    def garden_stats(self):
        print(f"=== {self.name}'s Garden Report ===")
        print("Plants in garden:")
        for plant in self.__plants:
            if isinstance(plant, PrizeFlower):
                print(
                    f"- {plant.name}: {plant.get_height()}cm, {plant.color}"
                    f" flowers (blooming), Prize points: {plant.prize}"
                )
            elif isinstance(plant, FloweringPlant):
                print(
                    f"- {plant.name}: {plant.get_height()}cm, {plant.color}"
                    " flowers (blooming)"
                )
            elif isinstance(plant, Plant):
                print(f"- {plant.name}: {plant.get_height()}cm")
        print(
            f"\nPlants added: {len(self.__plants)},"
            f" Total growth: {self.stats.growth}cm"
        )
        print(
            f"Plant types: {self.stats.plant} regular, "
            f"{self.stats.flower} flowering, "
            f"{self.stats.prize} prize flowers\n"
        )

    @classmethod
    def list_instances(cls):
        return cls.instances


class Plant:
    def __init__(self, name, height):
        self.name = name
        self.__height = height

    def get_height(self):
        return self.__height

    def set_height(self, value):
        if value < 0:
            print(
                f"Error: {self.name} has negative height"
                ".Give another height"
                )
            self.__height = 0
        else:
            self.__height = value

    def grow(self, value: int):
        if value >= 0:
            self.__height += value
            print(f"{self.name} grew {value}cm")
            return value
        else:
            print("Error: Negative growth height. Give another growth")


class FloweringPlant(Plant):
    def __init__(self, name, height, color):
        super().__init__(name, height)
        self.color = color


class PrizeFlower(FloweringPlant):
    def __init__(self, name, height, color, prize):
        super().__init__(name, height, color)
        self.prize = prize


if __name__ == "__main__":
    garden_manager = GardenManager()
    garden_manager.print("=== Garden Management System Demo ===\n")
    alice_garden = Garden("Alice")
    alice_garden.add_plant(Plant("Oak Tree", 100))
    alice_garden.add_plant(FloweringPlant("Rose", 25, "red"))
    alice_garden.add_plant(PrizeFlower("Sunflower", 50, "yellow", 10))
    print()
    alice_garden.grow_all(1)
    print()
    bob_garden = Garden("Bob")
    bob_garden.add_score(92)
    alice_garden.add_score(208)
    garden_manager.create_garden_network()
    garden_manager.stats("Alice")
    garden_manager.gen_stats()
