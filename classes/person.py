"""
Battle game:
A python implementation of a text based/terminal battle game
"""

import random
from classes.bcolors import bcolors


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk_h = atk + 10
        self.atk_l = atk - 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.atk_l, self.atk_h)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_target(self, enemies):
        i = 1
        print(bcolors.FAIL + bcolors.BOLD + " Targets:" + bcolors.ENDC)
        for enemy in enemies:
            print("   " + str(i) + "." + enemy.name + " - " + str(enemy.hp))
            i += 1
        index = int(input('Choose who to attack: ')) - 1
        return index


    def show_action(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + 'Actions' + bcolors.ENDC)
        for action in self.actions:
            print(" " + str(i) + ':', action)
            i += 1

    def show_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + 'Magic' + bcolors.ENDC)
        for spell in self.magic:
            print("     " + str(i) + ':', spell.name, '(cost:', str(spell.cost) + ')')
            i += 1

    def show_items(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + 'Items' + bcolors.ENDC)
        for item in self.items:
            print("     " + str(i) + '.', item['item'].name, '-', item['item'].description + '(x', str(item['quantity']), ')')
            i += 1

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        spell_dmg = spell.generate_damage()
        perc = self.hp / self.max_hp * 100

        if self.mp < spell.cost or spell.type == 'white' and perc > 50:
            self.choose_enemy_spell()
        else:
            return spell, spell_dmg


