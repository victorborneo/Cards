import pygame as pg
from pygame.locals import *

from consts import SCALE
from consts import HEIGHT


def scale_sprite(img_dir):
    img = pg.image.load(img_dir).convert_alpha()

    c = SCALE * HEIGHT / img.get_height()

    return pg.transform.scale(
        img,
        (img.get_width() * c, img.get_height() * c)
    )
