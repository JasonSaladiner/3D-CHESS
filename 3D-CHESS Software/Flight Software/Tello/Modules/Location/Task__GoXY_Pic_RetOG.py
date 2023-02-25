# import modules
from djitellopy import Tello
import cv2
import time

# Initialization
tello = Tello()
tello.connect()
print("Battery: " + str(tello.get_battery()))
spd = 30


# Capture image and save in dedicated folder
def TakePhoto(tello):
    tello.streamoff()
    tello.streamon()
    tello.set_video_direction(1)
    time.sleep(5)
    img = tello.get_frame_read().frame
    cv2.resize(img, (320, 240))
    cv2.imwrite(f'Images/{time.time()}.jpg', img)
    tello.streamoff()


# User Input for Coordinates
time.sleep(1)
print('Input XY coordinates in centimeters: ')
x_ui = int(input('X: '))
y_ui = int(input('Y: '))

# Go to XY Coordinates
tello.takeoff()
tello.go_xyz_speed(y_ui, -x_ui, 30, spd)  # ADJUST SPEED AS DESIRED

# Take a picture
TakePhoto(tello)

# Return to origin
tello.go_xyz_speed(-y_ui, x_ui, -30, spd)

tello.land()
quit()
