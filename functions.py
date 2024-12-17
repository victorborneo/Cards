import pygame as pg
from pygame.locals import *

import common


def scale_sprite(img_dir):
    img = pg.image.load(img_dir).convert_alpha()

    c = common.settings["SCALE"] * common.settings["HEIGHT"] / img.get_height()

    return pg.transform.scale(
        img,
        (img.get_width() * c, img.get_height() * c)
    )
