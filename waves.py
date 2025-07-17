"""
Esse módulo tem duas funções:
    -A auto_wave, que na verdade nada mais é que uma geração aleatória de inimigos de forma lenta que fica
    rodando constantemente durante o jogo

    -A wave_gen, que gera uma wave de inimigos de uma vez só, podendo ser um tipo específico de inimigos ou
    não
"""

import random
import pygame
import enemies
from player import player

WAVE_COOLDOWN = 2000 # ~~ 2 seg
last_wave = 0

def auto_wave(cam_offset):
    global WAVE_COOLDOWN, last_wave

    if pygame.time.get_ticks() - last_wave > WAVE_COOLDOWN:
        n = random.randint(1*player["LEVEL"] + 1,2*player["LEVEL"] + 1)

        for _ in range(n):
            enemies.spawn(random.choice(["JAVALI", "LENHADOR", "CACADOR"]), cam_offset)

        last_wave = pygame.time.get_ticks()

def reset():
    global last_wave
    last_wave = 0