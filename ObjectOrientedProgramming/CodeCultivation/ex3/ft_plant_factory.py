#!/usr/bin/env python3


class Plant:
    def __init__(self, name, height, age):
        """Initiates the element with a name, heigth and value"""
        self.name = name
        self.height = height
        self.age = age


if __name__ == "__main__":
    print("=== Plant Factory Output ===")
    rose = Plant("Rose", 25, 30)
    oak = Plant("Oak", 200, 365)
    cactus = Plant("Cactus", 5, 90)
    sunflower = Plant("Sunflower", 80, 45)
    fern = Plant("Fern", 15, 120)
    garden = [rose, oak, cactus, sunflower, fern]
    for i in range(5):
        print(f"Created: {garden[i].name} ", end="")
        print(f"({garden[i].height}cm, {garden[i].age} days)")
    print(f"\nTotal plants created : {len(garden)}")
