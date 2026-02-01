#!/usr/bin/env python3


class Plant:
    def __init__(self, name, height, age):
        """Initiates the class with 3 datas:name, height and age"""
        self.name = name
        self.height = height
        self.age = age


if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    rose = Plant(name="Rose", height=25, age=30)
    sunfl = Plant(name="Sunflower", height=79, age=45)
    cactus = Plant(name="Cactus", height=15, age=120)
    print(f"{rose.name}:   {rose.height} cm, {rose.age} days old")
    print(f"{sunfl.name}:   {sunfl.height} cm, {sunfl.age} days old")
    print(f"{cactus.name}:   {cactus.height} cm, {cactus.age} days old")
