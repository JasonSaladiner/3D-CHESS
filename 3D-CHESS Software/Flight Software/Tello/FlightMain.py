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
import Modules.ImageProcessing.LiveVideo as lv
import Modules.Controls.ManualControl as mc         #Manual Control of the drone


from time import sleep
import os



  # Connecting drones to my wifi
#tello_C = Tello()
#tello_C.connect()
#tello_C.connect_to_wifi('ConnectoPatronum','73752677')

def drone(ConnectedTello):
    ###DO stuff###
    tello = ConnectedTello

#Entrance
if __name__ == "__main__":
    
    
    #Config may be used to add artificial constraints in near future updates but for now its used to distinguish between Different Tellos
    configs = {"TIR":True
               }
    #select drones
    A = False
    B = False
    C = True
    #turn on drones
    if A:
        TelloA = TFS(cfg.telloIP_A,logs= False,
                                   location= False,
                                   map= False,
                                   emControl= True,
                                   video= True,
                                   livestream= True
                                   )
        TelloA.setConstraints(con="hi")
        #TA_thread = Thread(target=drone,args=(TelloA,),)
        #TA_thread.start()
    if B:
        TelloB = TFS(cfg.telloIP_B,logs= False,
                                   location= True,
                                   map= False,
                                   emControl= False,
                                   video= True,
                                   livestream= False
                                   )
        TelloB.setConstraints(**configs)
        #TB_thread = Thread(target=drone,args=(TelloB,),)
        #TB_thread.start()
    if C:
        TelloC = TFS(cfg.telloIP_C,logs= True,
                                   location= False,
                                   map= False,
                                   emControl= False,
                                   video= True,
                                   livestream= False
                                   )
        TelloC.setConstraints(bleh="meh")
        #TC_thread = Thread(target=drone,args=(TelloC,),)
        #TC_thread.start()
    
    ###Known ISSUE###
    #There are times when commands in quick succession confuses the drone. Make sure to use closed loop methods for future to hopefully prevent


  

    #input("Ready?")
    #TelloB.setColor()
    #cfg.task_requests.append(1)
    #TelloA.end()
    #TelloB.end()