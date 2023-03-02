"""
importable list of variables
"""
from contextlib import contextmanager
import sys,os


#Tello IP addresses
telloIP_A = '192.168.1.11'
telloIP_B = '192.168.1.12'       #NEED to change to .12
telloIP_C = '192.168.1.13'



#with cfg.suppress_out():
@contextmanager
def suppress_out():
    with open(os.devnull,"w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


xPos = 0
yPos = 0
zPos = 0
yaw = 0


emOps = False

def OutputAttitudePosition():
    print("X:",xPos,"Y:",yPos,"Z:",zPos,"Yaw:",yaw)
    adjust = lambda x : x+2
    print("Adjusted",adjust(xPos),adjust(yPos),adjust(zPos))