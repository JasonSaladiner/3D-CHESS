# import modules
import numpy as np
import cv2

def findFace(img):




cap = cv2.VideoCapture(0)
while True:
    _, img = cap.read()
    cv2.imshow("Output", img)
    cv2.waitKey(1)

