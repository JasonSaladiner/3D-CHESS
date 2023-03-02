"""
importable list of variables/functions
"""
from contextlib import contextmanager
import sys,os


#Tello IP addresses
telloIP_A = '192.168.1.11'
telloIP_B = '192.168.1.12'       #NEED to change to .12
telloIP_C = '192.168.1.13'


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

#Determine if emergency operations are occuring
emOps = False

#Simple attitude and position output for debugging. 
#May be removed in the future
def OutputAttitudePosition():
    print("X:",xPos,"Y:",yPos,"Z:",zPos,"Yaw:",yaw)
    adjust = lambda x : x+2
    print("Adjusted",adjust(xPos),adjust(yPos),adjust(zPos))