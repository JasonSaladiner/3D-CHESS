"""
This program serves as the main flight module
From here, all other flight modules will be controlled in order to achieve 3D-CHESS conops
"""



import ipaddress
import logging  #For changing the tello outputs
from djitellopy import Tello, TelloSwarm    #Tello 
import threading    #For multithreading
import Modules._config_ as cfg  #Shared variables 

import Modules.Controls.ManualControl as mc     #Manual Control of the drone
import Modules.Controls.ComputerControl as cc
from Modules.Location import IMU            #Location services

Tello.LOGGER.setLevel(logging.WARNING)      #Setting tello outpus to warning only




def _temp_():
    tello.takeoff()
    cfg.OutputAttitudePosition
    tello.move_forward(120)
    cfg.OutputAttitudePosition()
    tello.rotate_clockwise(180)
    cfg.OutputAttitudePosition()
    tello.move_forward(40)
    cfg.OutputAttitudePosition()
    #tello.move_back(80)
    tello.land()
    cfg.OutputAttitudePosition()




#Entrance
if __name__ == "__main__":

    #Connect to tello
    tello = Tello(cfg.telloIP_B)        #TelloB
    tello.connect()
    #tello.connect_to_wifi("tellonet","selvachess")


    #initialize and start location services on seperate thread
    locationThread = threading.Thread(target=IMU.init,args=(tello,),)
    locationThread.start()


    #Start manual control
    mc.EngageMC(tello)
    