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
    #os.system('clear')
    sleep(3)
    tello.set_speed(40)
    tello.takeoff()
    print("Move Forward 2m")
    tello.move_forward(200)
    
    sleep(1)
    print("Rotate 180 degrees")
    tello.rotate_counter_clockwise(90)
    print("Move Left 1.5m")
    tello.move_forward(150)
    sleep(1)
    print("Rotate 90 degrees")
    tello.rotate_counter_clockwise(90)
    sleep(1)
    print("Move Back 2m")
    tello.move_forward(200)
    sleep(1)
    print("Rotate another 90 degrees")
    tello.rotate_counter_clockwise(90)
    sleep(1)
    print("Move Right 1.5m")
    tello.move_forward(150)
    sleep(1)
    tello.rotate_counter_clockwise(90)
    tello.land()

#Entrance
if __name__ == "__main__":

    tello_B = TFS(cfg.telloIP_B,emControl = True,logs = False,map=True,video = False)
    tello_B.threadSetup()
    
    input("Start?")
    #samplePattern(tello_B)
    tello_B.takeoff()
    print(tello_B.position)
    tello_B.move_forward(100)
    print(tello_B.position)
    tello_B.move_back(75)
    print(tello_B.position)
    tello_B.land()