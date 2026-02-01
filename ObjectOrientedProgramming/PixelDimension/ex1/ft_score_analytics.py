#!/usr/bin/env python3

import sys


def analytics(lst: list[int]):
    """
    Analyse all sort of stats
    """
    nb_players = len(lst)
    total_score = sum(lst)
    avr_score = total_score/nb_players
    max_value = max(lst)
    min_value = min(lst)
    score_range = max_value - min_value
    print(
        f"Score processed: {lst}\n"
        f"Total players: {nb_players}\n"
        f"Total score: {total_score}\n"
        f"Average score: {avr_score}\n"
        f"High score: {max_value}\n"
        f"Low score: {min_value}\n"
        f"Score range: {score_range}"
        )


if __name__ == "__main__":
    print("=== Player Score Analytics ===")
    if len(sys.argv) == 1:
        print(
            "No score provided.\nUsage:\npython3 ft_score_analytics.py"
            " <score1> <score2> <score3> ...\nor\n"
            "./ft_score_analytics.py <score1> <score2> <score3> ..."
        )
    else:
        try:
            lst = [int(elem) for elem in sys.argv[1:]]
            analytics(lst)
        except ValueError as e:
            print(f"ValueError: {e}")
