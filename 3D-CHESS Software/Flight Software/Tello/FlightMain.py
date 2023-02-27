"""
This program serves as the main flight module
From here, all other flight modules will be controlled in order to achieve 3D-CHESS conops
"""

from djitellopy import Tello
import Modules.KeyboardControls.ManualControl as mc
from Modules.Location import IMU
from multiprocessing import Process
import threading



tello = Tello()
#tello.connect()

#xyz = threading.Thread(target=IMU.init(tello))
#mc.init()
xyz = Process(target=IMU.init)#,args=([tello]))
xyz.start()


#control = threading.Thread(target=mc.EngageMC(tello))
mc.EngageMC(tello)
#control.start()
#xyz.start()
#control.join()