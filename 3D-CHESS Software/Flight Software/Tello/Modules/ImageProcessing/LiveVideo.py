# Import modules
from djitellopy import Tello
import time
import cv2

# Global variables
global img
# global tello


def startVideo(ConnectedTello, LiveStream=True):
    tello = ConnectedTello
    tello.streamon()
    tello.set_video_fps(tello.FPS_30)
    tello.set_video_direction(1)

    while LiveStream == True:
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        cv2.imshow("Image", img)
        cv2.waitKey(2)
        if cv2.waitKey(1) & 0xff == ord('q'):
            tello.land()
        break



