from djitellopy import Tello

# User Input for Coordinates
print('Input XY coordinates in centimeters: ')
x_ui = int(input('X: '))
y_ui = int(input('Y: '))

# Initialization
tello = Tello()
tello.connect()
print("Battery: " + str(tello.get_battery()))

tello.takeoff()
tello.go_xyz_speed(y_ui, -x_ui, 0, 30)  # ADJUST SPEED AS DESIRED
tello.land()
quit()
