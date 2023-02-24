from djitellopy import Tello
import KeyPressModule as kp
from time import sleep
import numpy as np
import cv2
from math import cos, sin, radians

# Parameters
x, y = 500, 500
a = 0
yaw = 0
fSpeed = 117 / 10  # 15 cm/s theoretical
aSpeed = 360 / 10  # 50 deg/s theoretical
interval = 0.25

dInterval = fSpeed * interval
aInterval = aSpeed * interval

# Initialization
kp.init()
me = Tello()
me.connect()
print(me.get_battery())

points = [(0, 0), (0, 0)]


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    spd = 15
    aspd = 50
    global x, y, a, yaw
    d = 0

    if kp.getKey("LEFT"):
        lr = -spd
        d = dInterval
        a = -180
    elif kp.getKey("RIGHT"):
        lr = spd
        d = -dInterval
        a = 180
    if kp.getKey("UP"):
        fb = spd
        d = dInterval
        a = 270
    elif kp.getKey("DOWN"):
        fb = -spd
        d = -dInterval
        a = -90
    if kp.getKey("w"):
        ud = spd
    elif kp.getKey("s"):
        ud = -spd
    if kp.getKey("a"):
        yv = -aspd
        yaw -= aInterval
    elif kp.getKey("d"):
        yv = aspd
        yaw += aInterval

    if kp.getKey("e"): me.takeoff()
    if kp.getKey("q"): me.land()

    sleep(interval)
    a += yaw
    x += int(d * cos(radians(a)))
    y += int(d * sin(radians(a)))

    return [lr, fb, ud, yv, x, y]


def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)  # BGR
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0] - 500) / 100}, {(points[-1][1] - 500) / 100}m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)  # m NOT cm


while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    img = np.zeros((1000, 1000, 3), np.uint8)
    if points[-1][0] != vals[4] or points[-1][1] != vals[5]:
        points.append((vals[4], vals[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)
    cv2.waitKey(1)
