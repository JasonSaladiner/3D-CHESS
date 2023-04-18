# Import modules
from os import getcwd
from queue import Empty
from djitellopy import Tello
import time
import cv2
import os
import Modules._config_ as cfg

# Global variables + parameters
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
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)  # adjust minNeighbors as needed for clarity, default = 8

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

    # Initialize function + video connection
    tello = ConnectedTello
    tello.query_battery()  # testing purposes | DEMO
    tello.streamon()
    time.sleep(2) # adjust as needed
    #tello.set_video_direction(0) # Errors out randomly
    time.sleep(2) # adjust as needed
    global start_time
    alert_status = False

    while streamType == 'Live':
        imgL = tello.get_frame_read().frame
        imgL = cv2.resize(imgL, (400, 300))
        
        if streamShow == True:
            if ConnectedTello.name == "Tello_A":
                cv2.imshow("ConnectedTello.name", imgL)
                cv2.moveWindow("ConnectedTello.name", 0, 0)
            if ConnectedTello.name == "Tello_B":
                cv2.imshow("ConnectedTello.name", imgL)
                cv2.moveWindow("ConnectedTello.name", 0, 300)
            if ConnectedTello.name == "Tello_C":
                cv2.imshow("ConnectedTello.name", imgL)
                cv2.moveWindow("ConnectedTello.name", 0, 600)
        cv2.waitKey(5)

    while streamType == 'FT':
        #time.sleep(2) # if errors w/ first frame grab
        imgFT = tello.get_frame_read().frame
        imgFT, info = findFace(imgFT)
        area_val = info[1]  # area of face detected
        alert = 'OBJECT DETECTED'
        if area_val != 0 and start_time == 0:
            alert_status = True
            location = ConnectedTello.position
            x = location[0][0]
            y = location[1][0]
            cfg.task_requests.append(cfg.Task([x, y]))
            start_time = time.time()
            if takePic == True:
                cv2.imwrite(f'Flight Software/Tello/Resources/Images/{time.time()}.jpg', imgFT)
        elif area_val == 0 and time.time() - start_time > buffer:
            alert_status = False
            start_time = 0
        imgFT = cv2.resize(imgFT, (400, 300))
        if alert_status == True:
            cv2.putText(imgFT, alert, (250, 30), cv2.FONT_HERSHEY_PLAIN, .85, (0, 255, 255), 2)
        if streamShow == True:
            if ConnectedTello.name == "Tello_A":
                cv2.imshow("ConnectedTello.name", imgFT)
                cv2.moveWindow("ConnectedTello.name", 0, 0)
            if ConnectedTello.name == "Tello_B":
                cv2.imshow("ConnectedTello.name", imgFT)
                cv2.moveWindow("ConnectedTello.name", 0, 300)
            if ConnectedTello.name == "Tello_C":
                cv2.imshow("ConnectedTello.name", imgFT)
                cv2.moveWindow("ConnectedTello.name", 0, 600)
        else:
            print(ConnectedTello.name + ': ' + alert)
        cv2.waitKey(5)


