import random

from pygame import mixer

import common
from classes.card import Card
from functions import scale_sprite
from classes.object import Object


class Deck(Object):
    def __init__(self, x, y, back):
        self.back = back
        self.back_sprite = scale_sprite(f"./sprites/back_{back}.png")
        self.width, self.height = self.back_sprite.get_size()
        self.x = x - self.width // 2
        self.y = y - self.height // 2
        self.deck = self.init_deck()
        
        self.is_shuffling = False
        self.shuffle_wait = False
        self.shuffle_wait_secs = 1
        self.dx = None

        self.draw_sfx = mixer.Sound("./audio/draw.mp3")
        self.shuffle_sfx = mixer.Sound("./audio/shuffle.mp3")
        self.draw_sfx.set_volume(common.settings["SFX_VOLUME"])
        self.shuffle_sfx.set_volume(common.settings["SFX_VOLUME"])

    def init_deck(self):
        deck = []
        suits = ("Diamonds", "Clubs", "Spades", "Hearts")
        ranks = (2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'ACE')

        c = 0
        for suit in suits:
            for rank in ranks:
                deck.append(
                    Card(
                        self.x + c, self.y - c,
                        rank, suit, self.back
                    )
                )
                c += common.settings["WIDTH"] / 4000

        deck.append(
            Card(
                self.x + c, self.y - c,
                "1", "Joker", self.back
            )
        )

        deck.append(
            Card(
                self.x + c, self.y - c,
                "2", "Joker", self.back
            )
        )

        self.size = len(deck)
        return deck

    def start_shuffle(self):
        self.is_shuffling = True

    def shuffle(self):
        self.deck = self.init_deck()
        random.shuffle(self.deck)

        c = 0
        for card in self.deck:
            card.x = self.x + c
            card.y = self.y - c
            c += common.settings["WIDTH"] / 4000

    def draw(self):
        for card in self.deck:
            card.draw()

    def update(self):
        if not self.is_shuffling:
            return

        if self.shuffle_wait:
            self.shuffle_wait_secs -= common.dt
            
            if self.shuffle_wait_secs > 0:
                return
            else:
                self.shuffle_wait_secs = 0
                self.shuffle_wait = False

        if self.shuffle_wait_secs == 0:
            self.dx = (common.settings["WIDTH"] // 2 - self.width // 2) - self.x
        else:
            self.dx = -common.settings["WIDTH"] - self.x

        self.x += common.dt * 5 * self.dx
        for card in self.deck[::-1]:
            card.x += common.dt * 5 * self.dx
        for card in common.objs[1:]:
            card.x += common.dt * 5 * self.dx

        if abs(self.dx) <= 1:
            self.dx = 0

            if self.shuffle_wait_secs == 1:
                self.shuffle_sfx.play()
                self.shuffle()
                self.shuffle_wait = True
                common.objs = [self]
            else:
                self.shuffle_wait_secs = 1
                self.is_shuffling = False

    def clicked(self, click_pos):
        if self.size == 0 or self.is_shuffling:
            return False

        x, y = click_pos

        if self.x + self.size * (common.settings["WIDTH"] / 4000) <= x <= self.x + self.width + self.size * (common.settings["WIDTH"] / 4000) and \
                self.y - self.size * (common.settings["WIDTH"] / 4000) <= y <= self.y + self.height - self.size * (common.settings["WIDTH"] / 4000):
            return True

        return False

    def on_click(self, button):
        if button != 1 and button != 3:
            return

        card = self.deck.pop()
        common.objs.append(card)
        self.size -= 1

        if button == 1:
            common.selected.set_selected(card)
            self.draw_sfx.play()
        elif button == 3:
            card.on_click(button)


