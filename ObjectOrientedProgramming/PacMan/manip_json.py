from typing import Any
import json
import sys


def read_config(filename: str) -> dict[str, Any]:
    '''Read the config.json file to extract values and
    Set the missing ones to default values'''
    stats_dict: dict[str, Any] = {}
    try:
        if not filename.endswith(".json"):
            raise FileExistsError
        with open(filename, "r") as f:
            stats = f.read()
        stats_dict = dict(json.loads(stats))
        for (key, value) in stats_dict.items():
            if key == 'highscore_filename':
                if not isinstance(value, str):
                    raise AttributeError(f'{key} must be a str:')
            if key == 'side' or key == 'dt':
                if len(value) < 10:
                    raise AttributeError(f'Need 10 values for {key}:')
                if not isinstance(value, list):
                    raise AttributeError(f'Need a list for {key}:')
                for x in value:
                    if not isinstance(x, int):
                        raise AttributeError(f'A value in the {key}'
                                             'list is not an int:')
            if (key == 'level' or
                    key == 'lives' or
                    key == 'points_per_pacgum' or
                    key == 'points_per_super_pacgum' or
                    key == 'points_per_ghost' or
                    key == 'level_max_time'):
                if not isinstance(value, int):
                    raise AttributeError(f'{key} must be an int:')
    except FileExistsError:
        print('Config file is not a valid format, needs a ".json"')
        sys.exit(1)
    except FileNotFoundError:
        print('Config file non existent, generating backup data:')
    except json.decoder.JSONDecodeError:
        print('Not a valid json file format')
    except AttributeError as e:
        print(f'{e} Invalid value type in "config.json"')
        sys.exit(1)

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
    try:
        with open(filename, "r") as f:
            highscores = f.read()
        highscores_list = list(json.loads(highscores))
        for score in highscores_list:
            if score[1] < 0:
                raise ValueError
    except ValueError:
        print(f'Negative score found in {filename}')
        sys.exit(1)
    except FileNotFoundError:
        print('Creating "highscores.json"')
        highscores_list = [["Mario", 5000],
                           ["Link", 4500],
                           ["Fox", 4000],
                           ["DK", 3500],
                           ["Samus", 3000],
                           ["Bayonetta", 2500],
                           ["Pit", 2000],
                           ["Marth", 1500],
                           ["Sonic", 1000],
                           ["Kirby", 500]]
        with open(filename, "w") as f:
            f.write('[["Mario", 5000],'
                    '["Link", 4500], '
                    '["Fox", 4000], '
                    '["DK", 3500], '
                    '["Samus", 3000], '
                    '["Bayonetta", 2500], '
                    '["Pit", 2000], '
                    '["Marth", 1500], '
                    '["Sonic", 1000], '
                    '["Kirby", 500]]')

    return highscores_list


def register_highscore(filename: str,
                       player_name: str,
                       player_score: int) -> None:
    '''Add the actual pair Name/Score to the list of highscores
    and delete the smaller score from it'''
    with open(filename, "r") as f:
        highscores = f.read()
    highscores = json.loads(highscores)
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
    highscores_rest = json.dumps(highscores_list)
    with open(filename, "w") as f:
        f.write(highscores_rest)
