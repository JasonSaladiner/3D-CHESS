"""
This program serves as the main flight module
From here, all other flight modules will be controlled in order to achieve 3D-CHESS conops
"""



import logging  #For changing the tello outputs
from djitellopy import Tello    #Tello 
import threading    #For multithreading
import Modules._config_ as cfg  #Shared variables 

import Modules.KeyboardControls.ManualControl as mc     #Manual Control of the drone
from Modules.Location import IMU            #Location services

Tello.LOGGER.setLevel(logging.WARNING)      #Setting tello outpus to warning only

#Connect to tello
tello = Tello()
tello.connect()








#Entrance
if __name__ == "__main__":

    #initialize and start location services on seperate thread
    xyz = threading.Thread(target=IMU.init,args=(tello,),)
    xyz.start()

    #Start manual control
    mc.EngageMC(tello)

    #mc._tempPattern_(tello)