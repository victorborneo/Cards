from pygame.locals import *

import common


def motion_handler(evt):
    return


def click_handler(evt):
    for obj in common.objs[::-1]:
        if obj.clicked(evt.pos):
            obj.on_click(evt.button)
            break


def release_handler(evt):
    common.selected.clear()


def keyboard_handler(evt):
    if evt.key == K_r:
        common.deck.start_shuffle()
    elif evt.key == K_ESCAPE:
        quit()


def quit_handler(evt):
    quit()


linker = {
    QUIT: quit_handler,
    MOUSEMOTION: motion_handler,
    MOUSEBUTTONDOWN: click_handler,
    MOUSEBUTTONUP: release_handler,
    KEYDOWN: keyboard_handler
}
