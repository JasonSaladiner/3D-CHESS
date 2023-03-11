"""
This module seeks to visualize the XY location of the tello in space for the operator. 
Dependency:
    Location services

"""

from time import sleep
import numpy as np
import cv2
from math import cos, sin, radians
import Modules._config_ as cfg
import threading


_allowMapping_ = True
_showMap_ = True

#cfg.xPos
#cfg.yPos


def _drawPoints_(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)  # BGR
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0]) / 100}, {((points[-1][1]) / 100)}m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)  # m NOT cm
    #cv2.putText(img, f'({(points[-1][0] - 500) / 100}, {-1 *((points[-1][1] - 500) / 100)}m',
    #           (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)  # m NOT cm

def mapping(ConnectedTello,showMap=True):
    from math import floor
    
    points = [(0, 0), (0, 0)]
    while _allowMapping_:
        pos = ConnectedTello.position
        img = np.zeros((1000, 1000, 3), np.uint8)
        
        if points[-1][0] != pos[0] or points[-1][1] != pos[1]:
            
            points.append((floor(pos[0]), floor(pos[1])))
        _drawPoints_(img, points)
        if _showMap_:
            cv2.imshow("Output", img)
        cv2.waitKey(1)
    #End thread
    return

def _stopMap_():
    _allowMapping_ = False

def mapOn():
    _showMap_ = True

def mapOff():
    _showMap_ = False


"""
def init(ConnectedTello,showMap = True):
    global _showMap_
    global _allowMapping_
    global tello
    tello = ConnectedTello
    _showMap_ = showMap
    _allowMapping_ = True
    _mapping_()
"""