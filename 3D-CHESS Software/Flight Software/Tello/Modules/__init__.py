##Modules __init__

__all__ = []


from djitellopy import Tello as djiTello
import logging
import threading
import numpy as np
import socket
from typing import Optional 

#from .enforce_types import enforce_types




class TelloFlightSoftware(djiTello):
    
    """
    Subclass that inherits all of the djitellopy Tello class (here called djiTello)
    also has internet and thread intializations specific to 3dChess
    Optional Args:
        'logs','location','map','showmap','emControl' (or 'manControl'),'video','livestream'
    """
    dmToin = 10/2.54
    cmToin = 1/2.54


    udp_port = {'192.168.1.11':8869,   #A
                '192.168.1.12':8879,   #B
                '192.168.1.13':8889}   #C

    ###TODO###
    #go_xyz_speed()
    #go_xyz_speed_mid()
    #go_xyz_speed_yaw_mid()
    #Dont use these unitl they have been added

    def _rotationMatrix_(self,yaw):
        import numpy as np
        from math import sin,cos,radians
        self.yawrad = radians(yaw)
        return np.array([cos(self.yawrad),-sin(self.yawrad),0,
                         sin(self.yawrad),cos(self.yawrad),0,
                         0,0,1]).reshape((3,3))

    def _newCommand_(self,bodyVector,yaw):
        self.rotationMatrix = self._rotationMatrix_(yaw)
        self.Nvect = np.matmul(self.rotationMatrix,bodyVector).reshape((3,1))
        
        self.commandVector = self.commandVector + self.Nvect


    def move_forward(self,travelDistance:float,unit:str = 'cm'):
        #Get travelDistance in proper form/unit
        self.x = travelDistance
        if unit == 'in':
            self.x /= self.cmToin
        from math import floor
        self.x = floor(self.x)
        
        #get orientation
        self.yaw = self.t.get_yaw()
        self.bodyVector = np.array([self.x,0,0])

        #Apply to the commandVector
        self._newCommand_(self.bodyVector,self.yaw)
        
        #Apply the move distance using super class
        self.t.move_forward(self.x)

    def move_back(self,travelDistance:float,unit:str = 'cm'):
        #Get travelDistance in proper form/unit
        self.x = travelDistance
        if unit == 'in':
            self.x /= self.cmToin
        from math import floor
        self.x = floor(self.x)
        
        #get orientation
        self.yaw = self.t.get_yaw()
        self.bodyVector = np.array([-self.x,0,0])

        #Apply to the commandVector
        self._newCommand_(self.bodyVector,self.yaw)
        

        #Apply the move distance using super class
        self.t.move_back(self.x)

    def move_left(self,travelDistance:float,unit:str = 'cm'):
        #Get travelDistance in proper form/unit
        self.x = travelDistance
        if unit == 'in':
            self.x /= self.cmToin
        from math import floor
        self.x = floor(self.x)
        
        #get orientation
        self.yaw = self.t.get_yaw()
        self.bodyVector = np.array([0,-self.x,0])

        #Apply to the commandVector
        self._newCommand_(self.bodyVector,self.yaw)
        
        #Apply the move distance using super class
        self.t.move_left(self.x)

    def move_right(self,travelDistance:float,unit:str = 'cm'):
        #Get travelDistance in proper form/unit
        self.x = travelDistance
        if unit == 'in':
            self.x /= self.cmToin
        from math import floor
        self.x = floor(self.x)
        
        #get orientation
        self.yaw = self.t.get_yaw()
        self.bodyVector = np.array([0,self.x,0])

        #Apply to the commandVector
        self._newCommand_(self.bodyVector,self.yaw)
        
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
        
        #Get current time    
        import time
        self.curTime = time.time()

        if not abs(self.curTime-self.lastRCcommandTime) < 1e-8:
            #Get change in time
            self.dt = self.curTime-self.lastRCcommandTime

            self.bV = np.array([self.lastRCcommand[1]*self.dt,self.lastRCcommand[0]*self.dt,self.lastRCcommand[2]*self.dt]).reshape((3,1))
            self.yaw = self.t.get_yaw()
            #Apply the last RC command over the change in time
            self._newCommand_(self.bV,self.yaw)
            
            #reset last RC command
            self.lastRCcommand = self.rcIn
            self.lastRCcommandTime = self.curTime

            #Apply the move distance using super class
            self.t.send_rc_control(self.rcIn[0],self.rcIn[1],self.rcIn[2],self.rcIn[3])

    def takeoff(self,*takeoffLocation:float):
        """
        Command connected tello to takeoff
        Optional:
        *takeoff location: X,Y,Z float of the takeoff location
        """
        
        for i in range(len(takeoffLocation)):
            self.position[i] = takeoffLocation[i]
            self.IMUVector[i]= takeoffLocation[i]
            self.commandVector[i] = takeoffLocation[i]
        self.t.takeoff()


    def _updatePosition_(self,dt = .5,IMU_weight = 0,command_weight=1):
        """
        Meant to run as a seperate thread. Starts the IMU thread if necessary and continually takes the weighted average of IMU and Commands
        Updates location and the IMU and Command at time steps equalt to dt
        """
        
        import numpy as np
        from time import sleep
        from Modules.Location import IMU
        
        if IMU_weight > 0:
            self.IMUThread = threading.Thread(target=IMU.init,args=(self.t,),)
            self.IMUThread.start()

        while True:
            
            self.deltaIMU = self.IMUVector-self.position
            self.deltaCommand = self.commandVector-self.position

            self.delta = IMU_weight*self.deltaIMU + command_weight*self.deltaCommand
            self.delta = self.delta.reshape((3,1))
            self.position = self.position + self.delta
            self.commandVector = self.position
            self.IMUVector = self.position
            sleep(dt)

    def threadSetup(self):
        """
        Initalizes selected threads
        allowLocation = True : initializes the IMU location service thread to update cfg.X,Y,Z
        allowMap = True : starts the live mapping service
            showMap = True : outputs the map. 
        """

        
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



    def _tempPattern_(self):
        from time import sleep
        sleep(3)
        self.takeoff()
        
        self.move_forward(100)
        sleep(1)
        self.rotate_counter_clockwise(90)

        self.move_forward(100)
        sleep(1)
        self.rotate_counter_clockwise(90)

        self.move_forward(100)
        sleep(1)
        self.rotate_counter_clockwise(90)

        self.move_forward(100)
        sleep(1)
        self.rotate_counter_clockwise(90)

        self.land()

    def __init__(self,IP,**kwargs):
        import time
        
        """
        initialize the drone and connect to it
        IP : str
        """
        self.haveLogs = False
        #Location Thread
        self.haveLocation = True
        #Mapping Thread
        self.haveMap = False
        self.showMap = True
        #Manual Control
        self.emControl = True
        #Live Video
        self.haveVideo = True
        self.livestream = True

        for self.k in kwargs:
            if self.k == 'logs':
                self.haveLogs = kwargs[self.k]
            elif self.k == 'location':
                self.haveLocation = kwargs[self.k]
            elif self.k == 'map':
                self.haveMap = kwargs[self.k]
            elif self.k == 'showmap':
                self.showMap = kwargs[self.k]
            elif self.k == 'emControl':
                self.emControl = kwargs[self.k]
            elif self.k == 'manControl':
                self.emControl = not kwargs[self.k]
            elif self.k =='video':
                self.haveVideo = kwargs[self.k]
            elif self.k == 'livestream':
                self.livestream = kwargs[self.k]
        if not self.haveLogs:
            djiTello.LOGGER.setLevel(logging.WARNING)      #Setting tello output to warning only


        
        #self.last_rc_control_timestamp = time.time()
        self.lastRCcommandTime = time.time()        #Duplicate??

        #Command input and IMU locations
        self.commandVector = np.array([0,0,0]).reshape((3,1))        #X,Y,Z in cm
        self.IMUVector = np.array([0,0,0]).reshape((3,1))            #X,Y,Z in cm

        #Actual Position
        self.position = np.array([0,0,0]).reshape((3,1))             #X,Y,Z in cm

        self.lastRCcommand = 0,0,0,0


        #djiTello.CONTROL_UDP_PORT = TelloFlightSoftware.udp_port[IP]
        #djiTello.STATE_UDP_PORT = TelloFlightSoftware.udp_port[IP]+1
        super().__init__(IP)
        self.connect()


        if self.haveLocation:
            #from Modules.Location import IMU
            self.locationThread = threading.Thread(target=IMU.init,args=(self.t,),)
            self.locationThread = threading.Thread(target=self._updatePosition_)
            self.locationThread.start()

        #Initialize the map and determine if it will be seen
        if self.haveMap and self.haveLocation:        #map depends on Location
            from Modules.Location import Mapping
            self.mapThread = threading.Thread(target=Mapping.mapping,args=(self,self.showMap,),)
            self.mapThread.start()
        

        #Emergency Vs Manual Control (One is required)
        if self.emControl:
            from Modules.Controls.ManualControl import EmergencyControls as emc
            self.controlThread = threading.Thread(target=emc,args=(self,),)
            self.controlThread.start()
        else:
            from Modules.Controls.ManualControl import EngageMC as mc
            self.controlThread = threading.Thread(target=mc,args=(self,),)
            self.controlThread.start()

        if self.haveVideo:
            from Modules.ImageProcessing.LiveVideo import startVideo
            if self.livestream:
                self.videoThread = threading.Thread(target = startVideo,args=(self,'Live'),)
            else:
                self.videoThread = threading.Thread(target=startVideo,args=(self,),)

            self.videoThread.start()

        



        
        
        














#https://beenje.github.io/blog/posts/logging-to-a-tkinter-scrolledtext-widget/
#LOOK into this for logging console outputs