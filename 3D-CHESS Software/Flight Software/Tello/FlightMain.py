"""
This program serves as the main flight module
From here, all other flight modules will be controlled in order to achieve 3D-CHESS conops
"""



import ipaddress
import logging  #For changing the tello outputs
from djitellopy import Tello    #Tello 
import threading    #For multithreading

import Modules._config_ as cfg  #Shared variables 

import Modules.Controls.ManualControl as mc         #Manual Control of the drone
import Modules.Controls.ComputerControl as cc       #Computer Aided drone control
from Modules.Location import IMU,Mapping            #Location services







#Entrance
if __name__ == "__main__":
    
    #Enable/Disable Modules
    haveLogMessages = False
    haveLocation = True
    haveMap = True


    ########################################################################
                        ###Module Initializations###
    #Connect to tello
    tello = Tello(cfg.telloIP_B)        #TelloB
    #tello = Tello()
    tello.connect()
    #tello.connect_to_wifi("tellonet","selvachess")


    #initialize and start location services on seperate thread
    if haveLocation:
        locationThread = threading.Thread(target=IMU.init,args=(tello,),)
        locationThread.start()

    #Initialize the map and determine if it will be seen
                ###THIS IS UNTESTED###
    if haveMap and haveLocation:        #map depends on Location
        showMap = True
        mapThread = threading.Thread(target=Mapping.init,args=(showMap,),)
        mapThread.start()

    if not haveLogMessages:
        Tello.LOGGER.setLevel(logging.WARNING)      #Setting tello outpus to warning only

    ########################################################################
                        ###"MISSION" Commands###
    #testEmThread = threading.Thread(target=mc.EngageMC,args=(tello,),)
    print(tello.get_battery())
    #Start manual control
    mc.EngageMC(tello)
    