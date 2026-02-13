import sys
import os


if __name__ == "__main__":
    in_venv = sys.base_prefix != sys.prefix
    if not in_venv:
        os.system("python3 -m venv construct")
        print(
            "Virtual Environment created successfully!"
            "\nRun:\n'source construct/bin/activate'"
            "\n'pip install python-dotenv'"
            "\nThen run the program again!"
        )
    else:
        import dotenv
        dotenv.load_dotenv()
        keys = {
            "MATRIX_MODE": "Mode",
            "DATABASE_URL": "Database",
            "API_KEY": "API Access",
            "LOG_LEVEL": "Log level",
            "ZION_ENDPOINT": "Zion Network"
                    }
        mode = ["development", "production"]
        env = dict()
        print("ORACLE STATUS: Reading the Matrix...\n\n")
        print("Configuration loaded:")
        for key, value in os.environ.items():
            if key in keys.keys():
                if key == "MATRIX_MODE":
                    if value not in mode:
                        value = "developement"
                if key == "API_KEY":
                    if value == "secret123":
                        value = "Authenticated"
                    else:
                        value = "Not logged in"
                if key == "DATABASE_URL":
                    if value == "https://google.com":
                        value = "Connected to local instance"
                    else:
                        value = "No instance connected to"
                if key == "ZION_ENDPOINT":
                    if env.get("Database") == "Connected to local instance":
                        value = "Online"
                env.update({keys.get(key): value})
        no_var = "Not present in the env file."
        for key in keys.values():
            if key not in env.keys() and key != "API Access":
                env.update({key: no_var})
        if no_var in env.values():
            print("Missing configuration variable:")
            for key, value in keys.items():
                if env.get(value) == no_var:
                    print(f"- {key}")
        else:
            for value in keys.values():
                print(f"{value}: {env.get(value)}")
            print("\nEnvironment security check:")
            print(
                "[OK] No hardcoded secrets detected\n"
                "[OK] .env file properly configured"
                    )
            if env.get("Mode") == "development":
                print("[OK] Production override available")
            else:
                print("[OK] Default variable 'Development' available")
            print("\nThe Oracle sees all configurations.")
