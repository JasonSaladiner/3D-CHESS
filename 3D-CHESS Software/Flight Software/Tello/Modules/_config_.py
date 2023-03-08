"""
importable list of variables/functions
"""
from contextlib import contextmanager
import sys,os


#Tello IP addresses
telloIP_A = '192.168.1.11'
telloIP_B = '192.168.1.12'     
telloIP_C = '192.168.1.13'

dmToin = 10/2.54
#dmToin = 1
@contextmanager
def suppress_out():
    """
    This will suppress the output of some text when using the with command:

    with cfg.suppress_out():
    """
    with open(os.devnull,"w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


#Inertial X,Y,Z positions
xPos = 0
yPos = 0
zPos = 0
yaw = 0

#locationUpdate is a dictionary for creating of known location points that can be keyed when certain pictures are seen
#by the camera. Needs to be expanded/changed as needed
locationUpdate = {"L0" : [0,0,0]}
def updateLocation(location:str):
    """
    forces the drone to update the location
    location:str = a location of the form L# (e.g. L0). A key in the locationUpdate dictionary above
    """
    try:
        xPos = locationUpdate[location][0]
        yPos = locationUpdate[location][1]
        zPos = locationUpdate[location][2]
    except:
        print("Location not valid")
        


#Determine if emergency operations are occuring
emOps = False

#Simple attitude and position output for debugging. 
#May be removed in the future
def OutputAttitudePosition():
    print("X:",xPos,"Y:",yPos,"Z:",zPos,"Yaw:",yaw)
    adjust = lambda x : x+2
    print("Adjusted",adjust(xPos),adjust(yPos),adjust(zPos))