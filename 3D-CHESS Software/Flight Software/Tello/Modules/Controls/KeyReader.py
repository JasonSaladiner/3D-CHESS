import pygame as pg

def init():
    pg.init()
    win = pg.display.set_mode((400,400))


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
