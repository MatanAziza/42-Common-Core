#!/usr/bin/env python3


class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age


class Flower(Plant):
    def __init__(self, name, height, age, color):
        super().__init__(name, height, age)
        self.color = color

    def bloom(self):
        f"""Makes the {self.name} blooms"""
        print(f"{self.name} is blooming beautifully!")


class Tree(Plant):
    def __init__(self, name, height, age, trunk_diameter):
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter

    def produce_shade(self):
        f"""Generates from {self.name} shade"""
        print(f"{self.name} provides 78 square meters of shade")


class Vegetable(Plant):
    def __init__(self, name, height, age, harvest_season, nutritional_value):
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value


if __name__ == "__main__":
    print("=== Garden Plant Type===\n")
    dandruff = Plant("Dandruff", 56, 30)
    grass = Plant("Grass", 5, 156)
    rose = Flower("Rose", 25, 30, "red")
    sunflower = Flower("Sunflower", 123, 43, "yellow")
    oak = Tree("Oak", 500, 1825, 50)
    birch = Tree("Birch", 456, 983, 62)
    tomato = Vegetable("Tomato", 80, 90, "summer", "vitamin C")
    cucumber = Vegetable("Cucumber", 73, 32, "winter", "water")
    print(
        f"\n{dandruff.name} (Plant): {dandruff.height}cm, {dandruff.age} days"
        )
    print(
        f"\n{grass.name} (Plant): {grass.height}cm, {grass.age} days"
        )
    print(
        f"\n{rose.name} (Flower): {rose.height}cm, {rose.age} days,"
        f"{rose.color} color"
        )
    rose.bloom()
    print(
        f"\n{sunflower.name} (Flower): {sunflower.height}cm,"
        f"{sunflower.age} days, {sunflower.color} color"
        )
    sunflower.bloom()
    print(
        f"\n{oak.name} (Tree): {oak.height}cm, {oak.age} days,"
        f"{oak.trunk_diameter}cm diameter"
        )
    oak.produce_shade()
    print(
        f"\n{birch.name} (Tree): {birch.height}cm, {birch.age} days,"
        f"{birch.trunk_diameter}cm diameter"
        )
    birch.produce_shade()
    print(
        f"\n{tomato.name} (Vegetable): {tomato.height}cm, "
        f"{tomato.age} days, {tomato.harvest_season} harvest"
        )
    print(f"{tomato.name} is rich in {tomato.nutritional_value}")
    print(
        f"\n{cucumber.name} (Vegetable): {cucumber.height}cm, "
        f"{cucumber.age} days, {cucumber.harvest_season} harvest"
        )
    print(f"{cucumber.name} is rich in {cucumber.nutritional_value}")
