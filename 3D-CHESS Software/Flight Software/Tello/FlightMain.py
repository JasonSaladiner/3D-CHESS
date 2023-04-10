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




#Entrance
if __name__ == "__main__":
    
    #All drone kwargs are contained within the docustring of TFS. Below is a sample with all the default values (only different values need be passed)
    #kwargs =   logs= False
    #           location= True
    #           emControl= True        (manControl = False)
    #           video= True
    #           livestream= True       (tracking = Flase)
    #           showstream=True
    #           takepic = False
    #           takeOffLocation = (0,0,0)
    #           coverageArea = [] (list of verticies)
    #           auto = False


    #Config may be used to add artificial constraints in near future updates but for now its used to distiguse between Different Tellos


    #List of Tellos for mapping
    Tellos = []
    #select drones
    A = False
    B = True
    C = False
    #turn on drones
    if A:
        TelloA = TFS(cfg.telloIP_A,logs= True,
                                   location= True,
                                   map= True,
                                   emControl= False,
                                   video= False,
                                   livestream= False,
                                   sim = True,
                                   coverageArea = [[0,0],[-100,0],[-100,-100],[0,-100]],
                                   auto = True
                                   )
        Tellos.append(TelloA)
    if B:
        TelloB = TFS(cfg.telloIP_B,logs= False,
                                   location= True,
                                   map= True,
                                   emControl= False,
                                   video= False,
                                   livestream= False,
                                   sim = False,
                                   coverageArea = [[0,0],[150,0],[150,150],[0,150]],
                                   auto = True
                                   )
        Tellos.append(TelloB)
    if C:
        TelloC = TFS(cfg.telloIP_C,logs= True,
                                   location= False,
                                   map= False,
                                   emControl= False,
                                   video= False,
                                   livestream= False
                                   )
        Tellos.append(TelloC)
    

    mapping = True
    if mapping:
        from Modules.Location.Mapping import init
        mapThread = Thread(target=init,args=(Tellos,))
        mapThread.start()
    
    ###Known ISSUE###
    #There are times when commands in quick succession confuses the drone. Make sure to use closed loop methods for future to hopefully prevent
    #t = Tello()
    #t.connect()
    #t.connect_to_wifi("tellonet","selvachess")

    input("Ready?")
    cfg.task_requests.append(cfg.Task([250,250]))