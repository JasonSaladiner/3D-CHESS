# Import modules
from os import getcwd
from queue import Empty
from djitellopy import Tello
import time
import cv2
import os
import Modules._config_ as cfg  


# Global variables + parameters
global img, img_base, buffer
start_time = 0
buffer = 3  # Adjust according to speed of Tello
currentDir = os.getcwd()


# Royal Function
def startVideo(ConnectedTello, streamType='FT', streamShow = True, takePic=False):
    # Error if streamType or takePic not valid
    streamTypes = ['Live', 'FT']
    takePics = [True, False]
    if streamType not in streamTypes:
        raise ValueError("Invalid streamType type. Expected one of: %s" % streamTypes)
    if takePic not in takePics:
        raise ValueError("Invalid takePic type. Expected one of: %s" % takePics)

    # Initialize function + video connection
    tello = ConnectedTello
    tello.query_battery()  # testing purposes | DEMO
    tello.streamon()
    time.sleep(2) # adjust as needed
    global start_time, ind1, ind2
    alert_status = False

    while streamType == 'Live':
        imgL = tello.get_frame_read().frame
        imgL = cv2.resize(imgL, (400, 300))
        if streamShow == True:
            if ConnectedTello.name == "Tello_A":
                cv2.imshow(ConnectedTello.name, imgL)
                cv2.moveWindow(ConnectedTello.name, 0, 0)
            if ConnectedTello.name == "Tello_B":
                cv2.imshow(ConnectedTello.name, imgL)
                cv2.moveWindow(ConnectedTello.name, 0, 300)
            if ConnectedTello.name == "Tello_C":
                cv2.imshow(ConnectedTello.name, imgL)
                cv2.moveWindow(ConnectedTello.name, 0, 600)
        cv2.waitKey(5)

    while streamType == 'FT':
        imgFT = tello.get_frame_read().frame
        predictions, index = myClassifier.getPrediction(imgFT, scale=1, pos=(0, 30))
        if start_time == 0 and index != 0:
            start_time = time.time()
        if time.time() - start_time < buffer:
            if index == 1:
                ind1 += 1
            elif index ==2:
                ind2 += 1
        elif time.time() - start_time > buffer:
            start_time = 0
            if ind1 > ind2 and ind1 >= indmin:
                print('HIGH DETECTION: CUP')
                location = ConnectedTello.position
                x = location[0][0]
                y = location[1][0]
                cfg.task_requests.append(cfg.Task([x, y]))
            elif ind2 > ind1 and ind2 >= indmin:
                print('HIGH DETECTION: SLEEVE')
                x = location[0][0]
                y = location[1][0]
                cfg.task_requests.append(cfg.Task([x, y]))
            ind1 = 0
            ind2 = 0
        imgFT = cv2.resize(imgFT, (400, 300))
        if streamShow == True:
            if ConnectedTello.name == "Tello_A":
                cv2.imshow(ConnectedTello.name, imgFT)
                cv2.moveWindow(ConnectedTello.name, 0, 0)
            if ConnectedTello.name == "Tello_B":
                cv2.imshow(ConnectedTello.name, imgFT)
                cv2.moveWindow(ConnectedTello.name, 0, 300)
            if ConnectedTello.name == "Tello_C":
                cv2.imshow(ConnectedTello.name, imgFT)
                cv2.moveWindow(ConnectedTello.name, 0, 600)
        else:

            print(ConnectedTello.name + ': OBJECT OF INTEREST ADDED TO TASK REQUESTS')
        cv2.waitKey(5)


