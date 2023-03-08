"""
This program serves as the main flight module
From here, all other flight modules will be controlled in order to achieve 3D-CHESS conops
"""



import ipaddress
import logging  #For changing the tello outputs
from djitellopy import Tello   #Tello 
from Modules import TelloFlightSoftware as TFS
import threading    #For multithreading
import cv2

import Modules._config_ as cfg  #Shared variables 

import Modules.Controls.ManualControl as mc         #Manual Control of the drone
import Modules.Controls.ComputerControl as cc       #Computer Aided drone control
from Modules.Location import IMU,Mapping            #Location services

from time import sleep


#Entrance
if __name__ == "__main__":
    tello_B = TFS(cfg.telloIP_B)
    #tello_B = TFS(Tello.TELLO_IP)
    tello_B.threadSetup()


              ###Make sure to check the flight area dimensions against the expected flight (include margin)###

    
    #Code to test the line. Make sure to turn on the drone facing 'forward' and then turn the drone accordingly (opposite of desired test direction e.g. 'r' move the drone right)
    #cc.lineTest(tello_B,'f')
    #cc.lineTest(tello_B,'r')
    #cc.lineTest(tello_B,'b')
    #cc.lineTest(tello_B,'l')

    tello_B.takeoff()
    sleep(4)
    tello_B.move_forward(28,'in')
    print(tello_B.commandVector)
    tello_B.land()
    #Code to test waypoints
    #cc.move_to_waypoints(tello_B,cc.xLineWaypoints)
    #cc.move_to_waypoints(tello_B,cc.simpleSquarePoints)
    #cc.move_to_waypoints(tello_B,cc.simpleDiamondPoints)
    
    
    
    #Start manual control
    #mc.EngageMC(tello_B)
    