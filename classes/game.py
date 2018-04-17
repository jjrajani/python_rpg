import random
from utils.player_utils import generate_label, generate_stat_bar, generate_spaces
from classes.bcolors import bcolors


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n" + "    " + bcolors.BOLD + self.name + bcolors.ENDC)
        print(bcolors.OKGREEN + bcolors.BOLD + "    ACTIONS: select 0 to go back" + bcolors.ENDC)
        for item in self.actions:
            print("     ", str(i) + ".", item)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n", bcolors.OKGREEN + bcolors.BOLD + "   MAGIC: select 0 to go back" + bcolors.ENDC)
        for spell in self.magic:
            print("     ", str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n", bcolors.OKGREEN + bcolors.BOLD + "   ITEMS: select 0 to go back" + bcolors.ENDC)
        for item in self.items:
            print("     ", str(i) + ".", item["item"].name, ":", item["item"].description, "(x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "    TARGET:" + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("        " + str(i) + ".", enemy.name)
                i += 1
        choice = int(input("    Choose target:")) - 1
        return choice

    def get_stats(self):
        hp_character_count = len(str(self.hp)) + len("/") + len(str(self.maxhp))

        name_character_count = len(self.name)
        name_filled_spaces = name_character_count + len(":") + hp_character_count + len(" ")
        name_spaces = generate_spaces(20, name_filled_spaces)

        mp_character_count = len(str(self.mp)) + len("/") + len(str(self.maxmp))
        mp_spaces = generate_spaces(7, mp_character_count)

        name = generate_label(self.name, ":", name_spaces)
        mp = generate_label('', '', mp_spaces)
        hp_bar = generate_stat_bar(self.hp, self.maxhp, 25, bcolors.OKGREEN)
        mp_bar = generate_stat_bar(self.mp, self.maxmp, 10, bcolors.OKBLUE)

        print("                     _________________________             __________ ")
        print(name + hp_bar + "   " + mp + mp_bar)

    def get_enemy_stats(self):
        bar = generate_stat_bar(self.hp, self.maxhp, 50, bcolors.FAIL)
        hp_character_count = len(str(self.hp)) + len("/") + len(str(self.maxhp))

        name_filled_spaces = len(self.name) + len(":") + hp_character_count + len(" ")
        name_spaces = generate_spaces(20, name_filled_spaces)
        name = generate_label(self.name, ":", name_spaces)

        print("                     __________________________________________________ ")
        print(name + bar)

    def choose_enemy_spell(self):
        print('--------------', self.magic)
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        pct = self.hp / self.maxhp * 100

        if self.mp < spell.cost or spell.type == "white" and pct > 50:
            self.choose_enemy_spell()
        else:
            return spell, magic_dmg
