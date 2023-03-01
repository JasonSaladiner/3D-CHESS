"""
This program serves as the main flight module
From here, all other flight modules will be controlled in order to achieve 3D-CHESS conops
"""



import logging  #For changing the tello outputs
from djitellopy import Tello    #Tello 
import threading    #For multithreading
import Modules._config_ as cfg  #Shared variables 

import Modules.Controls.ManualControl as mc     #Manual Control of the drone
from Modules.Location import IMU            #Location services
#from Modules.Controls.ReturnToHome import return_to_home as rth
Tello.LOGGER.setLevel(logging.WARNING)      #Setting tello outpus to warning only

#Connect to tello
tello = Tello()
tello.connect()




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

    #initialize and start location services on seperate thread
    xyz = threading.Thread(target=IMU.init,args=(tello,),)
    xyz.start()

    #Start manual control
    #mc.EngageMC(tello)
    #cfg.OutputAttitudePosition
    print(tello.get_battery())
    #cfg.OutputAttitudePosition()
    #tello.takeoff()
    #tello.rotate_clockwise(360)
    #cfg.OutputAttitudePosition()
    #mc.EngageMC(tello)
    _temp_()