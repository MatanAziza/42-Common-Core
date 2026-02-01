#!/usr/bin/env python3

if __name__ == "__main__":
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")
    print(
        "Initiating secure vault access...\n"
        "Vault connection established with failsafe protocols"
        )
    with open("classified_data.txt", "r") as file:
        print("\nSECURE EXTRACTION:")
        print(file.read())
    with open("security_protocols.txt", "r+") as file:
        print("\nSECURE PRESEVATION:")
        string = "[CLASSIFIED] New security protocols archived"
        file.write(string)
        print(string)
        print("Vault automatically sealed upon completion\n")
    print("All vault operations completed with macimum security.")
