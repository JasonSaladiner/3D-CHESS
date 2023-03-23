"""
This program serves as the main flight module
From here, all other flight modules will be controlled in order to achieve 3D-CHESS conops
"""



import ipaddress
import logging  #For changing the tello outputs
from djitellopy import Tello   #Tello 
from Modules import TelloFlightSoftware as TFS
from threading  import Thread    #For multithreading
import multiprocessing as mp

import Modules._config_ as cfg  #Shared variables 

import Modules.Controls.ManualControl as mc         #Manual Control of the drone
#import Modules.Controls.ComputerControl as cc       #Computer Aided drone control
from Modules.Location import IMU,Mapping            #Location services

from time import sleep
import os

def simpleSquare(ConnectedTello):
    tello = ConnectedTello
    #os.system('clear')
    sleep(3)
    tello.set_speed(40)
    tello.takeoff()
    print("Move Forward 2m")
    tello.move_forward(100)
    
    sleep(1)
    print("Rotate 90 degrees")
    tello.rotate_counter_clockwise(90)
    print("Move Left 1.5m")
    tello.move_forward(75)
    sleep(1)
    print("Rotate 90 degrees")
    tello.rotate_counter_clockwise(90)
    sleep(1)
    print("Move Back 2m")
    tello.move_forward(100)
    sleep(1)
    print("Rotate 90 degrees")
    tello.rotate_counter_clockwise(90)
    sleep(1)
    print("Move Right 1.5m")
    tello.move_forward(75)
    sleep(1)
    tello.rotate_counter_clockwise(90)
    tello.land()


def drone(ConnectedTello):
    ###DO stuff###
    tello = ConnectedTello

#Entrance
if __name__ == "__main__":
    
    #configs is representative of the kwargs for TFS. These are default values and if nothing is passed, these will be used
    #Drones may have different requirements so creating beforehand may not be the most effective method. Potentially create the dicrionary in the Process line at kwargs={}
    configs = {"TIR":True,
               "TIR_Resolution":10
               }
    #select drones
    A = True
    B = True
    C = False
    #turn on drones
    if A:
        TelloA = TFS(cfg.telloIP_A,logs= True,
                                   location= False,
                                   map= False,
                                   emControl= True,
                                   video= False,
                                   livestream= False
                                   )
        TA_thread = Thread(target=drone,args=(TelloA,),)
        TA_thread.start()
    if B:
        TelloB = TFS(cfg.telloIP_B,logs= True,
                                   location= False,
                                   map= False,
                                   emControl= True,
                                   video= False,
                                   livestream= False
                                   )
        TB_thread = Thread(target=drone,args=(TelloB,),)
        TB_thread.start()
    if C:
        TelloC = TFS(cfg.telloIP_C,logs= True,
                                   location= False,
                                   map= False,
                                   emControl= True,
                                   video= False,
                                   livestream= False
                                   )
        TC_thread = Thread(target=drone,args=(TelloC,),)
        TC_thread.start()
    
    input("Ready?")
    cfg.task_requests.append(self.nominal)