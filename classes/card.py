import math

from pygame import mixer
from pygame.transform import scale
from pygame.mouse import get_pos
from pygame.mouse import get_pressed

import common
from functions import scale_sprite
from classes.object import Object


class Card(Object):
    def __init__(self, x, y, rank, suit, back):
        self.x = x
        self.y = y
        self.rank = rank
        self.suit = suit
        self.back = back
        self.orientation = -1  # -1 = face down, 1 = face up
        self.sprite = scale_sprite(f"./sprites/{suit}_{rank}.png")
        self.back_sprite = scale_sprite(f"./sprites/back_{back}.png")
        self.width, self.height = self.sprite.get_size()
        self.accel = common.settings["CARD_ACCEL"]
        self.speed = 0
        self.max_speed = self.accel * 10

        self.dx = None
        self.dy = None
        
        self.turn = False
        self.max_turn = 1
        self.turning = self.max_turn
        self.turn_rate = -common.settings["CARD_TURN_RATE"]
        self.rotate = 1
        self.prev_x = None

        self.flip_sfx = mixer.Sound("./audio/flip.mp3")
        self.flip_sfx.set_volume(common.settings["SFX_VOLUME"])

    def turn_animation(self, sprite):
        self.turning += self.turn_rate * common.dt

        sprite = scale(
            sprite,
            (max(self.width * min(self.turning, self.max_turn) / self.max_turn, 0), self.height)
        )

        self.x += (self.width // 2) * abs(self.turn_rate / self.max_turn) * self.rotate * common.dt

        if self.turning <= 0:
            self.turning = 0
            self.orientation *= -1
            self.turn_rate *= -1
            self.rotate *= -1

        if self.turning >= self.max_turn:
            self.x = self.prev_x
            self.turning = self.max_turn
            self.turn = False
            self.turn_rate *= -1
            self.rotate *= -1

        return sprite

    def draw(self):
        if self.orientation == 1:
            sprite = self.sprite
        else:
            sprite = self.back_sprite

        if self.turn:
            sprite = self.turn_animation(sprite)

        common.window.blit(sprite, (self.x, self.y))

    def clicked(self, click_pos):
        x, y = click_pos

        if self.x <= x <= self.x + self.width and \
                self.y <= y <= self.y + self.height:
            return True
        
        return False

    def on_click(self, button):
        common.objs.remove(self)
        common.objs.append(self)

        if button == 1:
            common.selected.set_selected(self)
        elif button == 3 and not self.turn:
            self.flip_sfx.play()
            self.turn = True

    def update(self):
        self.prev_x = self.x
        if self.speed == 0 and common.selected.get_selected() is not self:
            return

        mouse_x, mouse_y = get_pos()
        center_x, center_y = self.x + self.width // 2, self.y + self.height // 2

        if not (0 <= center_x <= common.settings["WIDTH"] and 0 <= center_y <= common.settings["HEIGHT"]):
            mouse_x, mouse_y = common.settings["WIDTH"] // 2, common.settings["HEIGHT"] // 2
            self.dx = mouse_x - center_x
            self.dy = mouse_y - center_y
            if common.selected.get_selected() is self:
                common.selected.clear()

        if get_pressed()[0] and common.selected.get_selected() is self and not self.turn:
            self.dx = mouse_x - center_x
            self.dy = mouse_y - center_y

        dist = math.sqrt(self.dx * self.dx + self.dy * self.dy)
        
        if dist > 0:
            dx = self.dx / dist
            dy = self.dy / dist

        if dist < 15:
            self.speed = math.floor(self.speed * 0.5)
        elif get_pressed()[0] and common.selected.get_selected() is self:
            if self.speed < self.max_speed:
                self.speed += self.accel
        else:
            self.speed = math.floor(self.speed * common.settings["CARD_MOMENTUM_KEEP"])

        self.x += dx * common.dt * self.speed
        self.y += dy * common.dt * self.speed
