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

WAVE_COOLDOWN = 4000 # ~~ 4 seg
last_wave = 0

def auto_wave():
    global WAVE_COOLDOWN, last_wave

    if pygame.time.get_ticks() - last_wave > WAVE_COOLDOWN:
        # Depois fazer o número de inimigos possíveis aumentar conforme o lvl do player(ou o tempo passado?)
        n = random.randint(1,3)

        for _ in range(n):
            # Depois fazer O Javali só spawnar a partir de x minutos, o mesmo para o caçador, para a dificuldade
            # ir aumentando conforme o tempo
            #enemies.spawn(random.choice(["JAVALI", "LENHADOR", "CACADOR"]))
            enemies.spawn("LENHADOR")

        last_wave = pygame.time.get_ticks()

def reset():
    global last_wave
    last_wave = 0