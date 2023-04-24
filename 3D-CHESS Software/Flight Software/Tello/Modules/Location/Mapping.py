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
points = [(0,0,0,0,0),(0,0,0,0,0)]

def _drawPoints_(img, points):
    #print(points)
    for point in points:
        color = (point[2],point[3],point[4])
        
        cv2.circle(img, (point[1]+500,-1*point[0]+500), 5, color , cv2.FILLED)  # BGR
    prevpoint = points[-1]
    cv2.circle(img, (prevpoint[1]+500,-1*prevpoint[0]+500), 8, (prevpoint[2],prevpoint[3],prevpoint[4]), cv2.FILLED)
    cv2.putText(img, f'{(points[-1][0])/100 }, {(points[-1][1])/100}m',
                (points[-1][1] + 500, -1*points[-1][0] + 500), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)  # m NOT cm




def _tmapping_(ConnectedTello):
    from math import floor
    start = ConnectedTello.position     #Take off position. Represents 500x500
    color = ConnectedTello.color
    global points
    while True:
        pos = ConnectedTello.position
        if points[-1][0] != pos[0] or points[-1][1] != pos[1]:
             points.append((floor(pos[0]), floor(pos[1]),color[0],color[1],color[2]))
        sleep(1)


def _trmapping_(TR):
    from math import floor

    color = (0,0,255)
    global points
    addedTR =0
    while _allowMapping_:
        
        if len(TR) > addedTR:
            #print("TR")
            #print(TR[addedTR].taskLocation)
            points.append((floor(TR[addedTR].taskLocation[0][0]),floor(TR[addedTR].taskLocation[1][0]),color[0],color[1],color[2]))
            addedTR += 1
        sleep(.25)



def init(Tellos):
    from threading import Thread
    for t in Tellos:
        tMap = Thread(target=_tmapping_,args=(t,))
        tMap.start()
    from Modules._config_ import task_requests as tr
    trMap = Thread(target=_trmapping_,args=(tr,))
    trMap.start()
    global points
    
    while _allowMapping_:
        img = np.zeros((1000, 1000, 3), np.uint8)
        _drawPoints_(img,points)
        #print(points)
        cv2.imshow("Output",img)
        cv2.waitKey(1)