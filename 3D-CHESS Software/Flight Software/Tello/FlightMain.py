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
import Modules.ImageProcessing.LiveVideo as lv
from time import sleep



#Entrance
if __name__ == "__main__":
    #tello_B = TFS(cfg.telloIP_B)
    
    #tello_B.threadSetup()
    #tello_B.runMission(mc.EngageMC,tello_B)
    #tello_B.runMission(cc.move_to_waypoints,tello_B,cc.sampleWaypoints)

    #tello_C = Tello()
    #tello_C.connect()
    #tello_C.connect_to_wifi('tellonet','selvachess')

    tello_C = Tello(cfg.telloIP_C)
    tello_C.connect()
    lv.startVideo(tello_C)

    #Start manual control
    #mc.EngageMC(tello_B)
    