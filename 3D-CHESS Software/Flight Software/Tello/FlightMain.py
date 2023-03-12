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
    #tello_C = TFS(cfg.telloIP_C,emControl = True)
    #tello_C.threadSetup()
    # OFF IN SAN FRAN, ADJUSTING FOR NO ROUTER ACCESS
    tello_C = TFS('192.168.10.1', emControl = True)

<<<<<<< Updated upstream
=======
    tello_C = Tello(cfg.telloIP_C)
    tello_C.connect()
    # DIDN'T MERGE YET, SO WILL DISAPPEAR AND HAVE THREADING FUNCTION IN TFS?
    mc = threading.Thread(target=mc.EngageMC, daemon=False, args=(tello_C, ))
    ft =threading.Thread(target=lv.startVideo, daemon=False, args=(tello_C, 'FT', True))
    ft.start()
    sleep(10)
    mc.start()
>>>>>>> Stashed changes


   