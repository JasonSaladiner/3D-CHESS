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

        for self.k in kwargs:
            if self.k == 'logs':
                self.haveLogs = kwargs[self.k]
            elif self.k == 'location':
                self.haveLocation = kwargs[self.k]
            elif self.k == 'map':
                self.haveMap = kwargs[self.k]
            elif self.k == 'showmap':
                self.showMap = kwargs[self.k]
        if not self.haveLogs:
            djiTello.LOGGER.setLevel(logging.WARNING)      #Setting tello output to warning only



        self.t = super()
        self.t.__init__(IP)
        self.t.connect()

        print(self.t.get_battery())

