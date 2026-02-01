#!/usr/bin/env python3

if __name__ == "__main__":
    try:
        print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
        print("Accessing 'ancient_fragment.txt' ...")
        file = open('ancient_fragment.txt', "r")
        print("File opened carefully ...\n\nAttempt to read...")
        print(file.read())
        print("\nData extracted successfully. Closing data-container...")
        file.close()
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
