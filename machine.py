from player import Player
from reel import *
from settings import *
from ui import UI
from wins import *
import pygame
from PIL import Image, ImageFilter


class Machine:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.reel_index = 0
        self.reel_list = {}
        self.can_toggle = True
        self.spinning = False
        self.can_animate = False
        self.win_animation_ongoing = False

        # Results
        self.prev_result = {0: None, 1: None, 2: None}

        self.spawn_reels()
        self.currPlayer = Player()
        self.ui = UI(self.currPlayer)

        # Import sounds
        # self.spin_sound = pygame.mixer.Sound('audio/spinclip.mp3')
        # self.spin_sound.set_volume(0.15)
        # self.win_three = pygame.mixer.Sound('audio/winthree.wav')
        # self.win_three.set_volume(0.6)
        # self.win_four = pygame.mixer.Sound('audio/winfour.wav')
        # self.win_four.set_volume(0.7)
        # self.win_five = pygame.mixer.Sound('audio/winfive.wav')
        # self.win_five.set_volume(0.8)

    def cooldowns(self):
        # Only lets player spin if all reels are NOT spinning

        for reel in self.reel_list:
            if self.reel_list[reel].reel_is_spinning:
                self.can_toggle = False
                self.spinning = True

        if (
            not self.can_toggle
            and [
                self.reel_list[reel].reel_is_spinning for reel in self.reel_list
            ].count(False)
            == 2
        ):
            self.can_toggle = True

            self.win_animation_ongoing = True

    def input(self):  # NO ES EL PROBLEMA
        keys = pygame.key.get_pressed()

        # Checks for space key, ability to toggle spin, and balance to cover bet size
        if keys[pygame.K_SPACE] and self.can_toggle:
            self.toggle_spinning()
            self.spin_time = pygame.time.get_ticks()

    def draw_reels(self, delta_time):
        for reel in self.reel_list:
            self.reel_list[reel].animate(delta_time)

    def spawn_reels(self):  # NO ES PROBLEMA
        if not self.reel_list:
            x_topleft, y_topleft = 10, -300
        while self.reel_index < 2:
            if self.reel_index > 0:
                x_topleft, y_topleft = x_topleft + (300 + X_OFFSET), y_topleft
            self.reel_list[self.reel_index] = Reel(
                (x_topleft, y_topleft)
            )  # Need to create reel class
            self.reel_index += 1

    def toggle_spinning(self):
        if self.can_toggle:
            self.spin_time = pygame.time.get_ticks()
            self.spinning = not self.spinning
            self.can_toggle = False
            for reel in self.reel_list:
                self.reel_list[reel].start_spin(int(reel) * 200)
                # self.spin_sound.play()
                self.win_animation_ongoing = False

    def win_animation(self):
        if self.win_animation_ongoing:
            for reel in self.reel_list:
                symbol_sprites = self.reel_list[reel].symbol_list.sprites()
                num_symbols = len(symbol_sprites)

                for i in range(num_symbols):
                    symbol = symbol_sprites[i]
                    if i in {0, 1, num_symbols - 2, num_symbols - 1}:
                        # Apply blur to the first and last symbols

                        # Convert Pygame Surface to Pillow Image
                        pillow_image = Image.frombytes(
                            "RGB",
                            symbol.image.get_size(),
                            pygame.image.tostring(symbol.image, "RGB"),
                        )
                        # Apply blur
                        blurred_pillow_image = pillow_image.filter(ImageFilter.BLUR)
                        # Convert Pillow Image back to Pygame Surface
                        symbol.image = pygame.image.fromstring(
                            blurred_pillow_image.tobytes(),
                            blurred_pillow_image.size,
                            "RGB",
                        )

    def update(self, delta_time):
        self.cooldowns()
        self.input()
        self.draw_reels(delta_time)
        for reel in self.reel_list:
            self.reel_list[reel].symbol_list.draw(self.display_surface)
            self.reel_list[reel].symbol_list.update()
        self.ui.update()
        self.win_animation()

        # Balance/payout debugger
        # debug_player_data = self.currPlayer.get_data()
        # machine_balance = "{:.2f}".format(self.machine_balance)
        # if self.currPlayer.last_payout:
        #     last_payout = "{:.2f}".format(self.currPlayer.last_payout)
        # else:
        #     last_payout = "N/A"
        # debug(f"Player balance: {debug_player_data['balance']} | Machine balance: {machine_balance} | Last payout: {last_payout}")
