from typing import Any
from json import loads, dumps


def read_config(filename: str) -> dict[str, Any]:
    '''Read the config.json file to extract values and
    Set the missing ones to default values'''
    with open(filename, "r") as f:
        stats = f.read()
    stats_dict = dict(loads(stats))
    keys = list(stats_dict.keys())
    if 'highscore_filename' not in keys:
        print('Key "highscore_filename" missing, back to default value')
        stats_dict.update({'highscore_filename': 'highscores.json'})
    if 'side' not in keys:
        print('Key "side missing, back to default value')
        stats_dict.update({'side': [16, 16, 15, 15, 14, 14, 13, 12, 11, 10]})
    if 'dt' not in keys:
        print('Key "dt" missing, back to default value')
        stats_dict.update({'dt': [2, 3, 2, 3, 3, 3, 4, 4, 4, 5]})
    if 'level' not in keys:
        print('Key "level" missing, back to default value')
        stats_dict.update({'level': 0})
    if 'lives' not in keys:
        print('Key "lives" missing, back to default value')
        stats_dict.update({'lives': 3})
    if 'points_per_pacgum' not in keys:
        print('Key "points_per_pacgum" missing, back to default value')
        stats_dict.update({'points_per_pacgum': 10})
    if 'points_per_super_pacgum' not in keys:
        print('Key "points_per_super_pacgum" missing, back to default value')
        stats_dict.update({'points_per_super_pacgum': 50})
    if 'points_per_ghost' not in keys:
        print('Key "points_per_ghost" missing, back to default value')
        stats_dict.update({'points_per_ghosts': 200})
    if 'level_max_time' not in keys:
        print('Key "level_max_time" missing, back to default value')
        stats_dict.update({'level_max_time': 120})

    return stats_dict


def get_highscores(filename: str) -> list[list[Any]]:
    'Return the list of highscores from the highscores.json file'
    with open(filename, "r") as f:
        highscores = f.read()
    highscores_list = list(loads(highscores))
    return highscores_list


def register_highscore(filename: str,
                       player_name: str,
                       player_score: int) -> None:
    '''Add the actual pair Name/Score to the list of highscores
    and delete the smaller score from it'''
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
