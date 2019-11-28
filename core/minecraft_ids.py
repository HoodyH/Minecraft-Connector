class Enchant:
    AQUA_AFFINITY = {'max_level': 1, 'id_string': 'aqua_affinity', 'id_int': 6}
    BANE_OF_ARTHROPODS = {'max_level': 5, 'id_string': 'bane_of_arthropods', 'id_int': 18}
    BLAST_PROTECTION = {'max_level': 4, 'id_string': 'blast_protection', 'id_int': 3}
    UNBREAKING = {'max_level': 3, 'id_string': 'unbreaking', 'id_int': 34}
    KNOCKBACK = {'max_level': 2, 'id_string': 'knockback', 'id_int': 19}
    SHARPNESS = {'max_level': 5, 'id_string': 'sharpness', 'id_int': 16}
    FEATHER_FALLING = {'max_level': 4, 'id_string': 'feather_falling', 'id_int': 2}
    INFINITY = {'max_level': 1, 'id_string': 'infinity', 'id_int': 51}

    def __init__(self, enchantments_list: list = None):
        """
        :param enchantments_list: optional list of tuple (Enchant.enchantment, level)
        """
        self.enchantments = {}
        if enchantments_list:
            self.add_enchantments(enchantments_list)

    def add_enchantments(self, enchantments_list, cheat=False):
        """
        :param enchantments_list: is a list of tuple (Enchant.enchantment, level)
        :param cheat: if the level che exceed the max level
        """
        for el in enchantments_list:
            enchant = el[0]
            level = el[1]
            if isinstance(el, tuple) and isinstance(enchant, dict):
                max_level = enchant.get('max_level')
                id_string = enchant.get('id_string')
                id_int = enchant.get('id_int')

                if cheat is True:
                    lvl = level
                elif level > max_level:
                    lvl = max_level
                elif level < 1:
                    lvl = 1
                else:
                    lvl = level

                self.enchantments[id_string.upper()] = {
                    'level': lvl,
                    'id_string': id_string,
                    'id_int': id_int,
                }
            else:
                raise ValueError

    @property
    def enchantments_string(self):
        if self.enchantments:
            out = '{Enchantments:['
            for key in self.enchantments.keys():
                enchant = self.enchantments.get(key)
                out += '{'
                out += 'id:{},lvl:{}'.format(
                    enchant.get('id_string'),
                    enchant.get('level'),
                )
                out += '},'
            out = out[:-1]  # remove last comma
            out += ']}'
            return out

        else:
            return ''


class MinecraftItem:

    def __init__(self, item: list, enchant: str = None, quantity=1):
        """
        :param item: Item list
        :param enchant: list of the enchant, to append only. Built with enchant class
        :param quantity: int value
        """
        self.item = item
        self.quantity = quantity
        self.enchant = enchant

    def __str__(self):
        return 'NAME: minecraft:{} | ID'

    @property
    def id_string(self):
        if self.enchant_available:
            return 'minecraft:{}{} {}'.format(self.item[0], self.enchant, self.quantity)
        else:
            return 'minecraft:{} {}'.format(self.item[0], self.quantity)

    @property
    def id_int(self):
        return self.item[1]

    @property
    def enchant_available(self):
        return self.item[2]


IRON_SWORD = ['iron_sword', 267, True]
IRON_HELMET = ['iron_helmet', 306, True]
IRON_CHESTPLATE = ['iron_chestplate', 307, True]
IRON_LEGGINGS = ['iron_leggings', 308, True]
IRON_BOOTS = ['iron_boots', 309, True]
BOW = ['bow', 261, True]
ARROW = ['arrow', 262, False]
CROSSBOW = ['crossbow', 362, True]

GOLDEN_CARROT = ['golden_carrot', 396, False]
FLINT_AND_STEEL = ['flint_and_steel', 259, False]
