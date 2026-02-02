#!/usr/bin/env python3

import alchemy.elements
import alchemy


if __name__ == "__main__":
    print("\n=== Sacred Scroll Mastery ===\n")
    print("Testing direct module access:")
    try:
        print("alchemy.elements.create_fire(): ", end='')
        print(f"{alchemy.elements.create_fire()}")
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        print("alchemy.elements.create_water(): ", end='')
        print(f"{alchemy.elements.create_water()}")
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        print("alchemy.elements.create_earth(): ", end='')
        print(f"{alchemy.elements.create_earth()}")
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        print("alchemy.elements.create_air(): ", end='')
        print(f"{alchemy.elements.create_air()}")
    except AttributeError:
        print("AttributeError - not exposed")
    print("\nTesting package-level access (controlled by __init__.py):")
    try:
        print("alchemy.elements.create_fire(): ", end='')
        print(f"{alchemy.create_fire()}")
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        print("alchemy.elements.create_water(): ", end='')
        print(f"{alchemy.create_water()}")
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        print("alchemy.elements.create_earth(): ", end='')
        print(f"{alchemy.create_earth()}")
    except AttributeError:
        print("AttributeError - not exposed")
    try:
        print("alchemy.elements.create_air(): ", end='')
        print(f"{alchemy.create_ai()}")
    except AttributeError:
        print("AttributeError - not exposed")
    print("\nPackage Metadata:")
    print(f"Version: {alchemy.__version__}")
    print(f"Author: {alchemy.__author__}")
