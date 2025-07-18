"""
Esse módulo tem duas funções:
    -A auto_wave, que na verdade nada mais é que uma geração aleatória de inimigos de forma lenta que fica
    rodando constantemente durante o jogo

    -A wave_gen, que gera uma wave de inimigos de uma vez só, podendo ser um tipo específico de inimigos ou
    não
"""

import random
import enemies
from player import player

WAVE_COOLDOWN = 2.0 # 2 Segundos
wave_timer = 0.0

def auto_wave(cam_offset, delta_t):
    global WAVE_COOLDOWN, wave_timer

    wave_timer += delta_t

    if wave_timer >= WAVE_COOLDOWN:
        wave_timer = 0.0

        n = None
        if player["LEVEL"] == 0: # Level 0 (1-2 inimigos)
            n = random.randint(1, 2)
        elif player["LEVEL"] == 1: # Level 1 (2-3 inimigos)
            n = random.randint(2,3)
        else: # >= Level 2 (2-4 inimigos)
            n = random.randint(2,4) 

        for _ in range(n):
            enemies.spawn(random.choice(["JAVALI", "LENHADOR", "CACADOR"]), cam_offset)

def reset():
    global wave_timer
    wave_timer = 0.0