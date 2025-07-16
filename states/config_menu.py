from PPlay.gameimage import *
from PPlay.sprite import *

import globals
import states.menu as menu
import states.game as game
from utils import clicked

def mostrar_configs():
    WINDOW = globals.WINDOW
    KEYBOARD = globals.KEYBOARD
    MOUSE = globals.MOUSE

    WINDOW.set_background_color(menu.MENU_BG_COLOR)

    manualButton = GameImage("assets/botao-modo-manual.png")
    manualButton.set_position( 100, 100)
    manualButton.draw()

    manualButtonPress = Sprite("assets/press-button.png", frames=2)
    manualButtonPress.set_curr_frame(globals.manual_mode)
    manualButtonPress.set_position(100 + manualButton.width + 40, 
                                   manualButton.y + (manualButton.height - manualButtonPress.height)/2)
    manualButtonPress.draw()

    returnButton = GameImage("assets/botao-voltar.png")
    returnButton.set_position((WINDOW.width - returnButton.width)/2, WINDOW.height - 150)
    returnButton.draw()
    
    # TODO: ALTERAR
    if KEYBOARD.key_pressed("ESC") or clicked(MOUSE, returnButton): 
        # Ele precisa ver se vai retornar pro main menu ou pro game menu
        globals.current_state = "GAME_MENU" if game.is_running else "MAIN_MENU"

    if clicked(MOUSE, manualButtonPress): 
        globals.manual_mode = 1 - globals.manual_mode # inverte