##Modules __init__

__all__ = []


from djitellopy import Tello as djiTello
import logging
import threading
import numpy as np
import socket
from typing import Optional 
from time import sleep,time
import Modules._config_ as cfg
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

    #Depreceated. Failed experiment. Will remove 
    udp_port = {'192.168.1.11':8869,   #A
                '192.168.1.12':8879,   #B
                '192.168.1.13':8889}   #C

    vs_port = {'192.168.1.11':11111,   #A
                '192.168.1.12':11112,   #B
                '192.168.1.13':11113}   #C

    


    ############################################# Movement ###############################################
        ###Not Adding. Do not Use###
    #go_xyz_speed()
    #go_xyz_speed_mid()
    #go_xyz_speed_yaw_mid()


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


    def goto(self, waypoint:list,timeout:float = 60):
        """
        goto will fly tello until its internal position is within 0.1m of waypoint. Uses self.velocity for speed.
        Assumption:
            - If len(waypoint) == 2: (x,y)
            - If len(waypoint) == 3: (x,y,z)
            - Else error
        input:
            timeout is maximum time to complete. If moving slow and need to go really far maybe adjust
        """


        if len(waypoint) == 2:
            self.waypoint = waypoint
            self.waypoint.append(self.position[2])
        elif len(waypoint) == 3:
            self.waypoint = waypoint
        else:
            print("Error goto expected positional data with len of 2 or 3. Got something else")
            return None
        self.waypoint = np.array(self.waypoint).reshape((3,1))
        self.gotoVector = self.position-self.waypoint

        self.bodygotoVector = np.matmul(np.linalg.inv(self._rotationMatrix_(self.get_yaw())),self.gotoVector)

        self.bUV = self.bodygotoVector / np.linalg.norm(self.bodygotoVector)        #body unit vector

        self.previousgotoVector = self.gotoVector

        self.gotoTimeOut = time.time()+timeout

        self.send_rc_control(self.bUV[1]*self.velocity,self.bUv[0]*self.velocity,self.bUV[2]*self.velocity,0)
        while np.linalg.norm(self.bodygotoVector) > 0.1:
            sleep(0.1/self.velocity)
            self.nextgotoVector = self.gotoVector = self.position-self.waypoint
            
            self.furtherCheck = self.previousgotoVector -self.nextgotoVector
            if self.furtherCheck[0] < -0.1 or self.furtherCheck[1] < -0.1 or self.furtherCheck[2] < -0.1:
                #growing further away
                print("Some distance is getting bigger")
                ####Could try again. Should I?
                break
        self.send_rc_control(0,0,0,0)

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


    ################################## Update functions  ######################################

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

    
    def _getTask_(self):
        ####NOTE: Likely Going to change after PDR ######

        totalTask = 0
        while True:
            if len(cfg.task_requests) > totalTask:
                if cfg.task_requests[-1] == 1:
                    self.nominal()
                totalTask+=1

            sleep(1)


    ########################### Setup #######################################

    def setConstraints(self,**kwargs):
        """
        Set the artificial constraints of the system
        Needs functionality
        Anything not found is assumed false
        """
        ####NOTE: Likely going to change after PDR#####
        for self.k in kwargs:
            if self.k == "TIR":
                self.nominal = self._squarePattern_
            else:
                self.nominal = self._linePattern_


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


        self.velocity = 20 #cm/s
        
        #self.last_rc_control_timestamp = time.time()
        self.lastRCcommandTime = time.time()        #Duplicate??

        #Command input and IMU locations
        self.commandVector = np.array([0,0,0]).reshape((3,1))        #X,Y,Z in cm
        self.IMUVector = np.array([0,0,0]).reshape((3,1))            #X,Y,Z in cm

        #Actual Position
        self.position = np.array([0,0,0]).reshape((3,1))             #X,Y,Z in cm

        self.lastRCcommand = 0,0,0,0
        self.t = super()
        self.t.__init__(IP)
        self.connect()


        if self.haveLocation:
            #from Modules.Location import IMU
            #self.locationThread = threading.Thread(target=IMU.init,args=(self.t,),)
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
            #self.controlThread.start()

        if self.haveVideo:
            self.VS_UDP_PORT = self.vs_port[IP]
            self.send_command_with_return("port 8890 " + str(self.vs_port[IP]))
            
            from Modules.ImageProcessing.LiveVideo import startVideo
            if self.livestream:
                self.videoThread = threading.Thread(target = startVideo,args=(self,'Live'),)
            else:
                self.videoThread = threading.Thread(target=startVideo,args=(self,),)

            self.videoThread.start()

        self.updateThread = threading.Thread(target=self._getTask_)
        self.updateThread.start()
        



        
        
        














#https://beenje.github.io/blog/posts/logging-to-a-tkinter-scrolledtext-widget/
#LOOK into this for logging console outputs