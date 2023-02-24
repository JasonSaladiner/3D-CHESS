from djitellopy import Tello
import cv2
import time

# User Input for Coordinates
print('Input XY coordinates in centimeters: ')
x_ui = int(input('X: '))
y_ui = int(input('Y: '))

# Initialization
tello = Tello()
tello.connect()
print("Battery: " + str(tello.get_battery()))

# Go to XY Coordinates
tello.takeoff()
tello.go_xyz_speed(y_ui, -x_ui, 20, 30)  # ADJUST SPEED AS DESIRED
time.sleep(2)

# Capture image at specified location
tello.land()
quit()
