# Import modules
from os import getcwd
from djitellopy import Tello
import time
import cv2
import os

# Global variables + parameters
w, h = 640, 480
global img


# Subject Function
def findFace(img):
    current_dir = os.getcwd()
    dir=current_dir+'/Flight Software/Tello/Resources/facedetect.xml'
    faceCascade = cv2.CascadeClassifier(dir)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)  # adjust minNeighbors as needed for clarity, OG = 8

    myFaceListC = []  # cx, cy = center of face detected
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + (w // 2)
        cy = y + (h // 2)
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


# Royal Function
def startVideo(ConnectedTello, streamType):
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
        img = cv2.resize(img, (w, h))
        cv2.imshow("LStream"+t_name, img)
        cv2.waitKey(5)

    while streamType == 'FT':
        img = tello.get_frame_read().frame
        img, info = findFace(img)
        img = cv2.resize(img, (w, h))
        cv2.imshow("LStreamFT"+t_name, img)
        cv2.waitKey(5)


