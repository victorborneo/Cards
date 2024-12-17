from random import randint

import pygame as pg

import common
from consts import *
from handlers import linker
from classes.selected import Selected
from classes.deck import Deck
from classes.text import Text


def update():
    common.window.fill(BG_COLOR)

    for obj in common.objs:
        obj.update()
        obj.draw()

    for text in common.texts:
        text.draw()

    pg.display.flip()


def set_common():
    common.selected = Selected()
    common.deck = Deck(WIDTH // 2, HEIGHT // 2, randint(1, 5))
    common.objs.append(common.deck)
    common.texts.append(
        Text(
            font_dir=FONT,
            size=round(WIDTH * 0.025),
            text="Press R",
            color=(200, 200, 200),
            pos=(WIDTH * 0.01, 0)
        )
    )

def run():
    pg.init()
    pg.mixer.init()
    pg.font.init()
    common.init()

    clock = pg.time.Clock()
    common.window = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption(GAMENAME)

    pg.mixer.music.set_volume(BGM_VOLUME)

    pg.mixer.music.load(BGM)
    pg.mixer.music.play(-1)

    set_common()

    if ICONDIR is not None:
        pg.display.set_icon(pg.image.load(ICONDIR))

    while True:
        common.dt = clock.tick(FPS) / 1000

        for evt in pg.event.get():
            handler = linker.get(evt.type)
            if handler is not None:
                handler(evt)

        update()
 

if __name__ == "__main__":
    run()
