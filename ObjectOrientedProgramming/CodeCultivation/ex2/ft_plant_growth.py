#!/usr/bin/env python3


class Plant:
    def __init__(self, name, height, days):
        """Initiates the class element with its name, height and age"""
        self.name = name
        self.height = height
        self.days = days

    def grow(self):
        """Grows the plant by 1 (one) centimeter"""
        self.height += 1
        return self

    def age(self):
        """Makes the plant grow 1 (one) day older"""
        self.days += 1
        return self

    def get_info(self):
        """Prints plant infos (name, height, age"""
        return f"{self.name}: {self.height}cm, {self.days} days old"


if __name__ == "__main__":
    rose = Plant("Rose", 25, 30)
    print("=== Day 1 ===")
    print(rose.get_info())
    print("=== Day 7 ===")
    days_passing = 6
    for i in range(days_passing):
        rose.age().grow()
    print(rose.get_info())
    print(f"Growth this week: +{days_passing}cm")
