##Modules __init__

__all__ = []


from djitellopy import Tello as djiTello
import logging
import threading



class TelloFlightSoftware(djiTello):
    
    """
    Subclass that inherits all of the djitellopy Tello class (here called djiTello)
    also has internet and thread intializations specific to 3dChess
    """
    dmToin = 10/2.54
    cmToin = 1/2.54
    def move_forward(self,travelDistance:float,unit:str = 'cm'):
        #Get travelDistance in proper form/unit
        self.x = travelDistance
        if unit == 'in':
            self.x /= self.cmToin
        from math import floor
        self.x = floor(self.x)
        #Apply to the commandVector
        self.commandVector[0] += self.x
        #Apply the move distance using super class
        self.t.move_forward(self.x)

    def move_back(self,travelDistance:float,unit:str = 'cm'):
        #Get travelDistance in proper form/unit
        self.x = travelDistance
        if unit == 'in':
            self.x /= self.cmToin
        from math import floor
        self.x = floor(self.x)
        #Apply to the commandVector
        self.commandVector[0] -= self.x
        #Apply the move distance using super class
        self.t.move_back(self.x)

    def move_left(self,travelDistance:float,unit:str = 'cm'):
        #Get travelDistance in proper form/unit
        self.x = travelDistance
        if unit == 'in':
            self.x /= self.cmToin
        from math import floor
        self.x = floor(self.x)
        #Apply to the commandVector
        self.commandVector[1] -= self.x
        #Apply the move distance using super class
        self.t.move_left(self.x)

    def move_right(self,travelDistance:float,unit:str = 'cm'):
        #Get travelDistance in proper form/unit
        self.x = travelDistance
        if unit == 'in':
            self.x /= self.cmToin
        from math import floor
        self.x = floor(self.x)
        #Apply to the commandVector
        self.commandVector[1] += self.x
        #Apply the move distance using super class
        self.t.move_right(self.x)

    def send_rc_control(self,rightVelcoity:float=0,forVelocity:float=0,downVelocity:float=0,yawVelocity:float=0,unit:str='cm'):
        #Get travelDistance in proper form/unit
        self.rcIn = [rightVelcoity,forVelocity,downVelocity,yawVelocity]
        from math import floor
        for self.i in range(4):
            if unit == 'in':
                self.rcIn[self.i] /= self.cmToin
            self.rcIn[self.i] = floor(self.rcIn[self.i])
            

        self.commandVector[0] += self.rcIn[1]
        self.commandVector[1] += self.rcIn[0]
        self.commandVector[2] += self.rcIn[2]
        #Apply the move distance using super class
        self.t.send_rc_control(self.rcIn[0],self.rcIn[1],self.rcIn[2],self.rcIn[3])


    def threadSetup(self):
        """
        Initalizes selected threads
        allowLocation = True : initializes the IMU location service thread to update cfg.X,Y,Z
        allowMap = True : starts the live mapping service
            showMap = True : outputs the map. 
        """

        if self.haveLocation:
            from Modules.Location import IMU
            self.locationThread = threading.Thread(target=IMU.init,args=(self.t,),)
            self.locationThread.start()

        #Initialize the map and determine if it will be seen
                    ###THIS IS UNTESTED###
        if self.haveMap and self.haveLocation:        #map depends on Location
            from Modules.Location import Mapping
            self.mapThread = threading.Thread(target=Mapping.init,args=(self.showMap,),)
            self.mapThread.start()
        
        if self.emControl:
            from Modules.Controls.ManualControl import EmergencyControls as emc
            self.emcThread = threading.Thread(target=emc,args=(self.t,),)
            self.emcThread.start()

    def wifi(self,SSID:str = 'tellonet',password:str = 'selvachess'):
        """
        connect the drone to the specific wifi (default is tellonet)
        """
        
        self.t.connect_to_wifi(SSID,password)
    

    def runMission(self,mission,*args,**kwargs):
        """
        Runs a specific mission function
        Very basic first set up. Might delete or update 
        """

        self.re = mission(*args,**kwargs)
        if self.re != None:
            return self.re


    def __init__(self,IP:str,**kwargs):
        """
        initialize the drone and connect to it
        """
        self.haveLogs = True
        #Location Thread
        self.haveLocation = True
        #Mapping Thread
        self.haveMap = False
        self.showMap = True
        #Manual Control
        self.emControl = True

        for self.k in kwargs:
            if self.k == 'logs':
                self.haveLogs = kwargs[self.k]
            elif self.k == 'location':
                self.haveLocation = kwargs[self.k]
            elif self.k == 'map':
                self.haveMap = kwargs[self.k]
            elif self.k == 'showmap':
                self.showMap = kwargs[self.k]
            elif self.k == 'emergency':
                self.emControl = kwargs[self.k]
        if not self.haveLogs:
            djiTello.LOGGER.setLevel(logging.WARNING)      #Setting tello output to warning only



        self.t = super()
        self.t.__init__(IP)
        self.t.connect()

        print(self.t.get_battery())


        self.commandVector = [0,0,0]        #X,Y,Z in cm




#Write log to CSV
