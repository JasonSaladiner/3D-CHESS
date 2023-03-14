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


def gui():
    import tkinter as tk
    window = tk.Tk()
    logs = tk.Label()

#Entrance
if __name__ == "__main__":

    tello_B = TFS(cfg.telloIP_B,emControl = False,logs = False,map=True)
    tello_B.threadSetup()
    
    #input("Start?")
    #print("this now runs")

   