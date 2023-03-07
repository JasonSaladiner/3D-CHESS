# Import modules
from djitellopy import Tello
import time
import cv2

# Global variables
global img
# global tello


def startVideo(ConnectedTello, streamType='Live'):
    tello = ConnectedTello
    tello.query_battery()  # testing purposes
    tello.streamon()
    time.sleep(2)
    tello.set_video_direction(0)
    time.sleep(2)

    while streamType == 'Live':
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        cv2.imshow("Image", img)
        cv2.waitKey(5)





