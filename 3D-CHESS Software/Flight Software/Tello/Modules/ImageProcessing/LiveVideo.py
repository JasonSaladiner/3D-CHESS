# Import modules
from djitellopy import Tello
import time
import cv2

# Global variables
global img
# global tello


def startVideo(ConnectedTello, liveStream=True):
    tello = ConnectedTello
    tello.streamon()
    tello.set_video_fps(tello.FPS_30)
    tello.set_video_direction(1)

