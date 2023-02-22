from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()


tello.move_left(100)
tello.rotate_counter_clockwise(90)
tello.rotate_clockwise(-90)
tello.move_foward(100)

tello.land()



if telcom == "w":
