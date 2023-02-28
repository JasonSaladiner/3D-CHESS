"""
This module hopes to integrate the IMU's X,Y,Z acceleartions to get position

"""
from time import sleep
import Modules._config_ as cfg
import numpy as np
from djitellopy.tello import Tello
from math import pi, sin,cos
def displacement(velocity,acceleration,time):
    """
    returns the change in position from initial velocity, constant acceleartion, over delta time
    """

    return velocity*time + .5*acceleration*time**2

class location:
    def update(self,V,dt):
        for i in range(0,3):
            self.cart[i] += self.vdisp(V[i],dt)



    def __init__(self,ConnectedTello):
        self.tello = ConnectedTello
        self.cart = [0,0,0]
        self.vdisp = lambda v,t: v*t


def init(ConnectedTello):
    tello = ConnectedTello
    #tello.connect()
    #x,y,z = 0,0,0
    vdisp = lambda v,t: v*t

    
    dt = 0.05 
    while True:
        try:
            vx = -tello.get_speed_x()
            vy = -tello.get_speed_y()
            vz = -tello.get_speed_z()
            yaw = -tello.get_yaw()*pi/180
            #s
            bV = np.array([vdisp(vx,dt),vdisp(vy,dt),vdisp(vz,dt)])
            orientationMatrix = np.array([cos(yaw),sin(yaw),0,-sin(yaw),cos(yaw),0,0,0,1]).reshape((3,3))
            
            absolute = np.matmul(orientationMatrix,bV)
            #print(absolute)
            cfg.xPos += absolute[0]
            cfg.yPos += absolute[1]
            cfg.zPos += absolute[2]
        except:
            pass
        #print(x,y,z)
        sleep(dt)