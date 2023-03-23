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
    #tello.threadSetup()
    if TelloLetter == 'b':
        tello.takeoff()
        tello.rotate_clockwise(30)
        sleep(1)
        tello.land()

#Entrance
if __name__ == "__main__":
    
    #configs is representative of the kwargs for TFS. These are default values and if nothing is passed, these will be used
    #Drones may have different requirements so creating beforehand may not be the most effective method. Potentially create the dicrionary in the Process line at kwargs={}
    configs = {"logs": True,
               "location": False,
               "map": False,
               "emControl":True,
               "video":False,
               "livestream":False
               }
    
    droneA = Thread(target=startDrone,args=("a",),kwargs={"logs":True,"emControl":False,"video":False,"first":True})
    droneB = Thread(target=startDrone,args=("b",),kwargs=configs)
    
    droneA.start()
    droneB.start()

    #da = TFS(cfg.telloIP_A,logs=True)
    #db = TFS(cfg.telloIP_B,logs=True)