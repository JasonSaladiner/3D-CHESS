"""
This program serves as the main flight module
From here, all other flight modules will be controlled in order to achieve 3D-CHESS conops
"""



import ipaddress
import logging  #For changing the tello outputs
from djitellopy import Tello   #Tello 
from Modules import TelloFlightSoftware as TFS
import threading    #For multithreading
import multiprocessing as mp

import Modules._config_ as cfg  #Shared variables 

import Modules.Controls.ManualControl as mc         #Manual Control of the drone
import Modules.Controls.ComputerControl as cc       #Computer Aided drone control
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



def startDrone(TelloLetter:str,**kwargs):
    """
    startDrone will connect to and set up the selected drone and then will execute all drone specific functionality. 
    Intended to be the target of a process
    """
    
    IP = {"a":'192.168.1.11',"b": '192.168.1.12',"c":'192.168.1.13'}
    tello = TFS(IP[TelloLetter.lower()],**kwargs)
    

#Entrance
if __name__ == "__main__":
    
    #configs is representative of the kwargs for TFS. These are default values and if nothing is passed, these will be used
    #Drones may have different requirements so creating beforehand may not be the most effective method. Potentially create the dicrionary in the Process line at kwargs={}
    configs = {"logs": False,
               "location": True,
               "map": False,
               "emControl":True,
               "video":True,
               "livestream":True
               }
    
    processA = mp.Process(target=startDrone,args=("a",),kwargs={"emControl":False,"video":False})
    processB = mp.Process(target=startDrone,args=("b",),kwargs=configs)
    