#!/usr/bin/env python3

class PlayerBase:
    """Store all players infos"""
    base = []
    items_infos = dict(
                    sword=dict(
                                value=500,
                                type_item="weapon",
                                rarity="rare"
                                ),
                    potion=dict(
                                value=50,
                                type_item="consumable",
                                rarity="common"
                                ),
                    shield=dict(
                                value=200,
                                type_item="armor",
                                rarity="uncommon"
                                ),
                    helmet=dict(
                                value=80,
                                type_item="armor",
                                rarity="uncommon"
                                ),
                    magic_ring=dict(
                                value=1000,
                                type_item="misc",
                                rarity="epic"
                                )
                    )

    @classmethod
    def items_list(cls):
        """Returns the list of existing items"""
        return cls.items_infos

    @classmethod
    def give_item(cls, p1, p2, item, qt):
        """TRies to give a number of item from a player to another"""
        print("\n=== Item Transfer Maneuver ===")
        print(f"{p1} transfers {qt}: '{str(item).title()}' to {p2} : Start")
        player_1 = None
        player_2 = None
        try:
            for player in cls.base:
                if player.name == p1:
                    player_1 = player
                if player.name == p2:
                    player_2 = player
            if player_1 is None:
                raise KeyError(f"{p1} does not exist in the DataBase")
            if player_2 is None:
                raise KeyError(f"{p2} does not exist in the DataBase")
            inv_qt_1 = player_1.inventory.get(item)
            if inv_qt_1 is None:
                raise KeyError(f"{str(item).title()} is not a valid item")
            if inv_qt_1 - qt < 0:
                raise ValueError(
                                f"to give to {p2}"
                                )
            player_1.inventory.update({item: inv_qt_1 - qt})
            player_1.nb_items -= qt
            player_2.nb_items += qt
            inv_qt_2 = player_2.inventory.get(item)
            player_2.inventory.update({item: inv_qt_2 + qt})
            print(f"{str(item).title()} transfer done successfully !")
            print("\n=== Updated Inventories ===")
            print(f"{p1}'s {item}: {inv_qt_1 - qt}")
            print(f"{p2}'s {item}: {inv_qt_2 + qt}")
        except (ValueError, KeyError) as e:
            print(f"{str(type(e))[8:-2]}: {e}")

    @classmethod
    def analytics(cls):
        """Provides multiple datas on all players inventory"""
        print("=== Inventory Analytics ===")
        max_wealth = 0
        max_p = ""
        for player in cls.base:
            current = player.get_inventory_value()
            if current > max_wealth:
                max_wealth = current
                max_p = player.name
        print(f"Most valuable player: {max_p} ({max_wealth} gold)")
        max_nb = 0
        for player in cls.base:
            current = player.get_inventory_nb()
            if current > max_nb:
                max_nb = current
                max_p = player.name
        print(f"Most items: {max_p} ({max_nb} items)")
        rarest_nb = 0
        list_rarest = []
        items = cls.items_infos.keys()
        while (1):
            for item in items:
                nb_invs = 0
                for player in cls.base:
                    nb_invs += int(player.inventory.get(item))
                if (nb_invs == rarest_nb):
                    list_rarest.append(item)
            if len(list_rarest) != 0:
                break
            else:
                rarest_nb += 1
        print(f"Rarest items: {str(list_rarest)[1:-1]}")

    class Player:
        """store a player nametag and its inventory,
        as long as multiple operation"""
        def __init__(self, name, sword_q, potion_q, shield_q, helm_q, ring_q):
            """Create a player account with its name and inventory"""
            self.name = name
            self.inventory = dict(
                                sword=sword_q,
                                potion=potion_q,
                                shield=shield_q,
                                helmet=helm_q,
                                magic_ring=ring_q
                                )
            self.nb_items = sword_q + potion_q + shield_q + helm_q + ring_q
            PlayerBase.base.append(self)

        def get_inventory(self):
            """Prints a player full inventory"""
            print(f"\n=== {self.name}'s inventory ===")
            inv_value = 0
            nb_items = 0
            list_cat = {}
            for elem in self.inventory:
                type_item = PlayerBase.items_list().get(elem).get('type_item')
                rarity = PlayerBase.items_list().get(elem).get('rarity')
                nbr = self.inventory.get(elem)
                value = PlayerBase.items_list().get(elem).get('value')
                if (nbr != 0):
                    print(
                        f"{elem} ({type_item}, {rarity}): {nbr}x @ {value}"
                        f" gold each = {nbr*value} gold"
                    )
                    inv_value += value
                    nb_items += nbr
                    list_cat.update({type_item: nbr})
            print(f"\nInventory value: {inv_value} gold")
            print(f"Item count: {nb_items} items")
            string = "Categories: "
            for i, elem in enumerate(list_cat.items()):
                string += f"{elem[0]}({elem[1]})"
                if i != len(list_cat.items()) - 1:
                    string += ", "
            print(string)

        def get_inventory_value(self):
            """Returns a player's inventory value"""
            inv_value = 0
            for elem in self.inventory:
                nbr = self.inventory.get(elem)
                value = PlayerBase.items_list().get(elem).get('value')
                if (nbr != 0):
                    inv_value += value
            return inv_value

        def get_inventory_nb(self):
            """returns a player's total number of items"""
            nb_items = 0
            for elem in self.inventory:
                nbr = self.inventory.get(elem)
                if (nbr != 0):
                    nb_items += nbr
            return nb_items


if __name__ == "__main__":
    alice = PlayerBase.Player("Alice", 1, 5, 1, 1, 0)
    bob = PlayerBase.Player("Bob", 0, 0, 1, 1, 1)
    alice.get_inventory()
    PlayerBase.give_item("Alice", "Bob", "potion", 2)
    PlayerBase.analytics()
