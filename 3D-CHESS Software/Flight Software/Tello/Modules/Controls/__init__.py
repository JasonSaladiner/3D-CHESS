##KeyboardControls __init__

#import KeyReader, ManualControl

__all__ = ["KeyReader","ManualControl"]


squareVert = [(0,0),(10,0),(10,10),(0,10)]


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
        t = ((x1-x3)*(y3-y4)-(y1-y3)*(x4-x4)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
        u = ((x1-x3)*(y1-y2)-(y1-y3)*(x1-x2)) / ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
    except ZeroDivisionError:
        return None
    #print(t,u)
    if t >=0 and t <= 1 and u >=0 and u <=1:
        #intersection occurs
        return (x3+u*(x4-x3),y3+u*(y4-y3))
    elif t>=0 and t <=1:
        #only in first line segment
        print("first")
        return (x1+t*(x2-x1),y1+t*(y2-y1))
    elif u >=0 and u <=1:
        #only in second line segment
        print("second")
        return (x3+u*(x4-x3),y3+u*(y4-y3))
    else:
        return None


def unitVector(p1,p2):
    from math import sqrt,pow
    norm = lambda x1,x2: sqrt(pow(x1,2)+pow(x2,2))
    xN = norm(p1[0],p2[0])
    yN = norm(p1[1],p2[1])

    try:
        x = -(p1[0]-p2[0])/xN
    except ZeroDivisionError:
        x = 0.

    try:
        y = -(p1[1]-p2[1])/yN
    except ZeroDivisionError:
        y = 0.

    return (x,y)

def pattern_decendingSpiral(verticies:list,swath=1,margin=0.1):
    """
    Give an area defined by a set of verticies, a swath, and an overlap margin, determine the waypoints necessary to view it in a decending spiral pattern
    """
    from math import sqrt,pow


    #Constants
    k = len(verticies) #starting number of bounds (usually equal to number of lines)
    effS = swath-margin     #effective swath
    diag = sqrt(2)*effS     #diagonal to effective swath corners
    
    #Starts on the outer bounds
    waypoints = verticies
    swathlines = []
    print(unitVector(waypoints[0],waypoints[1]))
    #first set
    for i in range(k-1):
        slStart = (waypoints[i][0]-effS,waypoints[i][1]+effS)
        slEnd = (waypoints[i+1][0]-effS,waypoints[i+1][1]+effS)
        
        swathlines.append((slStart,slEnd))

    print(swathlines)
    print(waypoints[k-1],waypoints[0])
    intersect = lineIntersection((waypoints[k-1],waypoints[0]),swathlines[0])
    print(intersect)

    #while True:     #should change so it doesn't get into a weird loop
        

if __name__=="__main__":
    pattern_decendingSpiral(squareVert)