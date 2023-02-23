"""
ManualControl.py module gives the user the capabilty to control the drone using simple WASDQE commands
"""

import KeyReader as kr
from djitellopy import Tello
from time import sleep

#def init():
tello = Tello()
tello.connect()

kr.init()
    
    #global vel
    #global yb
    #global xb
    #global zb
    #global yawb
    #Keybinds dictionary
def keybinds(key):
   return {
        "w": [0,vel,0,0],
        "a": [-vel,0,0,0],
        "s": [0,-vel,0,0],
        "d": [vel,0,0,0],
        "q": [0,0,-vel,0],
        "e": [0,0,vel,0],
        "SPACE": [0,0,0,vel],
        #"LSHIFT": ,
        "LCTRL": [0,0,0,vel]
        #"ESCAPE":,
        #"BACKSPACE": ,
        }.get(key, "error")()



def controlInput():
    
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
        yaw=-v
    elif kr.getKey("e"):
        yaw=v
    elif kr.getKey("ESCAPE"):
        tello.land()

    return [y,x,z,yaw]


#if __name__ == "__main__":
vel = 30
yb = 0
xb = 0
zb = 0
yawb = 0


while True:
    try:
        vals = controlInput()
    except:
        pass
    tello.send_rc_control(vals[0],vals[1],vals[2],vals[3])
    sleep(.2)