# Import modules
import cv2
import time
from threading import Thread
from djitellopy import Tello
import KeyPressModule as kp

# Initialization
global img
tello = Tello()
tello.connect()
print(tello.get_battery())
tello.streamoff()
tello.streamon()
tello.set_video_direction(1)
# tello.set_video_fps(tello.FPS_30)  # comment/uncomment as needed
time.sleep(5)  # adjust accordingly


# Functions
def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    spd = 25

    if kp.getKey("LEFT"):
        lr = -spd
    elif kp.getKey("RIGHT"):
        lr = spd
    if kp.getKey("UP"):
        fb = spd
    elif kp.getKey("DOWN"):
        fb = -spd
    if kp.getKey("w"):
        ud = spd
    elif kp.getKey("s"):
        ud = -spd
    if kp.getKey("a"):
        yv = -spd
    elif kp.getKey("d"):
        yv = spd
    if kp.getKey("e"):
        tello.takeoff()
    if kp.getKey("q"):
        tello.land()

    if kp.getKey("p"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(2)

    if kp.getKey("["):
        pass
    if kp.getKey("]"):
        pass

    return [lr, fb, ud, yv]


while True:
    vals = getKeyboardInput()
    tello.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = tello.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(2)
