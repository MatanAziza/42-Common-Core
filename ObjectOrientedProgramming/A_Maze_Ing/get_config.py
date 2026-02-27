from typing import Any


def get_config(file: str) -> dict[str, Any]:
    width = 0
    height = 0
    entry_maze = (-1, -1)
    exit_maze = (-1, -1)
    output_file = None
    perfect = None
    seed = None

    with open(file, 'r') as f:
        for line in f:
            _, value = line.split('=')
            if line.startswith('WIDTH'):
                width = int(value)
            elif line.startswith('HEIGHT'):
                height = int(value)
            elif line.startswith('ENTRY'):
                temp = value.split(',')
                x, y = int(temp[0].strip()), int(temp[1].strip())
                entry_maze = (x, y)
            elif line.startswith('EXIT'):
                temp = value.split(',')
                x, y = int(temp[0].strip()), int(temp[1].strip())
                exit_maze = (x, y)
            elif line.startswith('OUPUT_FILE'):
                output_file = value.strip()
            elif line.startswith('PERFECT'):
                if value == "True\n":
                    perfect = True
                else:
                    perfect = False
            elif line.startswith('SEED'):
                seed = value

    return {'width': width,
            'height': height,
            'entry': entry_maze,
            'exit': exit_maze,
            'output_file': output_file,
            'perfect': perfect,
            'seed': seed}
