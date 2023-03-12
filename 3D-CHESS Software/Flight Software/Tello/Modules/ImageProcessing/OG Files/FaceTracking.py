# import modules
import time
import numpy as np
import cv2
from djitellopy import Tello

# Initialization
tello = Tello()
tello.connect()
print(tello.get_battery())
tello.send_rc_control(0, 0, 0, 0)
tello.streamoff()
tello.streamon()
time.sleep(5)
tello.set_video_direction(0)  # ideally, 1 | errors out, so 3d-printing component 
tello.takeoff()


# Parameters
w, h = 640, 480
fbRange = [25000, 30000]  # test: when stable --> 2 ft or so
pid = [0.4, 0.4, 0]  # adjust as needed
pError = 0


def findFace(img):  # ONLY RUN VIA PYCHARM | ELSE DIRECTORY ERROR OCCURS
    faceCascade = cv2.CascadeClassifier("Resources/facedetect.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 7)  # adjust minNeighbors as needed for clarity, OG = 8

    myFaceListC = []  # cx, cy = center of face detected
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + (w // 2)
        cy = y + (h // 2)
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListC.append([cx, cy])  # drone will rotate based on this
        myFaceListArea.append(area)  # drone will move F/B based on this

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(info, w, pid, pError):  # NEW EDIT | EDITING MOVEMENT STYLE
    area = info[1]
    x, y = info[0]
    fb = 0

    ## should speed be yaw or lateral movement? 
    ## yaw brings detection error w/ high minNeighors
    ## without high minNeighbors, increased false positives occur
    error_x = x - (w // 2)
    speed = pid[0] * error_x + pid[1] * (error_x - pError)
    speed = int(np.clip(speed, -10, 10))  # adjust speed to cover residual drift
    # if speed is so clipped, rather than using a PID, why not just speed = fb?


    
    #########################################################################
    # PERFORM YAW --> LOSS OF DETECTION | LR_VEL = +/- (DEP. ON YAW INPUT)  #
    #########################################################################


    # ADDING HEIGHT ADJUSTMENT
    error_y = y - (h / 2)
    
    # UNTESTED
    if -80 < error_y < 80:  # covers 160px deadZone
        fby = 0
    elif error_y > 80:
        fby = -10  # adjust speed to cover residual drift
    elif error_y < -80:
        fby = 10  # adjust speed to cover residual drift

    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -10  # adjust speed to cover residual drift
    elif area < fbRange[0] and area != 0:
        fb = 10  # adjust speed to cover residual drift

    if x == 0 or y == 0:
        speed = 0
        error = 0

    tello.send_rc_control(0, fb, fby, speed)
    return error_x, error_y


while True:
    img = tello.get_frame_read().frame
    img, info = findFace(img)
    img = cv2.resize(img, (w, h))
    cv2.imshow("tellosight", img)
    pError = trackFace(info, w, pid, pError)
    cv2.waitKey(5)
    if cv2.waitKey(1) & 0xff == ord('q'):
        tello.land()
        break
