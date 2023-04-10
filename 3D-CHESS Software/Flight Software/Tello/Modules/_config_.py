"""
importable list of variables/functions
"""
from contextlib import contextmanager
import sys,os
import numpy as np

#Tello IP addresses
telloIP_A = '192.168.1.11'
telloIP_B = '192.168.1.12'     
telloIP_C = '192.168.1.13'


task_requests=[]

class Task:





    def __init__(self,location,**constraints):

        #Initialize offer list and number of active drones (how long to wait)
        self.offers = []
        self.maxDrones = 1

        self.loc = location.append(0.)
        self.taskLocation = np.array(self.loc).reshape((3,1))


        ##TODO: Task Requirements##