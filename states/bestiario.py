import globals
import json
from PPlay.sprite import * 

MENU_BG_COLOR = (22,158,38)


def carregar_abates():
    try:
        with open('abates.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    
def atualizar_abates(death_conts):
    abates_data = carregar_abates()
    abates_dict = {item['TYPE']: item for item in abates_data}

    for tipo, nova_morte in death_conts.items():
        if tipo in abates_dict:
            abates_dict[tipo]['ABATES'] += nova_morte
        else:
            abates_dict[tipo] = {'TYPE': tipo, 'ABATES': nova_morte}

    updated_abates_lista = list(abates_dict.values())    

    with open('abates.json', 'w') as f:
        json.dump(updated_abates_lista, f, indent=4)        

def mostrar_bestiario():
    WINDOW = globals.WINDOW
    KEYBOARD = globals.KEYBOARD

    WINDOW.set_background_color(MENU_BG_COLOR)

    PADDING = 50
    MEIO = WINDOW.height/2

    javali = Sprite("assets/javali1.png", frames = 1)
    javali.set_position(PADDING, PADDING)
    javali.draw()

    lenhador = Sprite("assets/lenhador1.png", frames = 1)
    lenhador.set_position(WINDOW.width - PADDING - lenhador.width, MEIO - lenhador.height)
    lenhador.draw()

    bar_1 = Sprite("assets/barra.png")
    bar_1.set_position((WINDOW.width - bar_1.width)/2, lenhador.y - javali.y)
    bar_1.draw()

    cacador = Sprite("assets/cacador1.png", frames = 1)
    cacador.set_position(PADDING,  MEIO + MEIO/2)
    cacador.draw()

    bar_2 = Sprite("assets/barra.png")
    bar_2.set_position((WINDOW.width - bar_2.width)/2, cacador.y - lenhador.height)
    bar_2.draw()

    line_height = 25
    text_x = javali.x + javali.width + PADDING
    WINDOW.draw_text("Javalis: Criaturas antes pacíficas, corrompidas pela ganância", text_x, 
                     javali.y, size=25, color=(0, 0, 0))
    WINDOW.draw_text("dos invasores. Atacam com presas afiadas, destruindo a", text_x, 
                     javali.y + line_height, size=25, color=(0, 0, 0))
    WINDOW.draw_text("vegetação e ameaçando o equilíbrio da floresta.", text_x, 
                     javali.y + 2 * line_height, size=25, color=(0, 0, 0))

    WINDOW.draw_text("Lenhadores: Homens impiedosos que veem a floresta como lucro.", PADDING, lenhador.y, size=25, color=(0, 0, 0))
    WINDOW.draw_text("Seus machados derrubam árvores centenárias sem remorso,", PADDING, lenhador.y + line_height, size=25, color=(0, 0, 0))
    WINDOW.draw_text("abrindo caminho para a destruição da mata.", PADDING, lenhador.y + 2 * line_height, size=25, color=(0, 0, 0))

    WINDOW.draw_text("Caçadores: Invasores letais, movidos pela cobiça de capturar", text_x, cacador.y, size=25, color=(0, 0, 0))
    WINDOW.draw_text("as criaturas mágicas. Armados com espingardas, são um", text_x, cacador.y + line_height, size=25, color=(0, 0, 0))
    WINDOW.draw_text("perigo mortal e um desafio direto ao Curupira.", text_x, cacador.y + 2 * line_height, size=25, color=(0, 0, 0))

    abates_atual = carregar_abates()
    for i, entrada in enumerate(abates_atual):
            nome = entrada['TYPE']
            abates = entrada['ABATES']
            if nome == "JAVALI":
                WINDOW.draw_text(f"Javalis abatidos: {abates}", javali.x, javali.y + javali.height, size=25, color=(0,0,0))

            elif nome == "LENHADOR":
                WINDOW.draw_text(f"Lenhados abatidos: {abates}", lenhador.x - lenhador.width, lenhador.y + lenhador.height , size=25, color=(0,0,0))
                

            elif nome == "CACADOR":
                WINDOW.draw_text(f"Caçadores abatidos: {abates}", cacador.x, cacador.y + cacador.height, size=25, color=(0,0,0))


    if KEYBOARD.key_pressed("ESC"):
        globals.current_state = "MENU"
    
    WINDOW.update()