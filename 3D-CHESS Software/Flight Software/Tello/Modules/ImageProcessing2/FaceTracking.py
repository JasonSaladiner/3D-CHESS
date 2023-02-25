# import modules
import numpy as np
import cv2


def findFace(img):
    faceCascade = cv2.CascadeClassifier("Resources/facedetect.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []  # cx, cy = center of face detected
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)


cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FPS, 30.0)  # without this, latency is crap

while True:
    _, img = cap.read()
    findFace(img)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
