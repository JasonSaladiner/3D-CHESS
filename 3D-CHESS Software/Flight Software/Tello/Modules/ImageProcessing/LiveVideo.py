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
buffer = 2  # Adjust according to speed of Tello

def TR(ConnectedTello,x,y,img):
    import numpy as np
    possibleLocation = np.array([x,y]).reshape((2,1))
    duplicateRequest = False
    for tr in cfg.task_requests:
        np.linalg.norm(possibleLocation-tr.taskLocation[0:2,])
        if np.linalg.norm(possibleLocation-tr.taskLocation[0:2,]) < 100:
            duplicateRequest = True
            o = np.array(tr.offers)
            if o[np.argmax(o[:,1])][0] == ConnectedTello:
                cv2.imwrite(f'Flight Software/Tello/Resources/Images/Response_{ConnectedTello.name}_{tr.taskLocation[0][0],tr.taskLocation[1][0]}.jpg', img)
                print("Take Picture")
    #print(duplicateRequest)
    if not duplicateRequest:   
       cfg.task_requests.append(cfg.Task([x, y]))


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

    # Initialize function + video connection
    tello = ConnectedTello
    tello.streamon()
    time.sleep(2) # adjust as needed
    global start_time
    alert_status = False

    # Initalize TelloVision
    TV_width, TV_height, TV_x, TV_y = 650, 500, 975, 520
    cv2.namedWindow("TelloVision", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("TelloVision", TV_width, TV_height)
    cv2.moveWindow("TelloVision", TV_x, TV_y)
    
    while streamType == 'Live':
        imgL = tello.get_frame_read().frame
        imgL = cv2.resize(imgL, (int(TV_width / 2), int(TV_height / 2)))
        
        if streamShow == True:
            if ConnectedTello.name == "Tello_A":
                cv2.imshow("A", imgL)
                cv2.moveWindow("A", TV_x, TV_y)  # Top-left corner
            if ConnectedTello.name == "Tello_B":
                cv2.imshow("B", imgL)
                cv2.moveWindow("B", int(TV_x + .5 * TV_width), TV_y)  # Top-right corner
            if ConnectedTello.name == "Tello_C":
                cv2.imshow("C", imgL)
                cv2.moveWindow("C", TV_x, int(TV_y + .5 * TV_height))  # Bottom-left corner
            if ConnectedTello.name == "Tello_D":
                cv2.imshow("D", imgL)
                cv2.moveWindow("D", int(TV_x + .5 * TV_width), int(TV_y + .5 * TV_height))  # Bottom-right corner
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
            TR(ConnectedTello,x,y,imgFT)
            
            start_time = time.time()
            if takePic == True:
                cv2.imwrite(f'Flight Software/Tello/Resources/Images/{time.time()}.jpg', imgFT)
        elif area_val == 0 and time.time() - start_time > buffer:
            alert_status = False
            start_time = 0
        imgFT = cv2.resize(imgFT, (TV_width / 2, TV_height / 2))
        if alert_status == True:
            cv2.putText(imgFT, alert, (250, 30), cv2.FONT_HERSHEY_PLAIN, .85, ConnectedTello.color, 2)
        if streamShow == True:
            if ConnectedTello.name == "Tello_A":
                cv2.imshow("A", imgFT)
                cv2.moveWindow("A", TV_x, TV_y)  # Top-left corner
            if ConnectedTello.name == "Tello_B":
                cv2.imshow("B", imgFT)
                cv2.moveWindow("B", TV_x + .5 * TV_width, TV_y)  # Top-right corner
            if ConnectedTello.name == "Tello_C":
                cv2.imshow("C", imgFT)
                cv2.moveWindow("C", TV_x, TV_y + .5 * TV_height)  # Bottom-left corner
            if ConnectedTello.name == "Tello_D":
                cv2.imshow("D", imgFT)
                cv2.moveWindow("D", TV_x + .5 * TV_width, TV_y + .5 * TV_height)  # Bottom-right corner
        else:
            print(ConnectedTello.name + ': ' + alert)
        cv2.waitKey(5)


