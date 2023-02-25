# import modules
import numpy as np
import cv2

def findFace(img):
    faceCascade = cv2.CascadeClassifier("venv/facedetect.hml")
    imgGray = cv2.cvtColor()



cap = cv2.VideoCapture(0)
while True:
    _, img = cap.read()
    cv2.imshow("Output", img)
    cv2.waitKey(1)

