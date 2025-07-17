from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.sound import *

from ui import desenhar_ui
import globals
import utils
import player
import enemies
import objects
import waves
from states.bestiario import atualizar_abates
import random

cam_offset = [0,0]

is_running = False
start_time = None  
delta_t = None

BG_MUSIC = Sound("assets/audio/bg1_the-gensokyo-the-gods-loved.mp3")
music_playing = False

death_count = {
    "JAVALI" : 0,
    "LENHADOR" : 0,
    "CACADOR" :0
} 

game_items = []

def update_scenario(): 
    """
    Atualiza as coordenadas reais de cada objeto e inimigo no cenário
    Obs. 1: Coordenada real -> A coordenada de fato do objeto
            Coordenada corrigida com offset -> A coordenada de onde o objeto está na tela corrigido com o offset da câmera

    Obs. 2: Coordenadas reais de objetos estáticos não são atualizadas pois eles não se movimentam
    """
    global delta_t

    for object in objects.objects_list:
        if object["TYPE"] == "FIREBALL" or object["TYPE"] == "BULLET":
            object["X"] += object["DIR_X"] * object["SPEED"] * delta_t
            object["Y"] += object["DIR_Y"] * object["SPEED"] * delta_t

def draw_scenario(): 
    """ 
    Desenha os sprites nas coordenadas corrigidas com o offset
    Obs.: Coordenada corrigida com offset -> A coordenada de onde o objeto está na tela corrigido com o offset da câmera
    """
    for object in objects.objects_list:
        object["SPRITE"].set_position(object["X"] - cam_offset[0], object["Y"] - cam_offset[1])

        if object["TYPE"] == "ARROW":
            sprite = object["SPRITE"]

            rotated_surface = object["ROTATED_SURFACE"]
            rect = rotated_surface.get_rect(center=(sprite.x, sprite.y))

            globals.WINDOW.get_screen().blit(rotated_surface, rect)
        elif object["TYPE"] == "FIREBALL":
            object["SPRITE"].update()
            object["SPRITE"].draw()
        elif object["TYPE"] == "XP":
            object["SPRITE"].update()
            object["SPRITE"].draw()
        else:
            object["SPRITE"].draw()

    for enemy in enemies.enemies_list:
        enemy["SPRITE"].set_position(enemy["X"] - cam_offset[0], enemy["Y"] - cam_offset[1])
        enemy["SPRITE"].update()

        if enemy["SPRITE"].x > player.player["SPRITE"].x:
            enemy["FACING_RIGHT"] = 0
        else:
            enemy["FACING_RIGHT"] = 1

        utils.draw_sprite(enemy)

def collision_detection():
    WINDOW = globals.WINDOW

    # P/a ficar menos verboso
    player_sprite = player.player["SPRITE"]

    X_MIN, X_MAX = player_sprite.x - WINDOW.width, player_sprite.x + WINDOW.width
    Y_MIN, Y_MAX = player_sprite.y - WINDOW.height, player_sprite.y + WINDOW.height

    for object in objects.objects_list:
        if object["TYPE"] == "FIREBALL":
            # VERIFICAÇÃO DE COLISÃO COM INIMIGO
            for enemy in enemies.enemies_list:
                enemy_sprite = enemy["SPRITE"]
                fireball_sprite = object["SPRITE"]

                verificavel = not(enemy_sprite.x > fireball_sprite.x + fireball_sprite.width or
                                  enemy_sprite.x + enemy_sprite.width < fireball_sprite.x or
                                  enemy_sprite.y > fireball_sprite.y + fireball_sprite.height or
                                  enemy_sprite.y + enemy_sprite.height < fireball_sprite.y
                                  )

                if verificavel:
                    objects.drop_xp(enemy)

                    # Chance de 10% de dropar comida
                    if random.random() < 0.1:
                        objects.spawn("Comida", enemy["X"] + 10, enemy["Y"] + 10)

                    objects.objects_list.remove(object)
                    enemies.enemies_list.remove(enemy)
                    player.player["ENEMIES_KILLED"] += 1
                    death_count[enemy["TYPE"]] += 1
                    break

            # Verifica se saiu dos limites da "tela". Não preciso me preocupar com o tamanho exato do sprite, já que essa remoção não será vista pelo jogador
            if not(X_MIN <= object["SPRITE"].x <= X_MAX and Y_MIN <= object["SPRITE"].y <= Y_MAX): 
                objects.objects_list.remove(object)
                
        elif object["TYPE"] == "BULLET":
            verificavel = not(player_sprite.x > object["SPRITE"].x + object["SPRITE"].width or
                              player_sprite.x + player_sprite.width < object["SPRITE"].x or
                              player_sprite.y > object["SPRITE"].y + object["SPRITE"].height or
                              player_sprite.y + player_sprite.height < object["SPRITE"].y
                              )
            
            if verificavel and object["SPRITE"].collided_perfect(player_sprite):
                dano = max(object["DAMAGE"] - player.player.get("RES", 0), 1)
                player.player["HP"] -= dano
                globals.HIT_SOUND.play()
                objects.objects_list.remove(object)
            
            if not(X_MIN <= object["SPRITE"].x <= X_MAX and Y_MIN <= object["SPRITE"].y <= Y_MAX): 
                objects.objects_list.remove(object)
        elif object["TYPE"] == "XP" and object["SPRITE"].collided(player_sprite):
                player.player["XP"] += object["VALUE"]
                globals.XP_SOUND.play()
                objects.objects_list.remove(object)
        elif object["TYPE"] == "Comida" and object["SPRITE"].collided(player_sprite):
            player.player["HP"] = min(player.player["HP"] + 20, player.player["HP_MAX"])
            objects.objects_list.remove(object)
    
    for enemy in enemies.enemies_list:
        verificavel = True
        if enemy["SPRITE"].x > player_sprite.x + player_sprite.width:
            verificavel = False
        elif enemy["SPRITE"].x + enemy["SPRITE"].width < player_sprite.x:
            verificavel = False
        elif enemy["SPRITE"].y + enemy["SPRITE"].height < player_sprite.y:
            verificavel = False
        elif enemy["SPRITE"].y > player_sprite.y + player_sprite.height:
            verificavel = False

        if verificavel and pygame.time.get_ticks() - enemy["LAST-ATK"] > enemy["ATK-COOLDOWN"]:
            if enemy["SPRITE"].collided_perfect(player_sprite):
                dano = max(enemy["ATK"] - player.player.get("RES", 0), 1)
                player.player["HP"] -= dano
                globals.HIT_SOUND.play()
                enemy["LAST-ATK"] = pygame.time.get_ticks()

