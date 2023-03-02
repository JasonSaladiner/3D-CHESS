import Modules._config_ as cfg
from time import sleep
import numpy as np
from math import pi, sin, cos, atan2, sqrt, floor
from djitellopy import Tello

def directRTH(ConnectedTello):
    """
    WIP and may be deleted in favor of go_nXYZ_direct
    """
    yaw = ConnectedTello.get_yaw()*pi/180

    orientationMatrix = np.array([cos(yaw),sin(yaw),0,-sin(yaw),cos(yaw),0,0,0,1]).reshape((3,3))
    absoluteCart = np.array([cfg.xPos,cfg.yPos,cfg.zPos]).reshape((3,1))
    
    relativeCart = np.matmul(np.linalg.inv(orientationMatrix),absoluteCart)

    rotationAngle = atan2(relativeCart[1],relativeCart[0])
    distance = sqrt(relativeCart[0]**2 + relativeCart[1]**2)

    ConnectedTello.rotate_counter_clockwise(floor(rotationAngle*180/pi))

    velocity = 30 #cm/s
    time = distance*10/velocity

    ConnectedTello.send_rc_control(0,velocity,0,0)
    sleep(time)
    ConnectedTello.send_rc_control(0,0,0,0)



def go_nXYZ_direct(ConnectedTello: Tello,X: int,Y: int,Z:int=floor(cfg.zPos), velocity = 30):
    """
    go_nXYZ_direct draws a straight line from ConnectedTello to the (X,Y,Z) location, rotates tello towards it, and drives straight towards it at velocity
    Inputs:
        ConnectedTello:Tello = the connected tello
        X:int = integer of desired x position in inertial coordinates
        Y:int = integer of desired y position in inertial coordinates  
        Z:int = integer of desired z position in inertial coordinates
        velocity = integer of velocity to fly at (cm/s)
    :NOTES:
        X,Y,Z mark locations in decimeters
        has a predicted accuracy of around 2 decimeters
    """
    Z = floor(Z)
    
    ####This block of code may be able to be deleted####
    #get current yaw
    #yaw = ConnectedTello.get_yaw()*pi/180

    #change absolute to relative 
    #orientationMatrix = np.array([cos(yaw),sin(yaw),0,-sin(yaw),cos(yaw),0,0,0,1]).reshape((3,3))
    #absoluteCart = np.array([cfg.xPos,cfg.yPos,cfg.zPos]).reshape((3,1))
    
    #relativeCart = np.matmul(np.linalg.inv(orientationMatrix),absoluteCart)
    ####

    #Get relative position vector
    relativePositionVector = np.array([X,Y,Z]) - np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    print("relativePosition", relativePositionVector)

    #Find necessary delta Yaw and ground distance
    rotationAngle = floor(atan2(relativePositionVector[1],relativePositionVector[0])*180/pi)
    distance = sqrt(relativePositionVector[0]**2 + relativePositionVector[1]**2)
    print(rotationAngle,distance)
    
    #Apply rotation
    ConnectedTello.rotate_counter_clockwise(rotationAngle)

    #Find time to complete movement and the speed to go up/down
    time = distance*10/velocity
    heightVelocity = relativePositionVector[2]*10/time

    #Fly the distance
    ConnectedTello.send_rc_control(0,floor(velocity),floor(heightVelocity),0)
    sleep(time)
    #Stop
    ConnectedTello.send_rc_control(0,0,0,0)
    