# Import modules
from os import getcwd
from queue import Empty
from djitellopy import Tello
import time
import cv2
import os

# Global variables + parameters
w, h = 640, 480
global img, img_base
global buffer
start_time = 0
buffer = 5  # Adjust according to speed of Tello


# Subject Function
def findFace(img):
    # Pull current directory for any user
    current_dir = os.getcwd()
    dir = current_dir + '/Flight Software/Tello/Resources/facedetect.xml'
    faceCascade = cv2.CascadeClassifier(dir)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 6)  # adjust minNeighbors as needed for clarity, OG = 8

    myFaceListC = []  # cx, cy = center of face detected
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + (w // 2)
        cy = y + (h // 2)
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


# Royal Functions
def startVideo(ConnectedTello, streamType='FT', takePic=False):
    # Error if streamType or takePic not valid
    streamTypes = ['Live', 'FT']
    takePics = [True, False]
    if streamType not in streamTypes:
        raise ValueError("Invalid streamType type. Expected one of: %s" % streamTypes)
    if takePic not in takePics:
        raise ValueError("Invalid takePic type. Expected one of: %s" % takePics)
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
    global start_time

    while streamType == 'Live':
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (w, h))
        cv2.imshow("LStream"+t_name, img)
        cv2.waitKey(5)

    while streamType == 'FT':
        img_base = tello.get_frame_read().frame
        img, info = findFace(img_base)
        area_val = info[1]
        if area_val != 0 and start_time == 0:
            start_time = time.time()
            print('OBJECT OF INTEREST DETECTED')
            if takePic == True:
                cv2.imwrite(f'Flight Software/Tello/Resources/Images/{time.time()}.jpg', img_base)
        elif area_val == 0 and time.time() - start_time > buffer:
            start_time = 0
        img = cv2.resize(img, (w, h))
        cv2.imshow("LStreamFT"+t_name, img)
        cv2.waitKey(5)

# Untested
def stopVideo(ConnectedTello):
    tello = ConnectedTello
    tello.streamoff()
    pass


