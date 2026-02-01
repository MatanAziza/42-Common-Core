#!/usr/bin/env python3


class SecurePlant:
    def __init__(self, name):
        self.name = name
        self.__height = 0
        self.__age = 0

    def get_height(self):
        """Returns the height in a secured way (can't access it otherwise)"""
        return self.__height

    def get_age(self):
        """Returns the age in a secured way (can't access it otherwise)"""
        return self.__age

    def set_height(self, value):
        """Set the height in a secured way (can't set it normally)"""
        if value < 0:
            print(f"Invalid operation attempted: height {value}cm [REJECTED]")
            print("Security: Negative height rejected")
        else:
            self.__height = value
            print(f"Height updated: {value}cm [OK]")

    def set_age(self, value):
        """Set the age in a secured way (can't set it normally)"""
        if value < 0:
            print(f"Invalid operation attempted: age {value} days [REJECTED]")
            print("Security: Negative age rejected")
        else:
            self.__age = value
            print(f"Age updated: {value} days [OK]")


if __name__ == "__main__":
    print("=== Garden Security System ===")
    rose = SecurePlant("Rose")
    print(f"Plant created: {rose.name}")
    rose.set_height(25)
    rose.set_age(30)
    print()
    rose.set_height(-5)
    print()
    print(
        f"Current plant: {rose.name}({rose.get_height()}cm,"
        f" {rose.get_age()} days)"
        )
