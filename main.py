from PPlay.window import *
from PPlay.sound import *

import globals
import states.game as game
from states.menu import main_menu
from states.menu import game_menu
from states.game_over import game_over
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
    elif current_state == "BESTIARIO":
        mostrar_bestiario()

    globals.WINDOW.update()
