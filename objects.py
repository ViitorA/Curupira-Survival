import random
import math

from PPlay.sprite import *
import player

objects_list = []

def spawn(type):
    new_object = {
        "TYPE": type.upper(),
        "X": random.randint(0, 800), 
        "Y": random.randint(0, 800),
    }
    
    if new_object["TYPE"] == "BAU":
     new_object["SPRITE"] = Sprite("assets/bau.png")
    elif new_object["TYPE"] == "COMIDA":
     new_object["SPRITE"] = Sprite("assets/comida.png")
    elif new_object["TYPE"] == "RELOGIO":
     new_object["SPRITE"] = Sprite("assets/relogio.png")

    objects_list.append(new_object)

def bullet_spawn(enemy, target_x, target_y):
    sprite_w = enemy["SPRITE"].width
    sprite_h = enemy["SPRITE"].height

    # Corrige o x e o y para ficar no meio:
    sprite_x = enemy["SPRITE"].x + sprite_w//2
    sprite_y = enemy["SPRITE"].y + sprite_h//2

    dx = target_x - sprite_x
    dy = target_y - sprite_y
    distancia = (dx**2 + dy**2)**0.5

    #angle = math.degrees(math.atan2(-dy,dx))
    spawn_pos_x = sprite_x
    spawn_pos_y = sprite_y
    """
    print(int(angle))

    if -45 < int(angle) < 45: # Spawna na direita do player
       spawn_pos_x += player_width//2 + 20
       print("DIREITA")  
    elif 45 < int(angle) < 135: # Spawna em cima do player=
       spawn_pos_y -= player_height//2 + 20
       print("CIMA")
    elif 135 < int(angle) < -135: # Spawna na esquerda do player
       print("ESQUERDA")
       spawn_pos_x -= player_width//2 + 20
    elif -135 < int(angle) < -45: # Spawna embaixo do player
       print("EMBAIXO")
       spawn_pos_y += player_height//2 + 20
    """

    if distancia == 0: # Evita divisão por 0
        dir_x, dir_y = 0,0
    else:
        dir_x = dx / distancia
        dir_y = dy / distancia

    bullet = {
        "TYPE": "BULLET",
        "SPEED": 300,
        "X": spawn_pos_x,
        "Y": spawn_pos_y,
        "DIR_X": dir_x,
        "DIR_Y": dir_y,
        "SPRITE": Sprite("assets/bullet.png"),
    }

    objects_list.append(bullet)

def fireball_spawn(player_x, player_y, target_x, target_y):
    player_width = player.player["SPRITE"].width
    player_height = player.player["SPRITE"].height

    # Corrige o x e o y para ficar no meio:
    player_x += player_width//2
    player_y += player_height//2

    dx = target_x - player_x
    dy = target_y - player_y
    distancia = (dx**2 + dy**2)**0.5

    angle = math.degrees(math.atan2(-dy,dx))
    
    print(int(angle))
    spawn_pos_x = player_x
    spawn_pos_y = player_y
    if -45 < int(angle) < 45: # Spawna na direita do player
       spawn_pos_x += player_width//2 + 20
       print("DIREITA")  
    elif 45 < int(angle) < 135: # Spawna em cima do player=
       spawn_pos_y -= player_height//2 + 20
       print("CIMA")
    elif 135 < int(angle) < -135: # Spawna na esquerda do player
       print("ESQUERDA")
       spawn_pos_x -= player_width//2 + 20
    elif -135 < int(angle) < -45: # Spawna embaixo do player
       print("EMBAIXO")
       spawn_pos_y += player_height//2 + 20

    if distancia == 0: # Evita divisão por 0
        dir_x, dir_y = 0,0
    else:
        dir_x = dx / distancia
        dir_y = dy / distancia

    fireball = {
        "TYPE": "FIREBALL",
        "SPEED": 300,
        "X": spawn_pos_x,
        "Y": spawn_pos_y,
        "DIR_X": dir_x,
        "DIR_Y": dir_y,
        "SPRITE": Sprite("assets/bola-fogo.png", frames=4),
    }
    fireball["SPRITE"].set_total_duration(300)
    objects_list.append(fireball)

def arrow_spawn(player_x, player_y, target_x, target_y):
    player_width = player.player["SPRITE"].width
    player_height = player.player["SPRITE"].height

    # Corrige o x e o y para ficar no meio:
    player_x += player_width//2
    player_y += player_height//2

    dx = target_x - player_x
    dy = target_y - player_y
    distancia = (dx**2 + dy**2)**0.5

    angle = math.degrees(math.atan2(-dy,dx))
    
    print(int(angle))
    spawn_pos_x = player_x
    spawn_pos_y = player_y
    if -45 < int(angle) < 45: # Spawna na direita do player
       spawn_pos_x += player_width//2 + 20
       print("DIREITA")  
    elif 45 < int(angle) < 135: # Spawna em cima do player=
       spawn_pos_y -= player_height//2 + 20
       print("CIMA")
    elif 135 < int(angle) < -135: # Spawna na esquerda do player
       print("ESQUERDA")
       spawn_pos_x -= player_width//2 + 20
    elif -135 < int(angle) < -45: # Spawna embaixo do player
       print("EMBAIXO")
       spawn_pos_y += player_height//2 + 20

    if distancia == 0: # Evita divisão por 0
        dir_x, dir_y = 0,0
    else:
        dir_x = dx / distancia
        dir_y = dy / distancia

    new_arrow = {
        "TYPE": "ARROW",
        "SPEED": 300,
        "X": spawn_pos_x,
        "Y": spawn_pos_y,
        "DIR_X": dir_x,
        "DIR_Y": dir_y,
        "SPRITE": Sprite("assets/flecha.png"),
    }
    new_arrow["ROTATED_SURFACE"] = pygame.transform.rotate(new_arrow["SPRITE"].image, angle)

    objects_list.append(new_arrow)

def drop_xp(enemy):
    xp_drop = {
        "TYPE": "XP",
        "X": enemy["X"],
        "Y": enemy["Y"],
        "SPRITE": Sprite("assets/xp.png", frames = 4)
    }
    xp_drop["SPRITE"].set_total_duration(300)

    if enemy["TYPE"] == "JAVALI": # Dropa 5 XP
        xp_drop["VALUE"] = 5
    elif enemy["TYPE"] == "LENHADOR": # Dropa 10 xp
        xp_drop["VALUE"] = 10
    elif enemy["TYPE"] == "CACADOR": # Dropa 20 xp
        xp_drop["VALUE"] = 15
    
    objects_list.append(xp_drop)

def reset():
   objects_list.clear()