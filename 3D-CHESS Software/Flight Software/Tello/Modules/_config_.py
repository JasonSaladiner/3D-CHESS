"""
importable list of variables
"""
from contextlib import contextmanager
import sys,os

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