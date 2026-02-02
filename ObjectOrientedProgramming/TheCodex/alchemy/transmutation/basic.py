from alchemy.elements import create_fire, create_earth


def lead_to_gold():
    f = create_fire()
    return f"Lead transmuted to gold using {f}"


def stone_to_gem():
    e = create_earth()
    return f"Stone transmuted to gem using {e}"
