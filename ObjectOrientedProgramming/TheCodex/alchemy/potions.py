from .elements import create_fire, create_earth, create_water, create_air

def healing_potion():
    return f"Healing potion brewed with {create_fire()} and {create_water()}"

def strength_potion():
    return f"Strength potion brewed with {create_earth()} and {create_fire()}"

def invisibility_potion():
    str_1 = f"Invisibility potion brewed with {create_air()}"
    return str_1+f"and {create_water()}"

def wisdom_potion():
    f = create_fire()
    w = create_water()
    a = create_air()
    e = create_earth()
    return f"Wisdom potion brewed with all elements: {f}, {w}, {a}, {e}"
