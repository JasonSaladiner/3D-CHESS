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
from math import cos,sin,pi
import Modules



class TelloFlightSoftware(djiTello):
    
    """
    Subclass that inherits all of the djitellopy Tello class (here called djiTello)
    also has internet and thread intializations specific to 3dChess
    Optional kwargs:
        'logs','location','map','showmap','emControl' (or 'manControl'),'video','livestream' (or 'tracking'), 'showstream', 'takepic', 'takeoffLocation'
    """
    dmToin = 10/2.54
    cmToin = 1/2.54

    
    TelloName = {'192.168.1.11':"Tello_A",   #A
                '192.168.1.12':"Tello_B",   #B
                '192.168.1.13':"Tello_C"}   #C
    TelloColor = {'192.168.1.11':(0,0,200),   #A
                '192.168.1.12':(255,0,0),   #B
                '192.168.1.13':(0,255,0)}   #C
    vs_port = {'192.168.1.11':11111,   #A
                '192.168.1.12':11112,   #B
                '192.168.1.13':11113}   #C

    


    ############################################# Movement ###############################################
        ###Not Adding. Do not Use###
    #go_xyz_speed()
    #go_xyz_speed_mid()
    #go_xyz_speed_yaw_mid()


    def _rotationMatrix_(self):
        import numpy as np
        from math import sin,cos,radians
        try:
            self.yaw = self.t.get_yaw()
        except:
            self.yaw = 0
        self.yawrad = radians(self.yaw)
        return np.array([cos(self.yawrad),-sin(self.yawrad),0,
                         sin(self.yawrad),cos(self.yawrad),0,
                         0,0,1]).reshape((3,3))

    def _newCommand_(self,bodyVector):
        self.rotationMatrix = self._rotationMatrix_()
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
        #self.yaw = self.t.get_yaw()
        self.bodyVector = np.array([self.x,0,0])

        #Apply to the commandVector
        self._newCommand_(self.bodyVector)
        
        #Apply the move distance using super class
        try:
            self.t.move_forward(self.x)
        except AttributeError:
            pass

    def move_back(self,travelDistance:float,unit:str = 'cm'):
        #Get travelDistance in proper form/unit
        self.x = travelDistance
        if unit == 'in':
            self.x /= self.cmToin
        from math import floor
        self.x = floor(self.x)
        
        #get orientation
        #self.yaw = self.t.get_yaw()
        self.bodyVector = np.array([-self.x,0,0])

        #Apply to the commandVector
        self._newCommand_(self.bodyVector)
        

        #Apply the move distance using super class
        try:
            self.t.move_back(self.x)
        except:
            pass

    def move_left(self,travelDistance:float,unit:str = 'cm'):
        #Get travelDistance in proper form/unit
        self.x = travelDistance
        if unit == 'in':
            self.x /= self.cmToin
        from math import floor
        self.x = floor(self.x)
        
        #get orientation
        #self.yaw = self.t.get_yaw()
        self.bodyVector = np.array([0,-self.x,0])

        #Apply to the commandVector
        self._newCommand_(self.bodyVector)
        
        #Apply the move distance using super class
        try:
            self.t.move_left(self.x)
        except AttributeError:
            pass
    def move_right(self,travelDistance:float,unit:str = 'cm'):
        #Get travelDistance in proper form/unit
        self.x = travelDistance
        if unit == 'in':
            self.x /= self.cmToin
        from math import floor
        self.x = floor(self.x)
        
        #get orientation
        #self.yaw = self.t.get_yaw()
        self.bodyVector = np.array([0,self.x,0])

        #Apply to the commandVector
        self._newCommand_(self.bodyVector)
        
        #Apply the move distance using super class
        try:
            self.t.move_right(self.x)
        except AttributeError:
            pass

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

        if  abs(self.curTime-self.lastRCcommandTime) > 1e-8:
            #Get change in time
            self.dt = self.curTime-self.lastRCcommandTime

            self.bV = np.array([self.lastRCcommand[1]*self.dt,self.lastRCcommand[0]*self.dt,self.lastRCcommand[2]*self.dt]).reshape((3,1))
            #self.yaw = self.t.get_yaw()
            #Apply the last RC command over the change in time
            self._newCommand_(self.bV)
            
            #reset last RC command
            self.lastRCcommand = self.rcIn
            self.lastRCcommandTime = self.curTime

            #Apply the move distance using super class
            try:
                self.t.send_rc_control(self.rcIn[0],self.rcIn[1],self.rcIn[2],self.rcIn[3])
            except AttributeError:
                pass

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
            self.waypoint.append(self.position[2][0])
        elif len(waypoint) == 3:
            self.waypoint = waypoint
        else:
            print("Error goto expected positional data with len of 2 or 3. Got something else")
            return None
        self.waypoint = np.array(self.waypoint).reshape((3,1))
        self.gotoVector =self.waypoint- self.position
        self.gotoTimeOut = time()+timeout
        #print("Going to",self.waypoint)

        self.c_count = 0
        while np.linalg.norm(self.gotoVector) > 10 and time() < self.gotoTimeOut:

            self.bodygotoVector = np.matmul(np.linalg.inv(self._rotationMatrix_()),self.gotoVector).reshape((3,1))

            for u in range(3):
                if abs(self.bodygotoVector[u][0]) <10:
                    self.bodygotoVector[u][0] = 0
            
            self.previousgotoVector = self.gotoVector
            if np.linalg.norm(self.bodygotoVector) <10:
                self.c_count += 1

                if self.c_count >10:
                    self.gotoVector = np.array([0,0,0]).reshape((3,1))
                continue

            self.c_count = 0
            self.bUV = self.bodygotoVector / np.linalg.norm(self.bodygotoVector)        #body unit vector
            
            self.send_rc_control(self.bUV[1][0]*self.velocity,self.bUV[0][0]*self.velocity,self.bUV[2][0]*self.velocity,0)
            

            sleep(0.5)   
            self.gotoVector = self.waypoint-self.position
        self.send_rc_control(0,0,0,0)
        #print("Finished Waypoint")



    def takeoff(self,*takeoffLocation:float):
        """
        Command connected tello to takeoff
        Optional:
        *takeoff location: X,Y,Z float of the takeoff location
        """
        
        #for i in range(len(takeoffLocation)):
        #    self.position[i] = takeoffLocation[i]
        #    self.IMUVector[i]= takeoffLocation[i]
        #    self.commandVector[i] = takeoffLocation[i]
        try:
            self.t.takeoff()
        except:
            pass
    def addArea(self,location,wayIndex = 0):
        """
        Add an area centered around location to waypoints at the index of wayIndex
        """
        self.vert = []
        for self.v in range(4):
            self.vert.append([location[0][0]+100*cos(self.v*pi/2+pi/4),location[1][0]+100*sin(self.v*pi/2+pi/4)])
        print(self.vert)
        self.newWay = Modules.Controls.pattern_decendingSpiral(self.vert,self.swath,self.margin)
        self.newWay.append(self.waypoints[wayIndex-1])
        for self.v in range(len(self.newWay)):
            self.waypoints.insert(wayIndex+self.v,self.newWay[self.v])
        print(self.waypoints)


    ################################## Task functions  ######################################

    def _findDistance_(self,location):
        """
        Find the shortest distance from any point in the waypoints
        """
        self.shortestPoint = 0
        self.dis = 1e8
        for self.x in self.waypoints:
            self.testDis = np.linalg.norm(self.x-location)
            if self.testDis<self.dis:
                self.shortestPoint = self.waypoints.index(self.x)
                self.dis = self.testDis
        return self.shortestPoint,self.dis

    def _taskBid_(self,Task):
         """
         will bid on the given task request
         """
         self.bid = 0

         #TODO add requirement check and create utility function
         #Temporarily just distance
         self.spi,self.dis = self._findDistance_(Task.taskLocation)

         self.bid = self.dis
         print(self.bid)

         Task.offers.append((self,self.bid))

         while len(Task.offers) < Task.maxDrones:
             sleep(1)
            
         self.o = np.array(Task.offers)
         
         if self.o[np.argmax(self.o[:,0])][0] == self:
             self.addArea(Task.taskLocation,self.spi)


    ################################## Thread functions  ######################################

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

    def _moveThroughWay_(self):
        """
        Target of movement thread. Will cycle through self.waypoints and goto the next one
        """
        
        while True:
            if len(self.waypoints) > 0:
                if self.is_flying:
                    self.goto(self.waypoints.pop(0))
                else:
                    self.takeoff(self.takeoffLocation)
                    self.goto(self.waypoints.pop(0))
            #elif np.linalg.norm(self.position-self.takeoffLocation) > 1:
            #    self.goto(self.takeoffLocation)
            #else:
            #    if self.is_flying:
            #        self.land
                #else:
            sleep(1)


    def _telloTasks_(self):
        """
        Target of tasks thread. Will check for new task and bid on it
        """
        self.tasksAnalysed = 0
        while True:
            if self.tasksAnalysed < len(cfg.task_requests):
                self.tasksAnalysed+=1
                self._taskBid_(cfg.task_requests[-1])
                


    ########################### Setup #######################################

    #def setConstraints(self,**kwargs):
        """
        Set the artificial constraints of the system
        Needs functionality
        Anything not found is assumed false
        """
        ####NOTE: Likely going to change after PDR#####
    #    for self.k in kwargs:
    #        if self.k == "TIR":
    #            self.nominal = self._squarePattern_
    #        else:
    #            self.nominal = self._linePattern_


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
        #Video
        self.haveVideo = True
        self.livestream = True
        self.showStream = True
        self.takePic = False
        #Automatic control
        self.auto = False
        self.waypoints = []

        self.sim = False

        self.takeoffLocation = np.array([0,0,0]).reshape((3,1))
        self.swath = 50
        self.margin = 5

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
            elif self.k == 'tracking':
                self.livestream = not kwargs[self.k]
            elif self.k == 'showstream':
                self.showStream = kwargs[self.k]
            elif self.k == 'takepic':
                self.takePic = kwargs[self.k]
            elif self.k == "takeoffLocation":
                self.takeoffLocation = np.array(kwargs[self.k]).reshape((3,1))
            elif self.k == "coverageArea":
                self.waypoints = Modules.Controls.pattern_decendingSpiral(kwargs[self.k],self.swath,self.margin)
            elif self.k == "auto":
                self.auto = kwargs[self.k]
            elif self.k == "sim":
                self.sim = kwargs[self.k]

        if not self.haveLogs:
            djiTello.LOGGER.setLevel(logging.WARNING)      #Setting tello output to warning only


        #TelloName
        self.name = self.TelloName[IP]
        self.color = self.TelloColor[IP]

        self.velocity = 20 #cm/s
        
        

        #self.last_rc_control_timestamp = time.time()
        self.lastRCcommandTime = time.time()        #Duplicate??

        #Command input and IMU locations
        self.commandVector = np.array([0,0,0]).reshape((3,1))        #X,Y,Z in cm
        self.IMUVector = np.array([0,0,0]).reshape((3,1))            #X,Y,Z in cm

        #Actual Position
        self.position = np.array([0,0,0]).reshape((3,1))             #X,Y,Z in cm

        self.lastRCcommand = 0,0,0,0

        
        if not self.sim:
            self.t = super()
            self.t.__init__(IP)
            self.connect()
            self.is_flying = True


        if self.haveLocation:
            #from Modules.Location import IMU
            #self.locationThread = threading.Thread(target=IMU.init,args=(self.t,),)
            self.locationThread = threading.Thread(target=self._updatePosition_)
            self.locationThread.start()

       
        

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
                 self.videoThread = threading.Thread(target = startVideo,args=(self,),kwargs=({'streamType':'Live',
                                                                                               'streamShow':self.showStream,
                                                                                               'takePic':self.takePic}),)
            else:
                self.videoThread = threading.Thread(target = startVideo,args=(self,),kwargs=({'streamType':'FT',
                                                                                               'streamShow':self.showStream,
                                                                                               'takePic':self.takePic}),)

            self.videoThread.start()

        if self.auto:
            self.taskThread = threading.Thread(target = self._telloTasks_)
            self.moveThread = threading.Thread(target = self._moveThroughWay_)
            self.taskThread.start()
            self.moveThread.start()


        #self.updateThread = threading.Thread(target=self._getTask_)
        #self.updateThread.start()
        



        
        
        














#https://beenje.github.io/blog/posts/logging-to-a-tkinter-scrolledtext-widget/
#LOOK into this for logging console outputs