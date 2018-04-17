from classes.game import Person
from classes.bcolors import bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Black Magic
fire = Spell("Fire", 25, 600, 'black')
thunder = Spell("Thunder", 25, 600, 'black')
blizzard = Spell("Blizzard", 25, 600, 'black')
meteor= Spell("Meteor", 40, 1200, 'black')
quake= Spell("Quake", 14, 140, 'black')

# Create White Magic
cure = Spell("Cure", 25, 620, 'white')
cura = Spell("Cura", 32, 1500, 'white')
curaga = Spell("Curaga", 50, 6000, "white")

# Create Items
potion = Item("Potion", "potion", "Heals 50 HP", 50)
hipotion = Item("Hi-Potion", "potion", "Heals 100 HP", 100)
superpotion = Item("Super Potion", "potion", "Heals 100 HP", 100)
elixer = Item("Elixer", "elixer", "Fully restores HP/MP of one party member", 4580)
hielixer = Item("MegaElixer", "elixer", "Fully restores part's HP/MP", 9999)

grenade = Item("Gremade", "attack", "Deals 500 damage", 500)

# Instantiate Players
player_magic = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [
    {"item": potion, "quantity": 15},
    {"item": hipotion, "quantity": 5},
    {"item": superpotion, "quantity": 5},
    {"item": elixer, "quantity": 5},
    {"item": hielixer, "quantity": 2},
    {"item": grenade, "quantity": 5}]

player1 = Person("Valos", 3260, 132, 300, 34, player_magic, player_items)
player2 = Person("humdrum", 4160, 188, 311, 34, player_magic, player_items)
player3 = Person("Robot", 3089, 174, 288, 34, player_magic, player_items)

enemy_magic = [fire, meteor, curaga]
enemy1 = Person("Imp", 1250, 130, 560, 325, enemy_magic, [])
enemy2 = Person("Magus", 11200, 701, 525, 25, enemy_magic, [])
enemy3 = Person("Imp", 1250, 130, 560, 325, enemy_magic, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]





running = True

print("\n")
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!!" + bcolors.ENDC)


def play(player):
    player.choose_action()
    choice = input("    Choose action: ")
    index = int(choice) - 1

    if index == 0:
        dmg = player1.generate_damage()
        enemy = player.choose_target(enemies)
        enemies[enemy].take_damage(dmg)
        print("You attacked " + enemies[enemy].name + " for", dmg, "points of damage")

        if enemies[enemy].get_hp() == 0:
            print(enemies[enemy].name + " has died.")
            del enemies[enemy]

    elif index == 1:
        player.choose_magic()
        magic_choice = int(input("     Choose magic:")) - 1

        if magic_choice == -1:
            return

        spell = player.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        current_mp = player.get_mp()

        if spell.cost > current_mp:
            print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
            return

        player.reduce_mp(spell.cost)

        if spell.type == 'white':
            player.heal(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " heals for", str(magic_dmg), "HP." + bcolors.ENDC)
        elif spell.type == 'black':
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(magic_dmg)
            print(bcolors.OKBLUE + "\n" + spell.name + " deals", str(magic_dmg), "points of damage to " + enemies[enemy].name + bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

    elif index == 2:
        player.choose_item()
        item_choice = int(input("     Choose item:")) - 1

        if item_choice == -1:
            return

        item = player.items[item_choice]["item"]

        if player.items[item_choice]["quantity"] == 0:
            print(bcolors.FAIL + "\n" + "None left..." + bcolors.ENDC)
            return

        player.items[item_choice]["quantity"] -= 1

        if item.type == 'potion':
            player.heal(item.prop)
            print(bcolors.OKGREEN, "\n", item.name, "heals for", str(item.prop), "HP", bcolors.ENDC)
        elif item.type == 'elixer':

            if item.name == "MegaElixer":
                for i in players:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
            else:
                player.hp = player.maxhp
                player.mp = player.maxmp

            print(bcolors.OKGREEN, "\n", item.name, "fully restores HP/MP", bcolors.ENDC)
        elif item.type == 'attack':
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(item.prop)
            print(bcolors.FAIL, "\n", item.name, "heals", str(item.prop), "points of damage to " + enemies[enemy].name, bcolors.ENDC)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]
    else:
        play(player)


while running:
    print("======================")

    print("\n")
    print("NAME                 HP                                    MP")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        play(player)

    # Check if battle is over
    defeated_enemies = 0;
    defeated_players = 0;

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    # Check if Player won
    if defeated_enemies == len(enemies):
        print(bcolors.OKGREEN + "You win!!" + bcolors.ENDC)
        running = False
    # Check if Enemy won
    elif defeated_players == len(players):
        print(bcolors.FAIL + "The enemies have defeated you!" + bcolors.ENDC)
        running = False

    print("\n")
    # Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, len(players))

        if enemy_choice == 0:
            # Chose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damage()
            players[target].take_damage(enemy_dmg)
            print(enemy.name, "attacks", players[target].name, "for", enemy_dmg)
        elif enemy_choice == 1:
            print("++++++++++++++++++++++", enemy.choose_enemy_spell())
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)
            if spell.type == 'white':
                enemy.heal(magic_dmg)
                print(bcolors.OKBLUE + spell.name + " heals", enemy.name, "for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == 'black':
                target = random.randrange(0, 3)
                players[target].take_damage(magic_dmg)
                print(bcolors.OKBLUE + "\n" + enemy.name + "'s " + spell.name + " deals", str(magic_dmg),
                      "points of damage to " + players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name + " has died.")
                    del players[player]
            # print(enemy.name, "chose", spell.name, "damage is", magic_dmg)
