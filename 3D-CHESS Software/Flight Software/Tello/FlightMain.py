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
import Modules.ImageProcessing.LiveVideo as lv
import Modules.Controls.ManualControl as mc         #Manual Control of the drone
import Modules.Controls.ComputerControl as cc       #Computer Aided drone control
from Modules.Location import IMU,Mapping        
#Location services

from time import sleep



#Entrance
if __name__ == "__main__":
    #tello_C = Tello(cfg.telloIP_C)
    tello_C = Tello('192.168.10.1') 
    tello_C.connect()
    mc = threading.Thread(target=mc.EngageMC, daemon=False, args=(tello_C, ))
    lv =threading.Thread(target=lv.startVideo, daemon=False, args=(tello_C, 'tello_C', 'FT', False))
    lv.start()
    sleep(10)
    mc.start()

   