def separar_inimigos():
    # Otimizado: evita pares repetidos e reduz cálculos desnecessários
    n = len(enemies.enemies_list)
    force = 1.5  # ajuste conforme necessário
    for i in range(n):
        enemy_a = enemies.enemies_list[i]
        rect_a = pygame.Rect(enemy_a["X"], enemy_a["Y"], enemy_a["SPRITE"].width, enemy_a["SPRITE"].height)
        for j in range(i + 1, n):
            enemy_b = enemies.enemies_list[j]
            rect_b = pygame.Rect(enemy_b["X"], enemy_b["Y"], enemy_b["SPRITE"].width, enemy_b["SPRITE"].height)
            if rect_a.colliderect(rect_b):
                dx = rect_a.centerx - rect_b.centerx
                dy = rect_a.centery - rect_b.centery
                dist = max((dx**2 + dy**2)**0.5, 1)
                sep_x = (dx / dist) * force * 0.5
                sep_y = (dy / dist) * force * 0.5
                enemy_a["X"] += sep_x
                enemy_a["Y"] += sep_y
                enemy_b["X"] -= sep_x
                enemy_b["Y"] -= sep_y

def game_init():
    global is_running, start_time, BG_MUSIC, music_playing, game_items
    is_running = True
    start_time = pygame.time.get_ticks()
    
    game_items = [
        {"NAME": "Bola De Fogo", "TYPE": "ATK-COOLDOWN", "EFFECT": -100, 
         "ICON": GameImage("assets/fireball_icon.png"), 
         "BIG_ICON": GameImage("assets/fireball_bicon.png")},
        
        {"NAME": "Botas Mágicas", "EFFECT": 5, "TYPE": "SPD", 
         "ICON": GameImage("assets/botas-magicas_icon.png"), 
         "BIG_ICON": GameImage("assets/botas-magicas_icon2.png")}, 

        {"NAME": "Armadura De Couro", "EFFECT": 20, "TYPE": "HP_MAX", 
         "ICON": GameImage("assets/armadura-couro_icon.png"), 
         "BIG_ICON": GameImage("assets/armadura-couro_bicon.png")},

        {"NAME": "Comida", "EFFECT": 20, "TYPE": "HP", 
         "ICON": GameImage("assets/comida.png"), 
         "BIG_ICON": GameImage("assets/comida_bicon.png")}
    ]

    player.spawn()
    cam_offset[0] = player.player["SPRITE"].x - globals.WINDOW.width // 2
    cam_offset[1] = player.player["SPRITE"].y - globals.WINDOW.height // 2

    BG_MUSIC.loop = True
    BG_MUSIC.play()
    BG_MUSIC.set_volume(50)
    music_playing = True
    globals.HIT_SOUND = Sound("assets/audio/hit.wav")
    globals.XP_SOUND = Sound("assets/audio/xp.wav")


def run():
    # P/a o código ficar menos verboso
    WINDOW = globals.WINDOW
    KEYBOARD = globals.KEYBOARD
    MOUSE = globals.MOUSE

    global is_running, start_time, delta_t, music_playing
    delta_t = WINDOW.delta_time()

    if not is_running:
        game_init()
    
    if not music_playing:
        BG_MUSIC.unpause()
        music_playing = True
        
    if KEYBOARD.key_pressed("ESC"):
        BG_MUSIC.pause()
        music_playing = False
        globals.current_state = "GAME_MENU"
        atualizar_abates(death_count.copy())

    player.input(KEYBOARD, MOUSE)
    utils.draw_background(WINDOW, cam_offset)

    waves.auto_wave(cam_offset)
    collision_detection()
    update_scenario()
    separar_inimigos()
    draw_scenario()

    player.update_info()
    utils.draw_sprite(player.player) 

    if enemies.enemies_list != []: enemies.think(cam_offset, delta_t)

    desenhar_ui(player.player)

    if player.player["HP"] <= 0:
        BG_MUSIC.stop()
        Sound("assets/audio/game-over.wav").play()
        atualizar_abates(death_count.copy())  # Salva os abates
        utils.reset_modules_vars()
        reset_game_vars()
        globals.current_state = "GAME_OVER"

def reset_game_vars():
    global is_running, start_time, delta_t, cam_offset
    is_running = False
    start_time = None
    delta_t = None

    cam_offset = [0,0]
