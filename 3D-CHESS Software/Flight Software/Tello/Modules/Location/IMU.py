"""
This module hopes to integrate the IMU's X,Y,Z acceleartions to get position

"""
from time import sleep
import Modules._config_ as cfg
import numpy as np
#from djitellopy.tello import Tello
from math import pi, sin,cos




fudgeFactor = 1       #a potential solve for the distance issue

def init(ConnectedTello):
    tello = ConnectedTello
    vdisp = lambda v,t: v*t*fudgeFactor

    
    dt = 0.05   #time step
    while True:
        try:
            #Get instant velocites
            vx = -tello.get_speed_x()
            vy = -tello.get_speed_y()
            vz = -tello.get_speed_z()
            
            #position vector
            position = [vdisp(vx,dt),vdisp(vy,dt),vdisp(vz,dt)]

            #Update IMUVector
            ConnectedTello.IMUVector += position

            #update config file
            #cfg.xPos += position[0]*cfg.dmToin
            #cfg.yPos += position[1]*cfg.dmToin
            #cfg.zPos += position[2]*cfg.dmToin
        except:
            pass

        #wait for next time step
        sleep(dt)