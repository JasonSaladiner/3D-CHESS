from sqlite3 import connect
import Modules._config_ as cfg
from time import sleep
import numpy as np
from math import pi, sin, cos, atan2, sqrt, floor
from djitellopy import Tello
import numpy as np


def writeLog(f,line):
    
    for i in range(0,len(line)-1):
        f.write(str(line[i])+",")
    f.write(str(line[len(line)-1])+'\n')
    

def directRTH(ConnectedTello):
    """
    WIP and may be deleted in favor of go_nXYZ_direct
    """
    yaw = ConnectedTello.get_yaw()*pi/180

    orientationMatrix = np.array([cos(yaw),sin(yaw),0,-sin(yaw),cos(yaw),0,0,0,1]).reshape((3,3))
    absoluteCart = np.array([cfg.xPos,cfg.yPos,cfg.zPos]).reshape((3,1))
    
    relativeCart = np.matmul(np.linalg.inv(orientationMatrix),absoluteCart)

    rotationAngle = atan2(relativeCart[1],relativeCart[0])
    distance = sqrt(relativeCart[0]**2 + relativeCart[1]**2)

    ConnectedTello.rotate_counter_clockwise(floor(rotationAngle*180/pi))

    velocity = 30 #cm/s
    time = distance*10/velocity

    ConnectedTello.send_rc_control(0,velocity,0,0)
    sleep(time)
    ConnectedTello.send_rc_control(0,0,0,0)


def go_nXYZ_P(ConnectedTello, X: float,Y: float,Z:float = cfg.zPos,velocity:int = 20):
    relativeO = [X-cfg.xPos,Y-cfg.yPos,Z-cfg.zPos]
    relative = relativeO
    #idealTime = np.magnitude(relative)/velocity
    while np.linalg.norm(relative) > 2:
        
        angle = floor(atan2(relative[1],relative[0])*180/pi)
        relAngle = ConnectedTello.get_yaw()-angle
        print("relative Angle: ", relAngle)
        if abs(relAngle)>=360:
            relAngle = relAngle*(1-360/abs(relAngle))
        if abs(relAngle)>2:
            ConnectedTello.rotate_counter_clockwise(relAngle)

        if relative[2]>.5:
            vertV = velocity
        else:
            vertV = 0
        ConnectedTello.send_rc_control(0,velocity,vertV,0)
        sleep(.5)
        
        relative = [X-cfg.xPos,Y-cfg.yPos,Z-cfg.zPos]
        if np.linalg.norm(relative) > np.linalg.norm(relativeO):
            break
        else:
            relativeO = relative
        print("Relative location:", relative)
    ConnectedTello.send_rc_control(0,0,0,0)

def go_nXYZ_direct(ConnectedTello,X: int,Y: int,Z:int=floor(cfg.zPos), velocity:int = 30):
    """
    go_nXYZ_direct draws a straight line from ConnectedTello to the (X,Y,Z) location, rotates tello towards it, and drives straight towards it at velocity
    Inputs:
        ConnectedTello:Tello = the connected tello
        X:int = integer of desired x position in inertial coordinates
        Y:int = integer of desired y position in inertial coordinates  
        Z:int = integer of desired z position in inertial coordinates
        velocity = integer of velocity to fly at (cm/s)
    :NOTES:
        X,Y,Z mark locations in decimeters
        has a predicted accuracy of around 2 decimeters
    """
    Z = floor(Z)
    
    ####This block of code may be able to be deleted####
    #get current yaw
    #yaw = ConnectedTello.get_yaw()*pi/180

    #change absolute to relative 
    #orientationMatrix = np.array([cos(yaw),sin(yaw),0,-sin(yaw),cos(yaw),0,0,0,1]).reshape((3,3))
    #absoluteCart = np.array([cfg.xPos,cfg.yPos,cfg.zPos]).reshape((3,1))
    
    #relativeCart = np.matmul(np.linalg.inv(orientationMatrix),absoluteCart)
    ####

    #Get relative position vector
    relativePositionVector = np.array([X,Y,Z]) - np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    print("relativePosition", relativePositionVector)

    #Find necessary delta Yaw and ground distance
    rotationAngle = floor(atan2(relativePositionVector[1],relativePositionVector[0])*180/pi)
    distance = sqrt(relativePositionVector[0]**2 + relativePositionVector[1]**2)
    print(rotationAngle,distance)
    
    #Apply rotation
    ConnectedTello.rotate_counter_clockwise(rotationAngle)

    #Find time to complete movement and the speed to go up/down
    time = distance*10/velocity
    heightVelocity = relativePositionVector[2]*10/time
    print(time)
    #Fly the distance
    ConnectedTello.send_rc_control(0,velocity,floor(heightVelocity),0)
    sleep(time)
    #Stop
    ConnectedTello.send_rc_control(0,0,0,0)
    



xLineWaypoints = [['takeoff'],
                   #[24,63,0,0],
                   #['wait',5],
                   [75,63,0,0],
                   ['wait',5],
                   [126,63,0,180],
                   ['wait',5],
                   [75,63,0,0],
                   ['wait',5],
                   [24,63,0,0],
                   ['wait',5],
                   ['land']]

simpleSquarePoints  =[['takeoff'],
                [24,94.5,0,0],
                ['wait',5],
                [126,94.5,0,0],
                ['wait',5],
                [126,24,0,0],
                ['wait',5],
                [24,63,0,0],
                ['wait',5],
                ['land']]
                
simpleDiamondPoints = [['takeoff'],
                 [7,8,0,0],
                 ['wait',5],
                 [10,4,0,0],
                 ['wait',5],
                 [7,0,0,0],
                 ['wait',5],
                 [4,4,0,0],
                 ['wait',5],
                 ['land']]

