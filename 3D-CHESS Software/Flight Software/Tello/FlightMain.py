"""
This program serves as the main flight module
From here, all other flight modules will be controlled in order to achieve 3D-CHESS conops
"""



import ipaddress
import logging  #For changing the tello outputs
from djitellopy import Tello   #Tello 
from Modules import TelloFlightSoftware as TFS
import threading    #For multithreading
import cv2

import Modules._config_ as cfg  #Shared variables 

import Modules.Controls.ManualControl as mc         #Manual Control of the drone
import Modules.Controls.ComputerControl as cc       #Computer Aided drone control
from Modules.Location import IMU,Mapping            #Location services

from time import sleep
import os

def samplePattern(ConnectedTello):
    tello = ConnectedTello
    os.system('clear')
    sleep(3)
    tello.set_speed(40)
    tello.takeoff()
    print("Move Forward 4m")
    tello.move_forward(400)
    sleep(1)
    print("Move Left 3m")
    tello.move_left(300)
    sleep(1)
    print("Rotate 180 degrees")
    tello.rotate_clockwise(180)
    sleep(1)
    print("Move \'Forward\' 4m")
    tello.move_forward(400)
    sleep(1)
    print("Rotate another 90 degrees")
    tello.rotate_clockwise(90)
    sleep(1)
    print("Move \'Forward\' 3m")
    tello.move_forward(300)
    sleep(1)
    tello.land()

#Entrance
if __name__ == "__main__":

    tello_B = TFS(cfg.telloIP_B,emControl = False,logs = False,map=True)
    tello_B.threadSetup()
    
    input("Start?")
    samplePattern(tello_B)

   