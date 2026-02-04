def record_spell(spell_name: str, ingredients: str) -> str:
    from alchemy.grimoire import validate_ingredients
    checker = validate_ingredients(ingredients)
    if "INVALID" not in checker:
        return f"Spell recorded: {spell_name} ({checker})"
    else:
        return f"Spell rejected: {spell_name} ({checker})"
