# Import modules
from os import getcwd
from queue import Empty
from djitellopy import Tello
import time
import cv2
import os
import cvzone
import Modules._config_ as cfg  #Shared variables 
from cvzone.ClassificationModule import Classifier

# Global variables + parameters
global img, img_base, buffer
start_time = 0
buffer = 3  # Adjust according to speed of Tello
currentDir = os.getcwd()
myClassifier = Classifier(currentDir + '\\Flight Software/Tello/Resources/keras_model.h5', currentDir + '\\Flight Software/Tello/Resources/labels.txt')
fpsReader = cvzone.FPS()
ind1 = 0
ind2 = 0
indmin=2


# Royal Function
def startVideo(ConnectedTello, streamType='FT', streamShow = True, takePic=False):
    # Error if streamType or takePic not valid
    streamTypes = ['Live', 'FT']
    takePics = [True, False]
    if streamType not in streamTypes:
        raise ValueError("Invalid streamType type. Expected one of: %s" % streamTypes)
    if takePic not in takePics:
        raise ValueError("Invalid takePic type. Expected one of: %s" % takePics)

    # Color identities for each Tello
    TelloColors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
    TelloColor = None
    if ConnectedTello.name == "Tello_A":
        TelloColor = TelloColors[0]
    elif ConnectedTello.name == "Tello_B":
        TelloColor = TelloColors[1]
    elif ConnectedTello.name == "Tello_C":
        TelloColor = TelloColors[2]

    # Create naming scheme for cv2 windows
    t = time.localtime()
    t_name = time.strftime("%H%M%S", t)

    # Initialize function + video connection
    tello = ConnectedTello
    #tello.query_battery()  # testing purposes | DEMO
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
        #time.sleep(2) # if errors w/ first frame grab
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
            if ind1 > ind2 and ind1 > indmin:
                print('HIGH DETECTION: CUP')
                cfg.task_requests.append(cfg.Task([ConnectedTello.position[0][0],ConnectedTello.position[1][0]]))
            elif ind2 > ind1 and ind2 > indmin:
                print('HIGH DETECTION: SLEEVE')
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


