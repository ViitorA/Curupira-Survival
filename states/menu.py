import globals
from utils import clicked
from PPlay.gameimage import *

MENU_BG_COLOR = (22,158,38)

def mostrar_menu():
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

    config_button = GameImage("assets/botao-configuracoes.png")
    config_button.set_position((play_button.x)/2 - PADDING, MEIO)
    config_button.draw()

    exit_button = GameImage("assets/botao-sair.png")
    exit_button.set_position( (WINDOW.width - BUTTON_WIDTH)/2, MEIO + BUTTON_HEIGHT + PADDING)
    exit_button.draw()

    bestiario_button = GameImage("assets/botao-bestiario.png")
    bestiario_button.set_position((play_button.x)/2 + play_button.width + PADDING, MEIO)
    bestiario_button.draw()

    if clicked(MOUSE, play_button):
        globals.current_state = "GAME"
    elif clicked(MOUSE, config_button):
        globals.current_state = "CONFIG"
    elif clicked(MOUSE, exit_button):
        WINDOW.close()
    elif clicked(MOUSE, bestiario_button):
        globals.current_state = "BESTIARIO"