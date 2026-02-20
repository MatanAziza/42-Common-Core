def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    res = sorted(artifacts, key=lambda x: x["power"], reverse=True)
    return res


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    res = filter(lambda x: x["power"] > min_power, mages)
    return list(res)


def spell_tranformer(spells: list[str]) -> list[str]:
    res = map(lambda s: f"*{s}*", spells)
    return list(res)


def mage_stats(mages: list[dict]) -> dict:
    max_power = max(mages, key=lambda x: x["power"])["power"]
    min_power = min(mages, key=lambda x: x["power"])["power"]
    powers = [mage["power"] for mage in mages]
    avg_power = sum(powers)/len(mages)
    return {
        "max_power": max_power,
        "min_power": min_power,
        "avg_power": float(f"{avg_power:.2f}")
    }


if __name__ == "__main__":
    mages = [
            {"name": "Aoris", "power": 41, "type": "Red"},
            {"name": "Boris", "power": 1789, "type": "Communist"},
            {"name": "Coris", "power": 1984, "type": "Faucil"},
            {"name": "Doris", "power": 68, "type": "Hammer"},
            {"name": "Eoris", "power": 1917, "type": "LittleRedBook"}
                ]
    spells = [
        "FireBall",
        "Ice Shards",
        "Lightning Bolt"
                ]

    def stats(mages: list[dict]) -> None:
        for mage in mages:
            print(
                f"- Mage: {mage["name"]}, Power: {mage["power"]}"
                    )

    print("Mages:")
    stats(mages)
    print("\nSorted mages:")
    stats(artifact_sorter(mages))
    print("\nFiltered mages :")
    stats(power_filter(mages, 1000))
    print("\nOriginal spells:")
    print(f"{", ".join(spells)}")
    print("Transformed spells:")
    print(f"{", ".join(spell_tranformer(spells))}")
    print("\nMages stats:")
    stat = mage_stats(mages)
    for value in stat.keys():
        print(f"- {value}: {stat[value]}")
