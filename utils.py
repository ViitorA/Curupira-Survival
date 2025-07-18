import pygame
import globals,objects,player,enemies,waves
from PPlay.gameimage import *

DELAY_ENTRE_CLIQUES = 300
ultimo_clique = 0

def clicked(mouse, button):
    global ultimo_clique, DELAY_ENTRE_CLIQUES

    tempo_atual = pygame.time.get_ticks()
    clicou = mouse.is_button_pressed(1) and mouse.is_over_object(button) and tempo_atual - ultimo_clique > DELAY_ENTRE_CLIQUES

    if clicou: ultimo_clique = tempo_atual
    return clicou

def draw_sprite(object):
    if (object["FACING_RIGHT"]): # Quando o sprite está do jeito que tá nos sprites é mais fácil
        object["SPRITE"].draw()
    else:
        # Poderia ter copiado e colado o desenho invertido de cada sprite, mas fiz isso por ser mais 
        # interessante e escalável
        sprite = object["SPRITE"]
        sprite_width = sprite.width
        sprite_height = sprite.height
        curr_frame = sprite.get_curr_frame()
        image = sprite.image

        # Recorta o frame atual
        frame_surface = image.subsurface(pygame.Rect(curr_frame * sprite_width, 0, sprite_width, sprite_height))
        
        # Gira horizontalmente o frame recortado
        flipped_surface = pygame.transform.flip(frame_surface, True, False)
        
        # Desenha na tela
        globals.WINDOW.get_screen().blit(flipped_surface, (sprite.x, sprite.y))

def draw_background(window, cam_offset):
    tile = GameImage("assets/grass.png")
    tile_w, tile_h = tile.width, tile.height # Tamanho dos tiles

    # Calcula o início do grid para cobrir toda a tela
    # Calcula as coordenadas x e y p/a começar a desenhar os tiles
    # Obs.: o % serve p/a alinhar os tiles com a posição da câmera
    # Exemplo: se a câmera se move para a direita, o cam_offset[0] aumenta. O % tile_w pega apenas 
    # quanto a câmera avançou além do tamanho de um tile.
    # Obs.: o - inverte o valor, fazendo com que o tile seja deslocado p/a trás
    start_x = -((cam_offset[0]) % tile_w)
    start_y = -((cam_offset[1]) % tile_h)

    # Calcula quantos tiles cabem na tela (+2 para garantir cobertura)
    tiles_x = window.width // tile_w + 2
    tiles_y = window.height // tile_h + 2

    for i in range(tiles_x):
        for j in range(tiles_y):
            x = start_x + i * tile_w
            y = start_y + j * tile_h
            tile.set_position(x, y)
            tile.draw()

def reset_modules_vars():
    # Volta os dados do jogo p/a o estado inicial  
    player.reset()
    objects.reset()
    enemies.reset()
    waves.reset()