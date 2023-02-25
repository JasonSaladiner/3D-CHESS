from djitellopy import Tello
import KeyPressModule as kp
from time import sleep

kp.init()
me = Tello()
me.connect()
print(me.get_battery())


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    spd = 50

    if kp.getKey("LEFT"): lr = -spd
    elif kp.getKey("RIGHT"): lr = spd
    if kp.getKey("UP"): fb = spd
    elif kp.getKey("DOWN"): fb = -spd
    if kp.getKey("w"): ud = spd
    elif kp.getKey("s"): ud = -spd
    if kp.getKey("a"): yv = -spd
    elif kp.getKey("d"): yv = spd

    if kp.getKey("e"): me.takeoff()
    if kp.getKey("q"): me.land()

    return [lr, fb, ud, yv]


while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.5)
