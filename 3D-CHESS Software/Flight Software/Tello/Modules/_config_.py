"""
importable list of variables/functions
"""
from contextlib import contextmanager
import sys,os
import numpy as np
from math import exp
emerg = False

#Tello IP addresses
telloIP_A = '192.168.1.11'
telloIP_B = '192.168.1.12'     
telloIP_C = '192.168.1.13'


task_requests=[]

class Task:

    ActiveDrones = 1



    def __init__(self,location,science_potential=1,**constraints):

        #Initialize offer list and number of active drones (how long to wait)
        self.offers = []
        self.maxDrones = self.ActiveDrones

        self.loc = np.append(location,[0.])
        self.taskLocation = np.array(self.loc).reshape((3,1))

        self.sci = lambda x :science_potential*exp(-x/20)
        ##TODO: Task Requirements##
        ##Priority##