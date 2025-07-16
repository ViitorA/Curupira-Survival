# TODO LIST:
# IMPLEMENTAR ITENS
# 1 - PLAYER STATS
# TODO: Colisão com os sprites inimigos quando estão virados p/a esquerda bugado
# TODO: otimizar a detecção de colisão de projéteis igual o do space invaders
# TODO: Ajustar o texto do bestiário
# TODO: Depois adicionar opção de ajustar volume do jogo
# BUGS CONHECIDOS:
# - inimigos spawnando na tua frente, eles spawnam em coordenadas fixas, ajuste para coordenadas a partir do 
# player
# TODO: ADICIONAR EFEITO SONORO DE QUANDO JOGADOR COLETA ITEM AUXILIAR
# TODO: FAZER A MÚSICA DE FUNDO PAUSAR QUANDO APERTAR O BOTÃO DO MENU
# TODO: FAZER ANIMAÇÃO DE CHARGE DO JAVALI
# TODO: Fazer animação idle do curupira
# TODO: OTIMIZAR SEPARAR INIMIGOS
    # Spatial partitioning (dividir o mapa em células e só comparar inimigos próximos)
    # QuadTree (estrutura para dividir o espaço e reduzir comparações)
    # Só comparar inimigos que estão próximos (por distância, antes de criar o Rect)

from PPlay.window import *
from PPlay.sound import *

import globals
import states.game as game
from states.menu import main_menu
from states.menu import game_menu
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

    globals.current_state = "MAIN_MENU"

init()

while True:
    current_state = globals.current_state

    if current_state == "GAME":
        game.run()
    elif current_state == "GAME_OVER":
        game_over()
    elif current_state == "MAIN_MENU":
        main_menu()
    elif current_state == "GAME_MENU":
        game_menu()
    elif current_state == "CONFIG":
        mostrar_configs()
    elif current_state == "BESTIARIO":
        mostrar_bestiario()

    globals.WINDOW.update()
