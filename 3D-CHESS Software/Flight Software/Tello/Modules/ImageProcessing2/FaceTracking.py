# import modules
import time

import numpy as np
import cv2
from djitellopy import tello

# Initialization
me = tello.Tello()
me.connect()
print(me.get_battery())
time.sleep(1)
me.streamoff()
me.streamon()
me.takeoff()
me.go_xyz_speed(0, 0, 30, 25)  # set height as needed

# Parameters
w, h = 360, 240
fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]  # adjust as needed
pError = 0


def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/facedetect.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 5)  # adjust minNeighbors as needed for clarity

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


def trackFace(info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - (w // 2)
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    # print(speed, fb)

    me.send_rc_control(0, fb, 0, speed)
    return error


# cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FPS, 30.0)  # figuring out if necessary or not

while True:
    # _, img = cap.read()
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    img, info = findFace(img)
    pError = trackFace(info, w, pid, pError)
    # print("Area", info[1], "Center", info[0])
    findFace(img)
    cv2.imshow("Output", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        me.land()
        break
