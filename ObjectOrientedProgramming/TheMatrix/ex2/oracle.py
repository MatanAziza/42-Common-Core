import sys
import os

from dotenv import dotenv_values


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
        env = dict()
        print("Configuration loaded:")
        for key, value in os.environ.items():
            if key in keys.keys():
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
        for value in keys.values():
            print(f"{value}: {env.get(value)}")
