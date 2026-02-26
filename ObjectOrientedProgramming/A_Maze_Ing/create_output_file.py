from get_config import get_config
from djikstra import shortest_path


def convert_to_hexa(maze: list[list[list[int]]]) -> str:
    base = '0123456789ABCDEF'
    maze_str = []
    for row in maze:
        for cell in row:
            value = 0
            for i in range(len(cell) - 1):
                value += 2**i if cell[i] == 1 else 0
            if cell[4]:
                maze_str.append("F")
            else:
                maze_str.append(base[value])
        maze_str.append('\n')
    str_m = "".join(maze_str)[:-1]
    rows = str_m.split('\n')
    rows.reverse()
    return "\n".join(rows)


def generate_output(maze: list[list[list[int]]], file: str) -> None:
    config = get_config(file)
    output_name = config['output_file']
    hexa = convert_to_hexa(maze)
    x_entry, y_entry = config['entry']
    x_exit, y_exit = config['exit']
    x_entry = str(x_entry)
    y_entry = str(y_entry)
    x_exit = str(x_exit)
    y_exit = str(y_exit)
    path = shortest_path(maze,
                         config['entry'],
                         config['exit'])
    with open(output_name, 'w') as f:
        f.write(hexa)
        f.write('\n\n')
        f.write(x_entry)
        f.write(', ')
        f.write(y_entry)
        f.write('\n')
        f.write(x_exit)
        f.write(', ')
        f.write(y_exit)
        f.write('\n')
        for nb in path:
            if nb == 0:
                char = 'N'
            elif nb == 1:
                char = 'E'
            elif nb == 2:
                char = 'S'
            elif nb == 3:
                char = 'W'
            f.write(char)
        f.write('\n')
