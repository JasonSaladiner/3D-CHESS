# Import modules
from djitellopy import Tello
import time
import cv2

# Global variables
global img
# global tello


def startVideo(ConnectedTello, streamType='Live'):
    # Error if streamType not valid
    streamTypes = ['Live', 'FT']
    if streamType not in streamTypes:
        raise ValueError("Invalid streamType type. Expected one of: %s" % streamTypes)
    # Create naming scheme for cv2 windows
    t = time.localtime()
    t_name = time.strftime("%H%M%S", t)
    # Initialize function + video connection
    tello = ConnectedTello
    tello.query_battery()  # testing purposes | DEMO
    tello.streamon()
    time.sleep(2) # adjust as needed
    tello.set_video_direction(0)
    time.sleep(2) # adjust as needed

    while streamType == 'Live':
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        cv2.imshow("LStream"+t_name, img)  # untested, should name view w/ timestamp
        cv2.waitKey(5)

    while streamType == 'FT':
        pass




