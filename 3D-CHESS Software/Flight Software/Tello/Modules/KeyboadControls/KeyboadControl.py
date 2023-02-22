import KeyboardReader as kr
from djitellopy import Tello
from time import sleep

tello = Tello()
tello.connect()


kr.init()

def move():
    v = 50 #cm/s
    y,x,z,yaw = 0,0,0,0
    if kr.getKey("a"):
        y=-v
    elif kr.getKey("d"):
        y=v
    if kr.getKey("w"):
        x=v
    elif kr.getKey("s"):
        x=-v
    if kr.getKey("SPACE"):
        z=v
    elif kr.getKey("LSHIFT"):
        z=-v
    if kr.getKey("q"):
        yaw=-v
    elif kr.getKey("e"):
        yaw=v
    elif kr.getKey("ESCAPE"):
        tello.land()

    return [y,x,z,yaw]

tello.takeoff()

while True:
    vals = move()
    tello.send_rc_control(vals[0],vals[1],vals[2],vals[3])
    sleep(.2)