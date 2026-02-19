def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    power_sort = lambda x : x["power"]
    artifacts.sort(key=power_sort, reverse=True)
    return artifacts

lst = [
    {"power": 25},
    {"power": 2},
    {"power": 5},
    {"power": 36},
    {"power": 3},
    {"power": 6},
        ]

print(artifact_sorter(lst))
