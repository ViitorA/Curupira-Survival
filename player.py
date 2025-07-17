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
    # Itens de comida não são equipáveis nem upgradáveis
    if item["NAME"] == "Comida":
        player["HP"] = min(player["HP"] + item["EFFECT"], player["HP_MAX"])
        return

    # Verifica se o item já está no inventário
    for inv_item in player_items:
        if inv_item["NAME"] == item["NAME"]:
            # Se já está, só faz o upgrade e não adiciona novamente no inventário
            if item["NAME"] == "Bola De Fogo":
                player[item["TYPE"]] = max(player[item["TYPE"]] + item["EFFECT"], 0)
            elif item["NAME"] == "Armadura De Couro":
                player[item["TYPE"]] = min(player[item["TYPE"]] + item["EFFECT"] , 200)
            else:
                player[item["TYPE"]] = min(player[item["TYPE"]] + item["EFFECT"], 100)
            return

    # Se não está no inventário, adiciona e aplica efeito
    player_items.append(item)
    if item["NAME"] == "Bola De Fogo":
        player[item["TYPE"]] = max(player[item["TYPE"]] + item["EFFECT"], 0)
    elif item["NAME"] == "Armadura De Couro":
        player[item["TYPE"]] = min(player[item["TYPE"]] + item["EFFECT"] , 200)
    else:
        player[item["TYPE"]] = min(player[item["TYPE"]] + item["EFFECT"], 100)

def spawn():
    WINDOW = globals.WINDOW

    player["HP"] = 100
    player["HP_MAX"] = 100
    player["ATK"] = 1
    player["ATK-COOLDOWN"] = 1500
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

    add_item(game.game_items[0]) # Adiciona bola de fogo


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
    
    # Seleciona 3 itens diferentes para o drop
    i1 = random.choice(choice_list)
    remaining_choices = [item for item in choice_list if item != i1]

    i2 = random.choice(remaining_choices)
    remaining_choices = [item for item in remaining_choices if item != i2]
    
    i3 = random.choice(remaining_choices)

    while True:
        user_choice = ui.mostrar_drops(i1,i2,i3)

        if user_choice == 1:
            add_item(i1)
            break
        elif user_choice == 2:
            add_item(i2)
            break
        elif user_choice == 3:
            add_item(i3)
            break

def update_info():
    # Checa se já pode subir de level
    if player["XP"] >= player["XP_MAX"]:
        player["LEVEL"] += 1
        player["ATK-COOLDOWN"] -= 10
        player["XP"] = player["XP_MAX"] - player["XP"]
        player["XP_MAX"] *= 1.5 # Aumenta a qtd necessária de xp com cada nível
        item_drop()

def reset():
    global last_player_attack
    last_player_attack = 0
    player.clear()
