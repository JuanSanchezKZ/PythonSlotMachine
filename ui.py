from player import Player
from settings import *
import pygame, random


class UI:
    def __init__(self, player):
        self.player = player
        self.display_surface = pygame.display.get_surface()
        try:
            self.font, self.bet_font = pygame.font.Font(
                UI_FONT, UI_FONT_SIZE
            ), pygame.font.Font(UI_FONT, UI_FONT_SIZE)
            self.win_font = pygame.font.Font(UI_FONT, WIN_FONT_SIZE)
        except:
            print("Error loading font!")
            print(f"Currently, the UI_FONT variable is set to {UI_FONT}")
            print("Does the file exist?")
            quit()
        self.win_text_angle = random.randint(-4, 4)

    def update(self):
        pygame.draw.rect(self.display_surface, "Black", pygame.Rect(0, 900, 1600, 100))
