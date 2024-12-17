from pygame import font

import common
from classes.object import Object


class Text(Object):
    def __init__(self, font_dir, size, text, color, pos, a_aliasing=True):
        self.pos = pos
        self.font = font.Font(font_dir, size)
        self.txt = self.font.render(text, a_aliasing, color)

    def draw(self):
        common.window.blit(self.txt, self.pos)

    def update(self):
        return

    def clicked(self, pos):
        return

    def on_click(self, button):
        return
