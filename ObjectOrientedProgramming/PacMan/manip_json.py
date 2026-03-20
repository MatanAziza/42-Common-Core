from typing import Any
from json import loads, dumps


def read_config(filename: str) -> dict[str, Any]:
    with open(filename, "r") as f:
        stats = f.read()
    stats_dict = dict(loads(stats))
    return stats_dict


def get_highscores(filename: str) -> list[list[Any]]:
    with open(filename, "r") as f:
        highscores = f.read()
    highscores_list = list(loads(highscores))
    return highscores_list


def register_highscore(filename: str,
                       player_name: str,
                       player_score: int) -> None:
    with open(filename, "r") as f:
        highscores = f.read()
    highscores = loads(highscores)
    highscores.append([player_name, player_score])
    min_score = 999999
    i_min = 0
    for i, x in enumerate(highscores):
        if x[1] < min_score:
            min_score = x[1]
            i_min = i
    highscores.pop(i_min)
    highscores_list = list(x for x in sorted(highscores,
                                             key=lambda x: x[1],
                                             reverse=True))
    highscores_rest = dumps(highscores_list)
    with open(filename, "w") as f:
        f.write(highscores_rest)
