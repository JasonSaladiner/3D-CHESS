"""
ManualControl.py module gives the user the capability to control the drone using simple WASDQE commands

Required Imports:
KeyReader.py
    pygame
djitellopy
time
"""

import Modules.Controls.KeyReader as kr
#from djitellopy import Tello
from time import sleep
from math import floor

from Modules.Location import IMU
import Modules._config_ as cfg
from Modules.Controls.ComputerControl import go_nXYZ_direct,go_nXYZ_P

#global tello variable
global tello

velocity = 50   #cm/s


def _WASDInput_():
    global tello
    global velocity
    y,x,z,yaw = 0,0,0,0
    if kr.getKey("a"):
        y=-velocity
    elif kr.getKey("d"):
        y=velocity
    if kr.getKey("w"):
        x=velocity
    elif kr.getKey("s"):
        x=-velocity
    if kr.getKey("SPACE"):
        if tello.is_flying:
            z=velocity
        else:
            print("Takeoff Inititated")
            try:
                tello.takeoff()
                print("Take-off Successful")
            except:
                print("Issue with takeoff")
    elif kr.getKey("LCTRL"):
        z=-velocity
    if kr.getKey("q"):
        yaw=-2*velocity
    elif kr.getKey("e"):
        yaw=2*velocity
    elif kr.getKey("ESCAPE"):
        tello.land()
    elif kr.getKey("m"):
        print(cfg.xPos,cfg.yPos,cfg.zPos,tello.get_yaw())
        print(tello.commandVector)
    elif kr.getKey("g"):
        #Potentially temporary for testing
        cfg.emOps = True
        print("Current Location:")
        print(cfg.xPos,cfg.yPos,cfg.zPos,tello.get_yaw())
        a = int(input("X position:"))
        b= int(input("Y position:"))
        #c = int(input("Z position:"))
        print("goto starting")
        go_nXYZ_direct(tello,a,b)
        print(cfg.xPos,cfg.yPos,cfg.zPos,tello.get_yaw())
        print("goto finished")
        tello.land()
        #cfg.emOps=False
    elif kr.getKey("h"):
        ##Potentially tempory for testing
        cfg.emOps = True
        print("Current Location:")
        print(cfg.xPos,cfg.yPos,cfg.zPos,tello.get_yaw())
        a = int(input("X position:"))
        b= int(input("Y position:"))
        #c = int(input("Z position:"))
        print("goto starting")
        go_nXYZ_P(tello,a,b,cfg.zPos)
        print(cfg.xPos,cfg.yPos,cfg.zPos,tello.get_yaw())
        print("goto finished")
        tello.land()
        #cfg.emOps=False
    elif kr.getKey("DELETE"):
        cfg.emOps=True
        tello.emergency()
    elif kr.getKey("UP"):
        velocity += 10
    elif kr.getKey("DOWN"): 
        if velocity > 10:
            velocity -= 10
    return [y,x,z,yaw]

def _arrowInput_():
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
keybinds = {"a":_arrowInput_,
            "b":_WASDInput_}




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
    choice = init()
    global tello
    tello = ConnectedTello


    dt = .2
    while not cfg.emOps:

        vals = keybinds[choice]()
        
        ConnectedTello.send_rc_control(vals[0],vals[1],vals[2],vals[3])
        sleep(dt)

def EmergencyControls(ConnectedTello):
    kr.init()
    while True:
        if kr.getKey('ESCAPE'):
            ConnectedTello.land()
        elif kr.getKey('DELETE'):
            ConnectedTello.emergency()
        else:
            pass