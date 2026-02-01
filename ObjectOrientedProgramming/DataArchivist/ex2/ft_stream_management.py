#!/usr/bin/env python3

import sys
from colorama import Fore

if __name__ == "__main__":
    print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n")
    archivist = input("Input Stream active. Enter archivist ID: ")
    print(
        "Input Stream active. Enter status report: ",
        end='',
        flush=True
        )
    status = sys.stdin.readline().strip()
    print(
        f"[STANDARD] Archive status from {archivist}"
        f": {status}", file=sys.stdout
    )
    print(
        Fore.RED +
        "[ALERT] System diagnostic: Communication channels verified" +
        Fore.WHITE, file=sys.stderr
        )
    print("[STANDARD] Data transmission complete", file=sys.stdout)
    print("\nTree-channel communication test successful.")
