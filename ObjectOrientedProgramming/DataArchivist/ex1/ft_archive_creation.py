#!/usr/bin/env python3

if __name__ == "__main__":
    try:
        print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")
        print("Initializing new archive: new_discovery.txt ...")
        file = open("new_discovery.txt", "x")
        file.close()
        file = open("new_discovery.txt", "w")
        print("New archive created successfully!\n")
        print("Inscribing new data...")
        str1 = "[ENTRY 001]: Quantum breakthrough: The Zonai were right, time"
        str11 = " travel is possible but only 22 minutes back"
        str2 = "[ENTRY 001]: Resources have been optimised,"
        str22 = " resulting in a 347% efficiency gain"
        str3 = "[ENTRY 002]: Matan has archived this data"
        file.write(f"{str1}{str11}\n")
        print(f"{str1}{str11}")
        file.write(f"{str2}{str22}\n")
        print(f"{str2}{str22}")
        file.write(str3)
        print(f"{str3}\n")
        print("Data inscription complete. Storage unit sealed.")
        file.close()
    except Exception as e:
        print(f"{str(type(e))[8:-2]}: {e}")
