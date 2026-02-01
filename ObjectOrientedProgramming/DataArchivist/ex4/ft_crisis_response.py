#!/usr/bin/env python3

import os

if __name__ == "__main__":
    print("=== CYBER ARCHIVES - CRISS RESPONSE SYSTEM ===\n")
    files = [
            "lost_archive.txt",
            "classified_vault.txt",
            "standard_archive.txt"
            ]
    os.system("touch classified_vault.txt;chmod 000 classified_vault.txt")
    for file in files:
        try:
            print(f"CRISIS ALERT: Attempting access to '{file}'...")
            with open(file) as f:
                print(f'SUCCESS: Archive recovered - "{f.read()}"')
                print("Normal operations resumed")
        except FileNotFoundError:
            print(
                "RESPONSE: Archive not found in storage matrix"
                "\nStatus: Crisis handled, system stable\n"
            )
        except PermissionError:
            print(
                "RESPONSE: Security protocols deny access\n"
                "STATUS: Crisis handled, security maintained\n"
            )
    os.system("rm -f classified_vault.txt")
    print("\nAll crisis scenarios handled successfully. Archives secure")
