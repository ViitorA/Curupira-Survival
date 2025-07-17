import pygame
import globals
import utils
import states.game as game
from PPlay.gameimage import *
from PPlay.sprite import *
from player import player
from player import player_items

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (88,97,98)
RED = (173, 24, 24)

FONTE = 'Tahoma'

# "segunda camda" da UI, logo embaixo da barra de XP
y_ui = 60  # 60 = barra_xp_height + 10 de padding
 
def mostrar_drops(i1, i2, i3):
    WINDOW = globals.WINDOW
    centro_x = WINDOW.width // 2
    centro_y = WINDOW.height // 2

    x0 = centro_x - 300
    y0 = centro_y - 300
    pygame.draw.rect(WINDOW.get_screen(), BLACK, (x0, y0, 600, 600))
    pygame.draw.rect(WINDOW.get_screen(), GRAY, (x0 + 10, y0 + 10, 580, 580))
    
    # TODO: MELHORAR ESSE CÓDIGO HORRROSO
    WINDOW.draw_text("SELECIONE UM ITEM:", x0 + 40, y0 + 30, size = 30, color=WHITE, font_name=FONTE, bold=True, italic=False)
    PADDING = 20
    SIZE = 165
    BOXES_Y = y0 + 200

    WINDOW.draw_text(i1["NAME"], x0 + 30, BOXES_Y - 30, size = 15, color=WHITE, font_name=FONTE, bold=True, italic=False)
    pygame.draw.rect(WINDOW.get_screen(), BLACK, (x0 + 30, BOXES_Y, SIZE, SIZE))
    pygame.draw.rect(WINDOW.get_screen(), WHITE, (x0 + 40, BOXES_Y + 10, SIZE - PADDING, SIZE - PADDING))
    i1["BIG_ICON"].set_position(x0 + 40 + 5, BOXES_Y + 10 + 5)
    i1["BIG_ICON"].draw()
    WINDOW.draw_text(str(i1["EFFECT"]) + ' ' + i1["TYPE"], x0 + 30, BOXES_Y + SIZE + PADDING, size = 15, color=WHITE, font_name=FONTE, bold=True, italic=False)
    

    BOX2_X = x0 + 30 + SIZE + PADDING 
    WINDOW.draw_text(i2["NAME"], BOX2_X, BOXES_Y - 30, size = 15, color=WHITE, font_name=FONTE, bold=True, italic=False)
    pygame.draw.rect(WINDOW.get_screen(), BLACK, (BOX2_X, BOXES_Y, SIZE, SIZE))
    pygame.draw.rect(WINDOW.get_screen(), WHITE, (BOX2_X + 10 , BOXES_Y + 10, SIZE - PADDING, SIZE - PADDING))
    i2["BIG_ICON"].set_position(BOX2_X + 10 + 5, BOXES_Y + 10 + 5)
    i2["BIG_ICON"].draw()
    WINDOW.draw_text(str(i2["EFFECT"]) + ' ' + i2["TYPE"], BOX2_X, BOXES_Y + SIZE + PADDING, size = 15, color=WHITE, font_name=FONTE, bold=True, italic=False)

    BOX3_X = x0 + 30 + 2*SIZE + 2*PADDING
    WINDOW.draw_text(i3["NAME"], BOX3_X, BOXES_Y - 30, size = 15, color=WHITE, font_name=FONTE, bold=True, italic=False)
    pygame.draw.rect(WINDOW.get_screen(), BLACK, (BOX3_X, BOXES_Y, SIZE, SIZE))
    pygame.draw.rect(WINDOW.get_screen(), WHITE, (BOX3_X + 10, BOXES_Y + 10, SIZE - PADDING, SIZE - PADDING))
    i3["BIG_ICON"].set_position(BOX3_X + 10 + 5, BOXES_Y + 10 + 5)
    i3["BIG_ICON"].draw()
    WINDOW.draw_text(str(i3["EFFECT"]) + ' ' + i3["TYPE"], BOX3_X, BOXES_Y + SIZE + PADDING, size = 15, color=WHITE, font_name=FONTE, bold=True, italic=False)

    if globals.MOUSE.is_button_pressed(1) and globals.MOUSE.is_over_object(i1["BIG_ICON"]):
        return 1
    elif globals.MOUSE.is_button_pressed(1) and globals.MOUSE.is_over_object(i2["BIG_ICON"]):
        return 2
    elif globals.MOUSE.is_button_pressed(1) and globals.MOUSE.is_over_object(i3["BIG_ICON"]):
        return 3

    WINDOW.update()

def mostrar_cronometro(window): # Mostra na tela há quanto tempo o jogador iniciou a partida
    tempo_atual = pygame.time.get_ticks() - game.start_time
    segundos_decorridos = tempo_atual // 1000 # Converte em segundos

    # Formata o tempo (MM:SS)
    minutos = segundos_decorridos // 60
    segundos = segundos_decorridos % 60
    cronometro = f"{minutos:02d}:{segundos:02d}"

    # Renderiza o texto
    text_surface = pygame.font.SysFont(FONTE, 40).render(cronometro, True, WHITE)
    text_rect = text_surface.get_rect() # Vê o tamanho do texto renderizado
    text_rect.centerx = window.width //2 # Posição X

    # Desenha na tela o texto
    window.draw_text(cronometro, text_rect.x, y_ui, size = 40, color = WHITE, font_name = FONTE, bold = True, italic = False)

