import Modules._config_ as cfg
from time import sleep
import numpy as np
from math import pi, sin, cos, atan2, sqrt, floor


def directRTH(ConnectedTello):
    yaw = ConnectedTello.get_yaw()*pi/180

    orientationMatrix = np.array([cos(yaw),sin(yaw),0,-sin(yaw),cos(yaw),0,0,0,1]).reshape((3,3))
    absoluteCart = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    
    relativeCart = np.matmul(np.linalg.inv(orientationMatrix),absoluteCart)

    rotationAngle = atan2(relativeCart[1],relativeCart[0])
    distance = sqrt(relativeCart[0]**2 + relativeCart[1]**2)

    ConnectedTello.rotate_counter_clockwise(floor(rotationAngle*180/pi))

    velocity = 30 #cm/s
    time = distance*10/velocity

    ConnectedTello.send_rc_control(0,velocity,0,0)
    sleep(time)
    ConnectedTello.send_rc_control(0,0,0,0)

#Entrance
#if __name__ == "__main__":
    
