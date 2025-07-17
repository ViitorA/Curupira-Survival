import globals
from utils import clicked
from PPlay.gameimage import *

MENU_BG_COLOR = (22,158,38)

def main_menu():
    WINDOW = globals.WINDOW
    MOUSE = globals.MOUSE

    WINDOW.set_background_color(MENU_BG_COLOR)

    BUTTON_WIDTH = GameImage("assets/botao-jogar.png").width
    BUTTON_HEIGHT = GameImage("assets/botao-jogar.png").height
    MEIO = (WINDOW.height - BUTTON_HEIGHT)/2
    PADDING = 20

    play_button = GameImage("assets/botao-jogar.png")
    play_button.set_position((WINDOW.width - BUTTON_WIDTH)/2, MEIO - BUTTON_HEIGHT - PADDING)
    play_button.draw()    

    bestiario_button = GameImage("assets/botao-bestiario.png")
    bestiario_button.set_position((WINDOW.width - BUTTON_WIDTH)/2, MEIO)
    bestiario_button.draw()

    exit_button = GameImage("assets/botao-sair.png")
    exit_button.set_position( (WINDOW.width - BUTTON_WIDTH)/2, MEIO + BUTTON_HEIGHT + PADDING)
    exit_button.draw()

    if clicked(MOUSE, play_button):
        globals.current_state = "GAME"
    elif clicked(MOUSE, bestiario_button):
        globals.current_state = "BESTIARIO"
    elif clicked(MOUSE, exit_button):
        WINDOW.close()

def game_menu():
    WINDOW = globals.WINDOW
    MOUSE = globals.MOUSE

    WINDOW.set_background_color(MENU_BG_COLOR)

    BUTTON_WIDTH = GameImage("assets/botao-jogar.png").width
    BUTTON_HEIGHT = GameImage("assets/botao-jogar.png").height
    MEIO_Y = (WINDOW.height - BUTTON_HEIGHT)/2
    MEIO_X = (WINDOW.width - BUTTON_WIDTH)/2
    PADDING = 20

    return_button = GameImage("assets/botao-voltar.png")
    return_button.set_position(MEIO_X, MEIO_Y - BUTTON_HEIGHT - PADDING)
    return_button.draw()

    exit_button = GameImage("assets/botao-sair.png")
    exit_button.set_position( MEIO_X, MEIO_Y + BUTTON_HEIGHT + PADDING)
    exit_button.draw()

    if clicked(MOUSE, return_button):
        globals.current_state = "GAME"
    elif clicked(MOUSE, exit_button):
        WINDOW.close()