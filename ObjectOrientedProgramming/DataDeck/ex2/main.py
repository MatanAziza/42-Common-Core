from ex2 import EliteCard

if __name__ == "__main__":
    print("=== DataDeck Ability System ===\n")
    print("EliteCard capabilities:")
    print("- Card: ['play', 'get_card_info', 'is_playable']")
    print("- Combatable: ['attack', 'defend', 'get_combat_stats']")
    print("- Magical: ['cast_spell', 'channel_mana', 'get_magic_stats']\n")
    print("Playing Arcane Warior (Elite Card):\n")
    card_1 = EliteCard("Arcane Warrior", 7, "Mythic", 12, 5, 3, 4)
    card_2 = EliteCard("Deez Nuts", 1, "Dirt", 6, 1, 1, 1)
    atk_result = card_1.attack(card_2)
    def_result = card_1.defend(2)
    if card_2.health < atk_result.get("damage"):
        card_2.health = 0
    else:
        card_2.health -= atk_result.get("damage")
    diff = def_result.get("damage_taken") - def_result.get("damage_blocked")
    if diff > 0:
        card_1.health -= diff
    print(f"Combat phase:\nAttack result: {atk_result}")
    print(f"Defense result:{def_result}\n")
    print("Arcane Warior stats:", card_1.get_card_info())
    print("Deez Nuts stats:", card_2.get_card_info(), '\n')
    spell_result = card_1.cast_spell("Fireball", [card_2])
    mana_channel = card_1.channel_mana(4)
    card_1.mana -= spell_result.get("mana_used")
    print(f"Magic phase:\nSpell cast: {spell_result}")
    print(f"Mana channel: {mana_channel}\n")
    print("Multiple interface implementation successful!")
