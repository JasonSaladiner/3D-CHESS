##KeyboardControls __init__

#import KeyReader, ManualControl

__all__ = ["KeyReader","ManualControl"]

from time import sleep
def lineIntersection(L1,L2):
    x1 = L1[0][0]
    y1 = L1[0][1]
    x2 = L1[1][0]
    y2 = L1[1][1]

    x3 = L2[0][0]
    y3 = L2[0][1]
    x4 = L2[1][0]
    y4 = L2[1][1]

    try: 
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x3-x4)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        u = ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    except ZeroDivisionError:
        #print("Zero")
        return None
    #print(t,u)
    if (abs(t) <1e-12 or t>0) and t <= 1 and (abs(u) <1e-12 or u>0) and u <=1:
        #intersection occurs
        return (x3+u*(x4-x3),y3+u*(y4-y3))
    elif (abs(t) <1e-12 or t>0) and t <=1:
        #only in first line segment
        #print("first")
        return x1+t*(x2-x1),y1+t*(y2-y1)
    elif (abs(u) <1e-12 or u>0) and u <=1:
        #only in second line segment
        #print("second")
        #return (x3+u*(x4-x3),y3+u*(y4-y3))
        return None
    else:
        #print("No inter")
        return None


def unitVector(p1,p2):
    from math import sqrt,pow
    import numpy as np
    v = np.array([p2[0]-p1[0],p2[1]-p1[1]])
    vn = np.linalg.norm(v)
    uv = v/vn
   
    x = uv[0]
    y = uv[1]
    return x,y

def swathUV(vector:tuple,angle=45):
    import numpy as np
    from math import radians,cos,sin
    diagAngle = radians(angle)


    rotation = np.array([cos(diagAngle),-sin(diagAngle),sin(diagAngle),cos(diagAngle)]).reshape((2,2))
    newVect = np.matmul(np.array(vector),rotation)

    return (newVect[0],newVect[1])


def pattern_decendingSpiral(verticies:list,swath:float=1,margin:float=0.1) -> list:
    """
    Given a list of verticies, pattern_decendingSpiral will generate a set of points needed to have the entire area covered
    Assumptions:
        -Right hand turns only (<180 degrees)
        -Clockwise travel
        -Not weird shapes (only "garunteed" to work on simple rectangular,triangular,etc shapes)
        -No signifigantly accute areas (may result in ending too soon and not covering area)
    Inputs
        list Vertices: a list of tuples with the verticies in a clockwise order
        float swath: the half swath (i.e. the furtherst the drone can see to the left)
        float margin: how much the swaths should overlap (to account for error)
    Return:
        list : an ordered list of waypoints
    
    Give an area defined by a set of verticies, a swath, and an overlap margin, determine the waypoints necessary to view it in a decending spiral pattern
    Currently supports regular rectagular or triangular shapes. Requires only right hand turns of < 180 degrees. Extremly accute angles may result in  unseen space. Further testing and logic required
    Primarily use only for square/rectangle space
    """
    from math import sqrt,pow,cos,sin,pi,radians,floor
    import numpy as np

    #Constants
    k = len(verticies) #starting number of bounds (usually equal to number of lines)
    effS = swath-margin     #effective swath
    diag = sqrt(2)*effS     #diagonal to effective swath corners
    

    #overlapp check
    if k ==3:
        check = (-2,-3)
    elif k % 2 == 0:
        check = (-2,-int((2+k/2)))
    else:
        check = (-3,-int((floor(k/2)+3)))

    diagAngle = radians(-45)
    rotation = np.array([cos(diagAngle),-sin(diagAngle),sin(diagAngle),cos(diagAngle)]).reshape((2,2))
    
    pl = []

    #Starts on the outer bounds
    waypoints = verticies
    swathlines = []
    
    #print(unitVector(waypoints[1],waypoints[2]))
    #print(np.matmul(np.array(unitVector(waypoints[1],waypoints[2])),rotation))
    #print(swathUV(unitVector(waypoints[1],waypoints[2])))
    
    #first set
    for i in range(k-1):
        
        UV = unitVector(waypoints[i],waypoints[i+1])
        sUV = swathUV(UV,-45)
        seUV = swathUV(UV,-135)

        slStart = (waypoints[i][0]+effS*sUV[0],waypoints[i][1]+effS*sUV[1])
        slEnd = (waypoints[i+1][0]+effS*seUV[0],waypoints[i+1][1]+effS*seUV[1])
        
        swathlines.append((slStart,slEnd))

    t=0
    while t<50:     #should change so it doesn't get into a weird loop
        #Unit vector (except is for the first in the loop)
        try:
            UV = unitVector(waypoints[-k-1],waypoints[-k])
        except:
            UV = unitVector(waypoints[-1],waypoints[-k])
        sUV = swathUV(UV,-45)

        seUV = swathUV(UV,-135)
        osUV = swathUV(UV,45)
        #check if start point and direction will overlap with previous runs (e.g. at end)
        pushline = (waypoints[-1][0]+effS*sUV[0],waypoints[-1][1]+effS*sUV[1]),(waypoints[-1][0]+effS*osUV[0],waypoints[-1][1]+effS*osUV[1])
        pl.append(pushline)
        if t>1:
            if lineIntersection(pushline,swathlines[check[0]]) != None and lineIntersection(pushline,swathlines[check[1]]) != None:
                #print("Overlap")
                break

        #unit swathline
        slStart = (waypoints[-1][0]+effS*sUV[0],waypoints[-1][1]+effS*sUV[1])
        slEnd = (slStart[0]+UV[0],slStart[1]+UV[1])

        #intersect (on the previous sl)
        for i in range(1-k,0):
            intersect = lineIntersection(swathlines[i],(slStart,slEnd))
            if intersect != None:
                break
        #if occurs add
        if intersect != None:
            swathlines.append((slStart,intersect))
            waypoints.append((intersect[0]-effS*sUV[0],intersect[1]-effS*sUV[1]))
        else:
            #this will maybe become fall away curves?
            break
        t+=1
     
        

    return waypoints
    ##Visualizing and testing stuff. Ignore
    #import matplotlib.pyplot as plt
    ##zw =zip(*waypoints)
    ##print(len(waypoints))
    ##plt.scatter(*zip(zw))
    ##plt.show()
    #a = 1
    #for line in swathlines:
    #    p1 = line[0]
    #    p2 = line[1]
    #    xs = np.linspace(p1[0],p2[0])
    #    ys = np.linspace(p1[1],p2[1])
    #    plt.plot(ys,xs,label=a)
    #    a+=1
    #plt.legend()
    #plt.show()
    #a=1
    #for line in pl:
    #    p1 = line[0]
    #    p2 = line[1]
    #    xs = np.linspace(p1[0],p2[0])
    #    ys = np.linspace(p1[1],p2[1])
    #    plt.plot(xs,ys,label=a)
    #    a+=1
    #plt.legend()
    #plt.show()



def _squarePattern_(self):
    """
    NOTE: Temp pattern for PDR
    """
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

def _linePattern_(self):
    """
    NOTE: Temp Pattern For PDR
    """
    sleep(3)
    self.takeoff()
    self.move_forward(100)
    sleep(2)
    self.move_back(100)
    self.land()