def move_to_waypoints(ConnectedTello,waypoints:list):
    """
    Move through a list of waypoints given in inertial X,Y,Z, yaw
    """
    
    goto = go_nXYZ_P
    tello = ConnectedTello
    cfg.xPos,cfg.yPos = 24,63
    for way in waypoints:
        try:
            goto(tello,way[0],way[1],cfg.zPos)
            if abs(tello.get_yaw()-way[3])>1:
                tello.rotate_counter_clockwise(floor(abs(tello.get_yaw()-way[3])))
        except:
            if way[0].lower() == "takeoff":
                tello.takeoff()
            elif way[0].lower() == "land":
                tello.land()
            elif way[0].lower() == "wait":
                sleep(way[1])
            else:
                print("Unregonized Command")
                break
    #Good for the testing I have now. May wish to remove in the future but improves safety            
    if tello.is_flying:
        tello.land()



def lineTest(ConnectedTello,direction):
    lr,fb,down,yaw = 0,0,0,0
    direct = {"f":fb,"b":fb,"l":lr,"r":lr}
    velocity = 15
    if direction =="b" or direction =="l":
        velocity *= -1
    direct[direction] = velocity
    fb = 15
    ConnectedTello.takeoff()
    cfg.xPos = 24
    cfg.yPos = 63

    smallTime = 5

    f = open('PositionLog.txt','a')

    #Simple line pattern
    pos0 = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    ConnectedTello.send_rc_control(lr,fb,down,yaw)
    sleep(smallTime)
    ConnectedTello.send_rc_control(0,0,0,0)
    expected = pos0 + smallTime*velocity*cfg.dmToin/10
    imuOut = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    res = abs(expected-imuOut)

    log = [pos0[0],pos0[1],cfg.xPos,cfg.yPos,expected[0],expected[1],res[0],res[1]]
    writeLog(f,log)

    print()
    print("Start:",pos0,"\nExpected:",expected,"\nIMU  Output:",imuOut,"\nResidual (IMU,Expected):",res)
    print()
    sleep(5)

    pos0 = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    ConnectedTello.send_rc_control(lr,fb,down,yaw)
    sleep(smallTime)
    ConnectedTello.send_rc_control(0,0,0,0)
    expected = pos0 + smallTime*velocity*cfg.dmToin/10
    imuOut = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    res = abs(expected-imuOut)

    log = [pos0[0],pos0[1],cfg.xPos,cfg.yPos,expected[0],expected[1],res[0],res[1]]
    writeLog(f,log)


    print()
    print("Start:",pos0,"\nExpected:",expected,"\nIMU  Output:",imuOut,"\nResidual (IMU,Expected):",res)
    print()
    sleep(5)

    pos0 = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    ConnectedTello.send_rc_control(lr,fb,down,yaw)
    sleep(smallTime)
    ConnectedTello.send_rc_control(0,0,0,0)
    expected = pos0 + smallTime*velocity*cfg.dmToin/10
    imuOut = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    res = abs(expected-imuOut)

    log = [pos0[0],pos0[1],cfg.xPos,cfg.yPos,expected[0],expected[1],res[0],res[1]]
    writeLog(f,log)


    print()
    print("Start:",pos0,"\nExpected:",expected,"\nIMU  Output:",imuOut,"\nResidual (IMU,Expected):",res)
    print()
    sleep(5)

    pos0 = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    ConnectedTello.send_rc_control(lr,fb,down,yaw)
    sleep(smallTime)
    ConnectedTello.send_rc_control(0,0,0,0)
    expected = pos0 + smallTime*velocity*cfg.dmToin/10
    imuOut = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    res = abs(expected-imuOut)

    log = [pos0[0],pos0[1],cfg.xPos,cfg.yPos,expected[0],expected[1],res[0],res[1]]
    writeLog(f,log)


    print()
    print("Start:",pos0,"\nExpected:",expected,"\nIMU  Output:",imuOut,"\nResidual (IMU,Expected):",res)
    print()
    sleep(5)

    ##Return
    print()
    print("=================Return==================")
    print()
    print()
    ConnectedTello.rotate_clockwise(180)

    pos0 = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    ConnectedTello.send_rc_control(lr,fb,down,yaw)
    sleep(2*smallTime)
    ConnectedTello.send_rc_control(0,0,0,0)
    expected = pos0 - smallTime*velocity*cfg.dmToin/10
    imuOut = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    res = abs(expected-imuOut)

    log = [pos0[0],pos0[1],cfg.xPos,cfg.yPos,expected[0],expected[1],res[0],res[1]]
    writeLog(f,log)


    print()
    print("Start:",pos0,"\nExpected:",expected,"\nIMU  Output:",imuOut,"\nResidual (IMU,Expected):",res)
    print()
    sleep(5)

    pos0 = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    ConnectedTello.send_rc_control(lr,fb,down,yaw)
    sleep(2*smallTime)
    ConnectedTello.send_rc_control(0,0,0,0)
    expected = pos0 - smallTime*velocity*cfg.dmToin/10
    imuOut = np.array([cfg.xPos,cfg.yPos,cfg.zPos])
    res = abs(expected-imuOut)

    log = [pos0[0],pos0[1],cfg.xPos,cfg.yPos,expected[0],expected[1],res[0],res[1]]
    writeLog(f,log)


    print()
    print("Start:",pos0,"\nExpected:",expected,"\nIMU  Output:",imuOut,"\nResidual (IMU,Expected):",res)
    print()
    sleep(5)


    ConnectedTello.land()


    f.close()