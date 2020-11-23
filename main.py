import random

from classes.person import Person
from classes.inventory import Item
from classes.magic import Spell
from classes.bcolors import bcolors
from pprint import pprint


# Create Items
potion = Item("Potion", "potion", "Heals for 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals for 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals for 500 HP", 500)
elixer = Item("Elixer", "elixer", "Fully restore HP/MP of one party member", 9999)
grenade = Item("Grenade", "attack", "Deals 500 damage", 500)


# Black magic
fire = Spell("Fire", 10, 100, "black")
thunder = Spell("Thunder", 10, 100, "black")
blizzard = Spell("Blizzard", 20, 200, "black")
meteor = Spell("Meteor", 14, 140, "black")

# White magic
cure = Spell("Cure", 12, 120, "white")
cura = Spell("Cura", 20, 200, "white")

player_spells = [fire, thunder, blizzard, meteor, cure, cura]

player_items = [
    {"item": potion, "quantity": 15},
    {"item": hipotion, "quantity": 5},
    {"item": superpotion, "quantity": 5},
    {"item": elixer, "quantity": 2},
    {"item": grenade, "quantity": 5}
]

# Initialize players
player1 = Person("Matan", 70, 65, 60, 34, player_spells, player_items)
player2 = Person("Netta", 1500, 65, 60, 34, player_spells, player_items)
player3 = Person("Omer", 2000, 65, 60, 34, player_spells, player_items)
players = [player1, player2, player3]

# Initialize enemies
enemy1 = Person("Enemy1", 1200, 65, 20, 25, player_spells, [])
enemy2 = Person("Enemy2", 1500, 65, 45, 25, player_spells, [])
enemy3 = Person("Enemy3", 1800, 65, 50, 25, player_spells, [])
enemies = [enemy1, enemy2, enemy3]

runnig = True

while runnig:
    print('==========================================')
    for index, player in enumerate(players):
        print("\nPlayer:", player.name)
        player.show_action()
        choice = input('Choose action:')
        index = int(choice) - 1
        target_enemy = None
        # Attack
        if index == 0:
            enemy_choice = player.choose_target(enemies)
            enemy = enemies[enemy_choice]
            print(enemy.get_hp())
            dmg = player.generate_damage()
            enemy.take_damage(dmg)
            print(enemy.get_hp())
            print('You attacked for', dmg, ' points of damage.')
            target_enemy = enemy
        # Magic
        elif index == 1:
            player.show_magic()
            magic_choice = int(input('Choose magic:')) - 1
            spell = player.magic[magic_choice]
            spell_dmg = spell.generate_damage()
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + '\n Not enough mp \n' + bcolors.ENDC)
                continue
            if magic_choice == -1:
                continue

            if spell.type == "white":
                player.heal(spell_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + ' heals for', str(spell_dmg) + 'HP.' + bcolors.ENDC)
            elif spell.type == "black":
                enemy_choice = player.choose_target(enemies)
                enemy = enemies[enemy_choice]
                enemy.take_damage(spell_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + ' deals ', str(spell_dmg) + 'points of damage.' + bcolors.ENDC)

            player.reduce_mp(spell.cost)
            enemy.take_damage(spell_dmg)
            target_enemy = enemy
        # Items
        elif index == 2:
            player.show_items()
            item_choice = int(input('Choose item: ')) - 1
            if item_choice == -1:
                continue
            item = player.items[item_choice]['item']
            player.items[item_choice]['quantity'] -= 1

            if player.items[item_choice]['quantity'] == 0:
                print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP." + bcolors.ENDC)
            if item.type == 'elixer':
                player.hp = player.max_hp
                player.mp = player.max_mp
                print(bcolors.OKGREEN + "\n" + item.name + " fully restored HP/MP" + bcolors.ENDC)
            if item.type == 'attack':
                enemy_choice = player.choose_target(enemies)
                enemy = enemies[enemy_choice]
                enemy.take_damage(item.prop)
                print(bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "points of damage." + bcolors.ENDC)
                target_enemy = enemy

        # Enemy turn
        enemy_choice = random.randrange(0, len(enemies))
        enemy = enemies[enemy_choice]
        enemy_action = random.randrange(0, 2)

        # Enemy Attack
        if enemy_action == 0:
            target = random.randrange(0, len(players))
            dmg = enemy.generate_damage()
            players[target].take_damage(dmg)
            print("Enemy attacks - " + players[target].name + " lost " + str(dmg) + " points.")

        # Enemy Magic
        elif enemy_action == 1:
            spell, spell_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == "white":
                enemy.heal(spell_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + ' heals ' + enemy.name, str(spell_dmg) + 'HP.'
                      + bcolors.ENDC)
            elif spell.type == "black":
                target = random.randrange(0, len(players))
                players[target].take_damage(spell.dmg)
                print(bcolors.OKBLUE + "Enemy chose magic attack on - " + players[target].name + ", " + spell.name +
                      ', deals', str(spell_dmg) + ' points of damage.' + bcolors.ENDC)



        # enemy_index = random.randrange(0, len(enemies))
        # enemy = enemies[enemy_index]
        # enemy_choice = 1
        # enemy_dmg = enemy.generate_damage()
        # player.take_damage(enemy_dmg)

        if enemy.get_hp() == 0:
            if len(enemies) == 0:
                runnig = False
                print(bcolors.BOLD + bcolors.OKGREEN + "You won the game !!!" + bcolors.ENDC)
                continue
            else:
                del enemies[enemy_choice]
                print("Enemy:", enemy.name, " was defeated")
        elif player.get_hp() == 0:
            if len(players) == 0:
                runnig = False
                print(bcolors.BOLD + bcolors.OKGREEN + "You lost the game !!!" + bcolors.ENDC)
                continue
            else:
                del players[index]
                print(bcolors.BOLD + bcolors.FAIL + player.name + " was killed" + bcolors.ENDC)


        print('----------------')
        print('Your HP:', bcolors.OKGREEN + str(player.get_hp()) + '/' + str(player.get_max_hp()) + bcolors.ENDC)
        print('Your MP:', bcolors.OKBLUE + str(player.get_mp()) + '/' + str(player.get_max_mp()) + bcolors.ENDC)
        print('Enemy HP:', bcolors.FAIL + str(target_enemy.get_hp()) + '/' + str(target_enemy.get_max_hp()) + bcolors.ENDC)
        print('----------------')


