"""
importable list of variables/functions
"""
from contextlib import contextmanager
import sys,os
import numpy as np
from math import exp
emerg = False
from collections.abc import Iterable
#Tello IP addresses
telloIP_A = '192.168.1.11'
telloIP_B = '192.168.1.12'     
telloIP_C = '192.168.1.13'


task_requests=[]



class sensor:

    def __init__(self,resolution,FOV):
        """
            class that defines a sensor by resolution and FOV
        """
        self.resolution = resolution
        self.FOV = FOV

class VNIR(sensor):
    """
    sub class of sensor specifically a VNIR
    """

    def __init__(self,resolution,FOV):
        super().__init__(resolution,FOV)

class TIR(sensor):
    """
    sub class of sensor specifically a TIR
    """

    def __init__(self,resolution,FOV):
        super().__init__(resolution,FOV)

class Radar(sensor):
    """
    sub class of sensor specifically a Radar
    """

    def __init__(self,resolution,FOV):
        super().__init__(resolution,FOV)

sampleConstraints = {"sensor":VNIR,
                    "resolution":10.,
                    "FOV":100.}


class Task:

    ActiveDrones = 1



    def __init__(self,location,science_potential=1,constraints=sampleConstraints):

        #Initialize offer list and number of active drones (how long to wait)
        self.offers = []
        self.maxDrones = self.ActiveDrones

        self.loc = np.append(location,[0.])
        self.taskLocation = np.array(self.loc).reshape((3,1))


        self.lagtime  = 30 #sec

        self.sci = lambda x :science_potential*exp(-pow(0,1+(x/20-self.lagtime)/abs(x/20-self.lagtime)))

        self.con = constraints

        ##TODO: Task Requirements##
        ##Priority##






