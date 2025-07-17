from math import sqrt

from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.mouse import *
import ui
import random
import pygame
import globals
import states.game as game
import objects

player = {}
player_items = []

VELOCIDADE = 250
last_player_attack = 0

def add_item(item):
    if item == "Bola De Fogo":
        player_items.append(game.game_items[0])

def spawn():
    WINDOW = globals.WINDOW

    player["HP"] = 100
    player["ATK"] = 1
    player["ATK-COOLDOWN"] = 2000
    player["RES"] = 1 # Resistance
    player["SPD"] = 1

    player["LEVEL"] = 0
    player["XP"] = 0
    player["XP_MAX"] = 100 # qtd de xp necessária p/a subir de level
    
    player["ENEMIES_KILLED"] = 0

    player["SPRITE"] = Sprite("assets/curupira.png", frames = 3)
    player["SPRITE"].set_total_duration(700)    
    player["SPRITE"].set_position(
        (WINDOW.width-player["SPRITE"].width)//2, 
        (WINDOW.height - player["SPRITE"].height)//2
    )

    # 1: Olhando p/a direita
    # 0: Olhando p/a esquerda
    player["FACING_RIGHT"] = 1

    add_item("Bola De Fogo")


def input(KEYBOARD, MOUSE):
    global VELOCIDADE, last_player_attack
    delta_t = game.delta_t
    cam_offset = game.cam_offset

    if KEYBOARD.key_pressed("W"):
        cam_offset[1] -= VELOCIDADE * delta_t
        player["SPRITE"].update()
    elif KEYBOARD.key_pressed("S"):
        cam_offset[1] += VELOCIDADE * delta_t
        player["SPRITE"].update()
    
    if KEYBOARD.key_pressed("A"):
        cam_offset[0] -= VELOCIDADE * delta_t
        player["SPRITE"].update()
        player["FACING_RIGHT"] = 0
    elif KEYBOARD.key_pressed("D"):
        cam_offset[0] += VELOCIDADE * delta_t
        player["SPRITE"].update()
        player["FACING_RIGHT"] = 1

    if MOUSE.is_button_pressed(1) and MOUSE.is_on_screen() and player["ATK-COOLDOWN"] < pygame.time.get_ticks() - last_player_attack:
        alvo = MOUSE.get_position()
        player_x = player["SPRITE"].x
        player_y = player["SPRITE"].y
        
        objects.fireball_spawn(player_x + game.cam_offset[0], 
            player_y + game.cam_offset[1], 
            alvo[0] + game.cam_offset[0], 
            alvo[1] + game.cam_offset[1]
        )

        last_player_attack = pygame.time.get_ticks()

def item_drop():
    global player, player_items
    choice_list = game.game_items
    
    i1 = random.choice(choice_list)
    i2 = random.choice(choice_list)
    i3 = random.choice(choice_list)

    while True:
        user_choice = ui.mostrar_drops(i1,i2,i3)

        if user_choice == 1:
            player_items.append(i1)
            # Limita todos os status a 100
            player[i1["TYPE"]] = min(player[i1["TYPE"]] + i1["EFFECT"], 100)
            break
        elif user_choice == 2:
            player_items.append(i2)
            player[i2["TYPE"]] = min(player[i2["TYPE"]] + i2["EFFECT"], 100)
            break
        elif user_choice == 3:
            player_items.append(i3)
            player[i3["TYPE"]] = min(player[i3["TYPE"]] + i3["EFFECT"], 100)
            break

def update_info():
    print(player["HP"])
    # Checa se já pode subir de level
    if player["XP"] >= player["XP_MAX"]:
        player["LEVEL"] += 1
        player["XP"] = player["XP_MAX"] - player["XP"]
        player["XP_MAX"] *= 2 # Dobra a qtd necessária de xp com cada nível
        item_drop()

def reset():
    global last_player_attack
    last_player_attack = 0
    player.clear()
