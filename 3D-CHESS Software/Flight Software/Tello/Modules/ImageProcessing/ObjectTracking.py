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
tello.set_video_direction(0)  # 0 for front, 1 for down
time.sleep(3)
# tello.takeoff()

# tello.go_xyz_speed(0, 0, 30, 25)  # set height as needed

# Parameters
w, h = 640, 480
fbRange = [25000, 30000]
pid = [0.4, 0.4, 0]  # adjust as needed
pError = 0


def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/haar_square.xml")  # adjust haar cascade file accordingly
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)  # adjust minNeighbors as needed for clarity, OG = 8

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
    speed = int(np.clip(speed, -10, 10))  # adjust speed to cover residual drift

    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = -10  # adjust speed to cover residual drift
    elif area < fbRange[0] and area != 0:
        fb = 10  # adjust speed to cover residual drift

    if x == 0:
        speed = 0
        error = 0

    # tello.send_rc_control(0, fb, 0, speed)
    return error


# cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FPS, 30.0)  # figuring out if necessary or not

while True:
    # _, img = cap.read()
    img = tello.get_frame_read().frame
    img, info = findFace(img)
    img = cv2.resize(img, (w, h))
    cv2.imshow("tellosight", img)
    pError = trackFace(info, w, pid, pError)
    cv2.waitKey(1)
    # print("Area", info[1], "Center", info[0])
    # findFace(img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        # tello.land()
        break
