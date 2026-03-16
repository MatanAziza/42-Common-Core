from typing import Any
from json import loads, dumps

def read_config(filename: str) -> dict[str, Any]:
    with open(filename, "r") as f:
        stats = f.read()
    stats = loads(stats)
    return stats


def get_highscores(filename: str) -> dict[str, int]:
    with open(filename, "r") as f:
        highscores = f.read()
    highscores = loads(highscores)
    return highscores


def register_highscore(filename: str , player_name: str, score: int) -> None:
    with open(filename, "r") as f:
        highscores = f.read()
    highscores = loads(highscores)
    highscores.update({player_name: score})
    min_score = 999999
    min_name = ""
    for name, score in highscores.items():
        if score < min_score:
            min_score = score
            min_name = name
    highscores.pop(min_name)
    highscores = {key: value for key, value in sorted(highscores.items(), key=lambda item: item[1], reverse=True)}
    highscores = dumps(highscores)
    with open(filename, "w") as f:
        f.write(highscores)
