"""
This program serves as the main flight module
From here, all other flight modules will be controlled in order to achieve 3D-CHESS conops
"""



import ipaddress
import logging  #For changing the tello outputs
from djitellopy import Tello as djiTello   #Tello 
import threading    #For multithreading
import cv2

import Modules._config_ as cfg  #Shared variables 

import Modules.Controls.ManualControl as mc         #Manual Control of the drone
import Modules.Controls.ComputerControl as cc       #Computer Aided drone control
from Modules.Location import IMU,Mapping            #Location services

from time import sleep

haveLogMessages = False
if not haveLogMessages:
    djiTello.LOGGER.setLevel(logging.WARNING)      #Setting tello outpus to warning only


class Tello(djiTello):
    
    """
    Subclass that inherits all of the djitellopy Tello class (here called djiTello)
    also has internet and thread intializations specific to 3dChess
    """

    #Location Thread
    allowLocation = True
    #Mapping Thread
    allowMap = False
    showMap = True


    def threadSetup(self):
        """
        Initalizes selected threads
        allowLocation = True : initializes the IMU location service thread to update cfg.X,Y,Z
        allowMap = True : starts the live mapping service
            showMap = True : outputs the map. 
        """

        if self.haveLocation:
            self.locationThread = threading.Thread(target=IMU.init,args=(self.t,),)
            self.locationThread.start()

        #Initialize the map and determine if it will be seen
                    ###THIS IS UNTESTED###
        if self.haveMap and self.haveLocation:        #map depends on Location
            self.mapThread = threading.Thread(target=Mapping.init,args=(self.showMap,),)
            self.mapThread.start()


    def wifi(self,SSID:str = 'tellonet',password:str = 'selvachess'):
        """
        connect the drone to the specific wifi (default is tellonet)
        """
        
        self.t.connect_to_wifi(SSID,password)
    

    def runMission(self,mission:function,*args,**kwargs):
        """
        Runs a specific mission function
        Very basic first set up. Might delete or update 
        """

        self.re = mission(*args,**kwargs)
        if self.re != None:
            return self.re


    def __init__(self,IP:str):
        """
        initialize the drone and connect to it
        """
        self.t = djiTello(IP)
        self.t.connect()
        print(self.t.get_battery())


#Entrance
if __name__ == "__main__":
    tello_B = Tello(cfg.telloIP_B)
    #tello_B.wifi()
    tello_B.threadSetup()

    tello_B.runMission(cc.move_to_waypoints,tello_B,cc.sampleWaypoints)


    #Start manual control
    #mc.EngageMC(tello_B)
    