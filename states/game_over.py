import pygame
import globals

def game_over():
    WINDOW = globals.WINDOW
    KEYBOARD = globals.KEYBOARD

    WINDOW.set_background_color([50,10,10])

    text_surface = pygame.font.SysFont('Tahoma', 50).render("GAME OVER", True, (255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.centerx = WINDOW.width // 2
    text_rect.centery = WINDOW.height // 2
    WINDOW.draw_text("GAME OVER", text_rect.x, text_rect.y, size = 50, color = (255,255,255), font_name = 'Tahoma', bold = True, italic = False) 

    if KEYBOARD.key_pressed("ESC"):
        globals.current_state = "MAIN_MENU"