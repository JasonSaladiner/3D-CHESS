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
#from Modules.Controls.ComputerControl import go_nXYZ_direct,go_nXYZ_P

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
        print(tello.position)

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

    # just for fun
    if kr.getKey('p'): tello.flip('r')

    return [lr, fb, ud, yv]

#Dictionary of all possible keybinds
keybinds = {"a":_arrowInput_,
            "b":_WASDInput_}




#init function
def init():
    
    while True:
        #choice = input("Which keyboard input Arrows (a) or WASD (b): ").lower()
        choice = "b"
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
    while True:

        vals = keybinds[choice]()
        
        ConnectedTello.send_rc_control(vals[0],vals[1],vals[2],vals[3])
        sleep(dt)

def EmergencyControls(Tellos):
    kr.init()
    import os
    while True:
        if kr.getKey('ESCAPE'):
            for t in Tellos:
                try:
                    t.land()
                except:
                    pass
            cfg.emerg = True
             #os._exit()
        elif kr.getKey('DELETE'):
            for t in Tellos:
                try:
                    t.emergency()
                except:
                    pass
            cfg.emerg = True    
            #os._exit()
        elif kr.getKey('1'):
            try:
                Tellos[0].land()
                #cfg.emerg = True
            except:
                pass
        elif kr.getKey('2'):
            try:
                Tellos[1].land()
                #cfg.emerg = True
            except:
                pass
        elif kr.getKey('3'):
            try:
                Tellos[2].land()
                #cfg.emerg = True
            except:
                pass
        elif kr.getKey('9'):
            try:
                Tellos[0].emergency()
                #cfg.emerg = True
            except:
                pass
        elif kr.getKey('8'):
            try:
                Tellos[1].emergency()
                #cfg.emerg = True
            except:
                pass
        elif kr.getKey('7'):
            try:
                Tellos[2].emergency()
                #cfg.emerg = True
            except:
                pass
        else:
            pass