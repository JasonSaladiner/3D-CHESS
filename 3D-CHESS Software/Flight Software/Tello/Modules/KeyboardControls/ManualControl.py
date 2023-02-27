"""
ManualControl.py module gives the user the capabilty to control the drone using simple WASDQE commands

Required Imports:
KeyReader.py
    pygame
djitellopy
time
"""

import Modules.KeyboardControls.KeyReader as kr
#from djitellopy import Tello
from time import sleep
from Modules.Location import IMU

#global tello variable
global tello

def WASDInput():
    global tello
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
        if tello.is_flying:
            z=v
        else:
            tello.takeoff()
    elif kr.getKey("LSHIFT"):
        z=-v
    if kr.getKey("q"):
        yaw=-2*v
    elif kr.getKey("e"):
        yaw=2*v
    elif kr.getKey("ESCAPE"):
        tello.land()

    return [y,x,z,yaw]

def arrowInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    spd = 50
    global tello
    if kr.getKey("LEFT"): lr = -spd
    elif kr.getKey("RIGHT"): lr = spd
    if kr.getKey("UP"): fb = spd
    elif kr.getKey("DOWN"): fb = -spd
    if kr.getKey("w"): ud = spd
    elif kr.getKey("s"): ud = -spd
    if kr.getKey("a"): yv = -spd
    elif kr.getKey("d"): yv = spd

    if kr.getKey("e"): tello.takeoff()
    if kr.getKey("q"): tello.land()

    return [lr, fb, ud, yv]

#Dictionary of all possible keybinds
keybinds = {"a":arrowInput,
            "b":WASDInput}




#init function
def init():
    
    while True:
        choice = input("Which keyboard input Arrows (a) or WASD (b): ").lower()
        if choice == "a" or choice == "b":
            break
        else:
            print("Please input either a or b")

    kr.init()
    return choice

def EngageMC(ConnectedTello):
    """
    EngageMC will begin searching for keyboard inputs to control a connected tello
    Tello ConnectedTello representing the connected tello
    """
    #tello = ConnectedTello
    choice = init()
    global tello
    tello = ConnectedTello
    #rps = IMU.location(tello)
    while True:
        try:
            vals = keybinds[choice]()
        except:
            pass
        dt = .2
        ConnectedTello.send_rc_control(vals[0],vals[1],vals[2],vals[3])
        #rps.update([tello.get_speed_x(),tello.get_speed_y(),tello.get_speed_z()],dt)
        #print(rps.cart)
        sleep(dt)

