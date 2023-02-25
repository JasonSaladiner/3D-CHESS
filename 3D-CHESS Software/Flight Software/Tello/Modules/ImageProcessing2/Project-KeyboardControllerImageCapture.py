from djitellopy import Tello
import KeyPressModule as kp
import time
import cv2

kp.init()
me = Tello()
me.connect()
print(me.get_battery())
global img
me.streamon()
me.set_video_fps(me.FPS_30)
time.sleep(10)


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
    if kp.getKey("e"): me.takeoff()
    if kp.getKey("q"): me.land()

    if kp.getKey("p"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(2)

    return [lr, fb, ud, yv]


me.set_video_direction(1)

while True:
    vals = getKeyboardInput()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    cv2.imshow("Image", img)
    cv2.waitKey(2)
