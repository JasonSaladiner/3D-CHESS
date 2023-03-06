# Import modules
from djitellopy import Tello
import time
import cv2

# Global variables
global img
# global tello


def LiveVideo(ConnectedTello):
    tello = ConnectedTello

    tello.streamon()
    tello.set_video_fps(tello.FPS_30)
    # time.sleep(2)  # is this needed?
    tello.set_video_direction(1)
