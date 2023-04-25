import pygame as pg

def init():
    x,y = 975,375
    import os
    os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (x,y)

    pg.init()
    win = pg.display.set_mode((650,155))


def getKey(keyName):
    ans = False
    for eve in pg.event.get(): pass

    keyIn = pg.key.get_pressed()
    myKey = getattr(pg,'K_{}'.format(keyName))

    if keyIn[myKey]:
        ans = True
    pg.display.update()

    return ans




if __name__ == "__main__":
    init()
