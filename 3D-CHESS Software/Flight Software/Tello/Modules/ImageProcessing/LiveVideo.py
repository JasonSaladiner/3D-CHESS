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
buffer = 3  # Adjust according to speed of Tello


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
def startVideo(ConnectedTello, TelloName, streamType='FT', takePic=False):
    # Error if NameTello, streamType, or takePic not valid   
    TelloNames = ['tello_A', 'tello_B', 'tello_C']
    streamTypes = ['Live', 'FT']
    takePics = [True, False]
    if TelloName not in TelloNames:
        raise ValueError("Invalid TelloName type. Expected one of: %s" % TelloNames)
    if streamType not in streamTypes:
        raise ValueError("Invalid streamType type. Expected one of: %s" % streamTypes)
    if takePic not in takePics:
        raise ValueError("Invalid takePic type. Expected one of: %s" % takePics)

    # Color identities for each Tello
    TelloColors = [(0, 0, 255), (0, 255, 0), (255, 0, 0)]
    TelloColor = None
    if TelloName == TelloNames[0]:
        TelloColor = TelloColors[0]
    elif TelloName == TelloNames[1]:
        TelloColor = TelloColors[1]
    elif TelloName == TelloNames[2]:
        TelloColor = TelloColors[2]

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
    alert_status = False

    while streamType == 'Live':
        img = tello.get_frame_read().frame
        img = cv2.resize(img, (w, h))
        #telloPOS = TFC(tello_C)
        #currentPOS = tello.position
        #print(currentPOS)
        cv2.putText(img, TelloName, (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, TelloColor, 2)
        cv2.imshow(TelloName + "LStream" + t_name, img)
        cv2.waitKey(5)

    while streamType == 'FT':
        img_base = tello.get_frame_read().frame
        img, info = findFace(img_base)
        area_val = info[1]
        alert = 'OBJECT DETECTED'
        if area_val != 0 and start_time == 0:
            alert_status = True
            start_time = time.time()
            if takePic == True:
                cv2.imwrite(f'Flight Software/Tello/Resources/Images/{time.time()}.jpg', img_base)
        elif area_val == 0 and time.time() - start_time > buffer:
            alert_status = False
            start_time = 0
        img = cv2.resize(img, (w, h))
        cv2.putText(img, TelloName, (20, 30), cv2.FONT_HERSHEY_PLAIN, 2, TelloColor, 2)
        if alert_status == True:
            cv2.putText(img, alert, (300, 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
        cv2.imshow("FTStream" + t_name, img)
        cv2.waitKey(5)

# Untested w/ threading
def stopVideo(ConnectedTello):
    tello = ConnectedTello
    tello.streamoff()
    pass


