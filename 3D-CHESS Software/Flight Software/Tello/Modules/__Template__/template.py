"""
This is a template subpackage to ease in creation. In order to make a new subpackage:
1) Copy the __Template__ folder and rename it (only 1 word. Use camelcasing as needed)
2) Rename template.py to appropriate module name.
3) In __init__.py, in __all__ change "template" to new module name exaclty (case sensitve)
4) Code as usual in your new module
5) Create as many modules as you need ensuring that each one is reflected in the __all__. 
6) If you need to refrence sibling or children modules, use absolute refrences (start from "Modules". Should take the form import Modules.__Template__.template)
If you have any questions or issues, let Jason know.

NOTE: once you set up your script as a module/subpackage, you can't test it by running that python file directly. You should go to some higher level file (e.g. FlightMain.py)
and import your subpackage as if you were using it for a real flight scenario. This is tedious at first so if you prefer to develop code not in package for first that is ok, 
you just may have bugs when turing it into a subpackage. Either method is ok
"""
