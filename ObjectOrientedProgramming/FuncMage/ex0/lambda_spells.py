def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    new_list = sorted(artifacts, key=lambda x : x["power"], reverse=True)
    return new_list
