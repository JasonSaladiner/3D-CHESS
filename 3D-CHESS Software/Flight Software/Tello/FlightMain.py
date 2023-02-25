"""
This program serves as the main flight module
From here, all other flight modules will be controlled in order to achieve 3D-CHESS conops
"""

from djitellopy import Tello
import Modules.KeyboardControls.ManualControl as mc
tello = Tello()
#tello.connect()
mc.EngageMC(tello)
