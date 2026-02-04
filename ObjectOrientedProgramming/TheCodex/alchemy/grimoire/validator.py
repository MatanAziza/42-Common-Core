def validate_ingredients(ingredients: str) -> str:
    valid_ingredients = set(["fire", "water", "air", "earth"])
    list_ingredients = set(ingredients.split(" "))
    remaining = list_ingredients.difference(valid_ingredients)
    if not remaining:
        return f"{ingredients} - VALID"
    else:
        return f"{ingredients} - INVALID"
