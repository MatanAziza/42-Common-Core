import sys
import importlib
import random


if __name__ == "__main__":
    in_venv = sys.base_prefix != sys.prefix
    if in_venv:
        needed = {
            'requests': '2.32.5',
            'pandas': '3.0.0',
            'matplotlib': '3.10.8'
                    }
        goal = {
                'requests': 'Network access ready',
                'pandas': 'Data manipulation ready',
                'matplotlib': 'Visualization ready'
                }
        rest = {}
        for p, v in needed.items():
            rest.update({p: v})
        not_installed = dict()
        print("Checking dependencies:\n")
        for package, version in needed.items():
            try:
                importlib.import_module(package)
            except ImportError:
                not_installed.update({package: version})
                rest.pop(package)
        for package, version in rest.items():
            print(f"[OK] {package} ({version}) installed")
        if not_installed:
            if len(not_installed) == len(needed):
                print("No dependencies were found")
            print("\nMissing dependencies:")
            for package, version in not_installed.items():
                print(f"- {package} ({version})")

            print("\nTo install missing dependencies, execute:")
            print("With pip:")
            print("'pip install -r requirements.txt'")
            print("With Poetry:")
            print("'poetry install'\n")
        else:
            import matplotlib.pyplot as plt
            list_plot = random.sample(range(1, 1001), 1000)
            x = [x for x in range(1000)]
            print("\nAnalysing Matrix Data...")
            print("Processing 1000 data points...")
            print("Generating vizualisation...\n")
            file_name = "matrix_analysis.png"
            plt.plot(x, list_plot)
            plt.savefig(file_name)
            print("Analysis complete!")
            print(f"Generation stored in {file_name}")

    else:
        print("You're not in a virtual environment!\n")
        print(
            "To enter the construct, run:\n"
            "python -m venv construct\n"
            "source construct/bin/activate\n"
                )
        print("Then run this program again")
