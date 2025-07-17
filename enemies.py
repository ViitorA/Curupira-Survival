import random
from player import player
from objects import bullet_spawn
import ui
from PPlay.sprite import *

enemies_list = []

def spawn(type, cam_offset):
    player_x = int(cam_offset[0])
    player_y = int(cam_offset[1])

    x_left = random.randint(player_x - 1000, player_x - 850)
    x_right = random.randint(player_x + 850, player_x + 1000)
    y_up = random.randint(player_y - 1000, player_y - 850)
    y_down = random.randint(player_y + 850, player_y + 1000)

    new_enemy = {
        "TYPE": type.upper(),
        "X": random.choice([x_left, x_right]), 
        "Y": random.choice([y_up, y_down]),
        "FACING_RIGHT": 1,
        "ATK-COOLDOWN": 500, # Por enquanto é o mesmo cooldown para todos os inimigos
        "LAST-ATK": 0
    }
    
    if new_enemy["TYPE"] == "JAVALI":
        new_enemy["HP"] = 150
        new_enemy["ATK"] = 15
        new_enemy["SPEED"] = 150

        new_enemy["SPRITE"] = Sprite("assets/javali.png", frames = 3)
        new_enemy["SPRITE"].set_total_duration(500)
        
        new_enemy["CHARGE_ACTIVATION_DISTANCE"] = 150
        new_enemy["CHARGE_MODE"] = False
        new_enemy["CHARGED"] = False
        new_enemy["CHARGE_SPEED"] = 300
    elif new_enemy["TYPE"] == "LENHADOR":
        new_enemy["HP"] = 100
        new_enemy["ATK"] = 10
        new_enemy["SPEED"] = 100
        
        new_enemy["SPRITE"] = Sprite("assets/lenhador.png", frames = 3)
        new_enemy["SPRITE"].set_total_duration(1000)
    elif new_enemy["TYPE"] == "CACADOR":
        new_enemy["HP"] = 100
        new_enemy["ATK"] = 0 # Não dá dano meelee
        new_enemy["SPEED"] = 50

        new_enemy["AIMING_TIME"] = 150

        new_enemy["SPRITE"] = Sprite("assets/cacador.png", frames = 3)
        new_enemy["SPRITE"].set_total_duration(1000)
    
    enemies_list.append(new_enemy)

def reset():
    enemies_list.clear()

def cacador_ai(cacador, player_x, player_y, delta_t):
    dir_x = player_x - cacador["X"]
    dir_y = player_y - cacador["Y"]
    distancia = (dir_x**2 + dir_y**2)**0.5 # Teorema de Pitágoras

    if distancia > 0: # Evita divisão por 0
        dir_x /= distancia
        dir_y /= distancia

    if distancia <= 250:
        ui.mostrar_tempo_mira(cacador)

        if cacador["AIMING_TIME"] == 0:
            bullet_spawn(cacador, player_x, player_y)
            cacador["AIMING_TIME"] = 150
        else:
            cacador["AIMING_TIME"] -= 1
            cacador["SPRITE"].set_curr_frame(0)
            cacador["SPRITE"].pause()
    else:
        cacador["AIMING_TIME"] = 150
        cacador["SPRITE"].play()
        cacador["X"] += dir_x * cacador["SPEED"] * delta_t
        cacador["Y"] += dir_y * cacador["SPEED"] * delta_t

def generic_ai(enemy, player_x, player_y, delta_t):
    dir_x = player_x - enemy["X"]
    dir_y = player_y - enemy["Y"]

    distancia = (dir_x**2 + dir_y**2)**0.5 # Teorema de Pitágoras

    if distancia > 0: # Evita divisão por 0
        dir_x /= distancia
        dir_y /= distancia

    enemy["X"] += dir_x * enemy["SPEED"] * delta_t
    enemy["Y"] += dir_y * enemy["SPEED"] * delta_t

def think(cam_offset, delta_t):
    """
    Aqui é definido o comportamento da IA de cada inimigo
    """
    player_x = player["SPRITE"].x + cam_offset[0]
    player_y = player["SPRITE"].y + cam_offset[1]

    for enemy in enemies_list:
        if enemy["TYPE"] == "LENHADOR" or enemy["TYPE"] == "JAVALI":
            generic_ai(enemy, player_x, player_y, delta_t)
        elif enemy["TYPE"] == "CACADOR":
            cacador_ai(enemy, player_x, player_y, delta_t)