"""
This module hopes to integrate the IMU's X,Y,Z acceleartions to get position

"""
from time import sleep

from djitellopy.tello import Tello
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


def init():
    tello = Tello
    tello.connect()
    x,y,z = 0,0,0

    vdisp = lambda v,t: v*t
    while True:
        try:
            vx = tello.get_speed_x()
            vy = tello.get_speed_y()
            vz = tello.get_speed_z()
        
            dt = .2 #s

            x += vdisp(vx,dt)
            y += vdisp(vy,dt)
            z += vdisp(vz,dt)
        except:
            pass
        print(x,y,z)
        sleep(dt)