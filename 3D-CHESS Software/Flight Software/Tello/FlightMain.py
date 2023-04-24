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
from Modules._config_ import VNIR,TIR,Radar
import Modules.Controls.ManualControl as mc         #Manual Control of the drone
#import Modules.Controls.ComputerControl as cc       #Computer Aided drone control
from Modules.Location import IMU,Mapping            #Location services

from time import sleep
import os




#Entrance
if __name__ == "__main__":
    emergencyControls = True
    mapping = True
    
    connect = False
    sim = False

    if sim:
        emergencyControls = False

    if connect:
        t = Tello()
        t.connect()
        t.connect_to_wifi("tellonet","selvachess")


    #All drone kwargs are contained within the docustring of TFS. Below is a sample with all the default values (only different values need be passed)
    #kwargs =   logs= False
    #           location= True
    #           video= True
    #           livestream= True       (tracking = Flase)
    #           showstream=True
    #           takepic = False
    #           takeOffLocation = [0,0,0]
    #           coverageArea = [(x1,y1),(x2,y2)...] (list of verticies)
    #           auto = False


    #Config may be used to add artificial constraints in near future updates but for now its used to distiguse between Different Tellos


    #List of Tellos for mapping
    Tellos = []
    #select drones
    A = False
    B = True
    C = True
    D = False
    #turn on drones
    if A:
        TelloA = TFS(cfg.telloIP_A,OBS = [VNIR(9.,100.)],
                                   logs= False,
                                   location= True,
                                   video= True,
                                   tracking= True,
                                   sim = sim,
                                   takeoffLocation = [50,50,0],
                                   coverageArea = [[50,50],[250,50],[250,300],[50,300]],
                                   auto = True
                                   )
        Tellos.append(TelloA)
    if B:
        TelloB = TFS(cfg.telloIP_B,OBS=[VNIR(10.,110.),VNIR(10.,120.),TIR(8.,100.)],
                                   logs= False,
                                   location= True,
                                   video= True,
                                   tracking= True,
                                   sim = sim,
                                   takeoffLocation = [-60,-120,0],
                                   coverageArea = [[-60,-120],[60,-120],[60,0],[-60,0]],
                                   auto = True
                                   )
        Tellos.append(TelloB)
    if C:
        TelloC = TFS(cfg.telloIP_C,OBS=[VNIR(10.,110.),VNIR(10.,120.),TIR(8.,100.)],
                                   logs= True,
                                   location= True,
                                   video= True,
                                   tracking= True,
                                   sim = sim,
                                   takeoffLocation = [120,240,0],
                                   coverageArea = [[120,240],[120,120],[0,120],[0,240]],
                                   auto = True
                                   )
        Tellos.append(TelloC)
    if D:
        TelloD = TFS(cfg.telloIP_D,OBS=[VNIR(9.,100.)],
                                   logs= True,
                                   location= True,
                                   video= True,
                                   tracking= True,
                                   sim = sim,
                                   takeoffLocation = [50,50,0],
                                   coverageArea = [[50,50],[250,50],[250,300],[50,300]],
                                   auto = True
                                   )
        Tellos.append(TelloD)
    cfg.Task.ActiveDrones = len(Tellos)
    
    if mapping:
        from Modules.Location.Mapping import init
        mapThread = Thread(target=init,args=(Tellos,))
        mapThread.start()
    
    if emergencyControls:
        ##Escape and Delete are land and emergency for all
        ##1,2,3 are land for the first, second, and third drone respectively (A,B,C when all three exist)
        ##9,8,7 are emergency for the first, second, and third drone respectively (A,B,C when all three exist)
        from Modules.Controls.ManualControl import EmergencyControls
        emCThread = Thread(target=EmergencyControls,args=(Tellos,))
        emCThread.start()

    ###Known ISSUE###
    #There are times when commands in quick succession confuses the drone. Make sure to use closed loop methods for future to hopefully prevent
    
    #input("Ready?")
    #cfg.task_requests.append(cfg.Task([-250,250],20))
    #cfg.task_requests.append(cfg.Task([TelloA.position[0][0],TelloA.position[1][0]]))
    #input("Ready?")
    #cfg.task_requests.append(cfg.Task([-300,-250]))
    #input("Ready?")
    #cfg.task_requests.append(cfg.Task([TelloA.position[0][0],TelloA.position[1][0]],5))

    while not sim:
        if cfg.emerg:
            os._exit(0)
    