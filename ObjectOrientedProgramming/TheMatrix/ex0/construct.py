import sys


if __name__ == "__main__":
    in_venv = sys.base_prefix != sys.prefix
    print("\nMATRIX STATUS: ", end='')
    if in_venv:
        print("Welcome to the Construct\n")
    else:
        print("You're still plugged in\n")
    current = str(sys.prefix)
    v = str(sys.version)
    print(f"Current Python: {current}/bin/python{v[:v.index("(")-1]}")
    print("Virtual Environment: ", end='')
    if in_venv:
        print(current[current.rindex("/")+1:])
        print(f"Environment Path: {current}\n")
        print("SUCCESS: You're in an isolated environment!")
        print(
            "Safe to install packages without affecting"
            "the global system.\n"
                )
        print("Package installation path:")
        print([path for path in sys.path if current in path][0])
        print("\nTo go back in the Matrix, execute this command:\ndeactivate")
    else:
        print("None detected\n")
        print("Warning: You're in the glbal environment!")
        print("The machines can see everything you install.\n")
        print(
            "To enter the construct, run:\n"
            "python -m venv matrix_env\n"
            "source matrix_env/bin/activate\n"
                )
        print("Then run this program again")
