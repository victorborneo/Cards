import os
import json
from random import randint

import pygame as pg

import common
from handlers import linker
from classes.selected import Selected
from classes.deck import Deck
from classes.text import Text


def update():
    common.window.fill(common.settings["BG_COLOR"])

    for obj in common.objs:
        obj.update()
        obj.draw()

    for text in common.texts:
        text.draw()

    pg.display.flip()


def set_common():
    common.selected = Selected()
    common.deck = Deck(common.settings["WIDTH"] // 2, common.settings["HEIGHT"] // 2, randint(1, 5))
    common.objs.append(common.deck)
    common.texts.append(
        Text(
            font_dir=common.settings["FONT"],
            size=round(common.settings["WIDTH"] * 0.025),
            text="Press R",
            color=(200, 200, 200),
            pos=(common.settings["WIDTH"] * 0.01, 0)
        )
    )


def create_settings():
    default = {
        "GAMENAME": "Cards",
        "ICONDIR": "./icon.ico",
        "FPS": 120,
        "WIDTH": 800,
        "HEIGHT": 600,
        "SCALE": 0.25,
        "BG_COLOR": [
            120,
            120,
            120
        ],
        "BGM": "./audio/bgm.wav",
        "BGM_VOLUME": 0.3,
        "SFX_VOLUME": 0.5,
        "FONT": "./fonts/8-BIT WONDER.TTF",
        "CARD_MOMENTUM_KEEP": 0.9,
        "CARD_OVERSHOOT": 0.8,
        "CARD_ACCEL": 75,
        "CARD_TURN_RATE": 10,
        "CARD_MAX_ANGLE": 60
        }

    with open("./settings.json", mode="w") as f:
        json.dump(default, f, indent=4)


def load_settings():
    if not os.path.exists("./settings.json"):
        create_settings()

    with open("./settings.json", mode="r") as f:
        return json.load(f)


def run():
    pg.init()
    pg.mixer.init()
    pg.font.init()
    common.init()

    common.settings = load_settings()

    clock = pg.time.Clock()
    common.window = pg.display.set_mode((common.settings["WIDTH"], common.settings["HEIGHT"]))
    pg.display.set_caption(common.settings["GAMENAME"])

    pg.mixer.music.set_volume(common.settings["BGM_VOLUME"])

    pg.mixer.music.load(common.settings["BGM"])
    pg.mixer.music.play(-1)

    set_common()

    if common.settings["ICONDIR"] is not None:
        pg.display.set_icon(pg.image.load(common.settings["ICONDIR"]))

    while True:
        common.dt = clock.tick(common.settings["FPS"]) / 1000

        for evt in pg.event.get():
            handler = linker.get(evt.type)
            if handler is not None:
                handler(evt)

        update()
 

if __name__ == "__main__":
    run()
