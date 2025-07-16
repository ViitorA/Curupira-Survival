# TODO LIST:
# IMPLEMENTAR ITENS
# 1 - PLAYER STATS
# TODO: otimizar a detecção de colisão de projéteis igual o do space invaders
# TODO: Implementar colisão para inimigos não ficar o sprite um em cima do outro
# BUGS CONHECIDOS:
# - inimigos spawnando na tua frente, eles spawnam em coordenadas fixas, ajuste para coordenadas a partir do 
# player
# TODO: ADICIONAR EFEITO SONORO DE QUANDO JOGADOR COLETA ITEM AUXILIAR
# TODO: FAZER A MÚSICA DE FUNDO PAUSAR QUANDO APERTAR O BOTÃO DO MENU
# TODO: FAZER ANIMAÇÃO DE CHARGE DO JAVALI
# TODO: Fazer animação idle do curupira

from PPlay.window import *
from PPlay.sound import *

import globals
import states.game as game
from states.menu import mostrar_menu
from states.game_over import game_over
from states.config_menu import mostrar_configs
from states.bestiario import mostrar_bestiario


def init():
    """
    Inicializa algumas variáveis globais do programa
    """
    globals.WINDOW = Window(1000,800)
    globals.WINDOW.set_title("Curupira Survival")

    globals.KEYBOARD = globals.WINDOW.get_keyboard()
    globals.MOUSE = globals.WINDOW.get_mouse()

    globals.current_state = "MENU"

init()

while True:
    current_state = globals.current_state

    if current_state == "GAME":
        game.run()
    elif current_state == "GAME_OVER":
        game_over()
    elif current_state == "MENU":
        mostrar_menu()
        globals.WINDOW.update()
    elif current_state == "CONFIG":
        mostrar_configs()
        globals.WINDOW.update()
    elif current_state == "BESTIARIO":
        mostrar_bestiario()
        globals.WINDOW.update()