def mostrar_itens(janela): # Desenha os "contâiners" dos itens
    global y_ui

    pygame.draw.rect(janela.get_screen(), BLACK, (10, y_ui, 30*5 + 5*6, 30*2 + 5*3))
    
    slot_width = 30
    slot_height = 30
    padding = 5
    slots_per_row = 5

    # Itera sobre todos os itens do jogador para desenhar os slots e os ícones
    for idx in range(len(player_items)):
        # Calcula a linha e coluna do slot atual
        row = idx // slots_per_row
        col = idx % slots_per_row

        # Calcula a pos do desenho do slot na tela
        x = 15 + col * (slot_width + padding)
        y = y_ui + 5 + row * (slot_height + padding)

        # Desenha o retângulo do slot
        pygame.draw.rect(janela.get_screen(), GRAY, (x, y, slot_width, slot_height))
        
        item = player_items[idx]
        if item is not None:
            # Centraliza
            icon_x = x + slot_width // 2 - item["ICON"].width // 2
            icon_y = y + slot_height // 2 - item["ICON"].height // 2
            
            item["ICON"].set_position(icon_x, icon_y)
            item["ICON"].draw()

def desenhar_barra_xp(janela):
    WINDOW = globals.WINDOW

    barra_xp_width = janela.width
    barra_xp_height = 50

    #print("PLAYER XP: " + str(player["XP"]))
    xp_ratio = min(player["XP"] / player["XP_MAX"], 1)
    xp_fill_width = int(barra_xp_width * xp_ratio)

    # DESENHA A BARRA DE XP VAZIA
    pygame.draw.rect(janela.get_screen(), BLACK, (0,0, barra_xp_width, barra_xp_height))
    pygame.draw.rect(janela.get_screen(), (255,249,89), (0,0, barra_xp_width, barra_xp_height),2)

    # PREENCHE A BARRA
    pygame.draw.rect(janela.get_screen(), (143,250,55), (0,0, xp_fill_width, barra_xp_height))

def desenhar_barra_vida(window):
    largura_barra_hp = 100
    
    # DESENHA A BARRA DE HP VAZIA
    pygame.draw.rect(window.get_screen(), BLACK, (player["SPRITE"].x - 100/4, 
                                                  player["SPRITE"].y + player["SPRITE"].height + 5, 
                                                  largura_barra_hp, 20))
    
    barra_preenchida = (player["HP"] / player["HP_MAX"]) * largura_barra_hp

    # DESENHA A BARRA COM A VIDA ATUAL DO JOGADOR
    pygame.draw.rect(window.get_screen(), RED, (player["SPRITE"].x - 100/4, 
                                                player["SPRITE"].y + player["SPRITE"].height + 5,
                                                barra_preenchida, 20))

def mostrar_inimigos_mortos(window):
    caveira = GameImage("assets/ui_caveira.png")
    caveira.set_position(window.width - caveira.width -  10, y_ui)
    caveira.draw()

    text = pygame.font.SysFont('Tahoma', 25).render(str(player["ENEMIES_KILLED"]), True, (255,255,255))
    text_rect = text.get_rect()
    
    window.draw_text(str(player["ENEMIES_KILLED"]), 
                     caveira.x - text_rect.width - 10, 
                     caveira.y + 2, 
                     size = 25, 
                     color = WHITE, 
                     font_name = FONTE, 
                     bold = False, 
                     italic = False)

def mostrar_tempo_mira(enemy):
    x = (enemy["SPRITE"].x + enemy["SPRITE"].width/2) - 40 if enemy["FACING_RIGHT"] else (enemy["SPRITE"].x + enemy["SPRITE"].width/2)    
    y = enemy["SPRITE"].y - 35
    globals.WINDOW.draw_text(str(enemy["AIMING_TIME"]), x, y,
                             size = 25,
                             color=WHITE,
                             font_name=FONTE,
                             bold = False,
                             )

def desenhar_ui(player):
    WINDOW = globals.WINDOW

    barra_xp_height = 50
    
    desenhar_barra_xp(WINDOW)

    # MOSTRA O NÍVEL DO JOGADOR
    WINDOW.draw_text( "LVL " + str(player["LEVEL"]), WINDOW.width - 70, barra_xp_height/4 , size = 25, color = WHITE, font_name = FONTE, bold = False, italic = False)

    # MOSTRA A QTD DE INIMIGOS MORTOS
    mostrar_inimigos_mortos(WINDOW)

    mostrar_cronometro(WINDOW)
    mostrar_itens(WINDOW)

    # Mostra barra de vida do player
    desenhar_barra_vida(WINDOW)
