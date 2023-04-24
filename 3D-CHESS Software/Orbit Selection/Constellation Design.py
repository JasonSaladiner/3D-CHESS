"""
Code will implement STK API to select an optimal walker constellation and generate visuals
"""

#Imports
#STK Stuff
from shutil import ReadError
from string import octdigits
from agi.stk12.stkengine import STKEngine
from agi.stk12.stkdesktop import STKDesktop
from agi.stk12.stkobjects import *
from agi.stk12.stkutil import *
#Basic Stuff
from math import *
import numpy as np
import matplotlib.pyplot as plt

from time import time
global stk
global stkRoot
global scenario


#Global Parameters
Re = 6378.1     #Radius of Earth in KM
mu = 3.986e14   #Mu of earth in m^3/s^2


def SSOinclination(alt:float) -> float:
    """
    SSO inclination will return the required Sun-Synchronous Inclination (degrees) as a functino of altitude (in KM) using J2 pertubation
    Inputs:
        -Altitude in KM
    Output:
        -Inclination in degrees
    """
    J2 = 1.08262668e-3
    omegaDot = 2*pi/365/86400

    a = (alt+Re)*1000
    n = sqrt(mu/pow(a,3))
    return acos(-2/3 * omegaDot/n/J2 * pow(a/Re/1000,2))*180/pi

def OEfromWalker(totalSats:int,planes:int,relativeSpacing:int)->list:
    """
    OEfromWalker will create a list of lists of the non-constant orbital elements for each satellite in a walker constellation.
    The satellites are assumed to be in a ciruclar orbits and equally space in true anomaly and RAAN
    Inputs:
        int totalSats = t; total number of satellites
        int planes = p; number of equally spaced planes
        int relativeSpacing = f; relative spacing between satellites in adjacent place      ##float or int???
    Output:
        list of lists of the form:
        [[RAAN,trueAnom],[<sat 2>],...,[<sat n>]]
    """

    satsPerPlane = floor(totalSats/planes)
    satLocations = []
    for i in range(planes):
        RAAN = 360/planes*i
        for j in range(satsPerPlane):
            trueAnom = 360/satsPerPlane*j
            satLocations.append([RAAN,trueAnom])
        
    return satLocations


def findMaxRT_STK(satelliteLocations:list,coverageResolution:float = 2000):
    """
    Run STK and report the maximum revisit time
    Input:
        list of list of satellite location OE of the form:
            [[a,e,i,argOfPer,RAAN,trueAnom],[<sat2>],...,[<sat n>]]
        float coverageResolution  = the distance in KM between points in the global coverage definiton (default 2000km)
        tuple scenarioTime = two strings of the scenario time bounds in UTC/DMYHMS
    Returns:
        float revisit time in hours
    """

    global stk
    global stkRoot
    global scenario

    #Coverage Definition
    coverageDef = scenario.Children.New(AgESTKObjectType.eCoverageDefinition, "CoverageDefinition")

    ##Set bounds
    grid = coverageDef.Grid
    grid.BoundsType = AgECvBounds.eBoundsGlobal
    grid.ResolutionType = AgECvResolution.eResolutionDistance
    grid.Resolution.Distance = coverageResolution

    const = scenario.Children.New(AgESTKObjectType.eConstellation, "SatConstellation")

    stkRoot.BeginUpdate()

    for j in range(len(satelliteLocations)):


        #insert Sat
        sat = scenario.Children.New(AgESTKObjectType.eSatellite,f"Sat{j}")

        #Propagator
        sat.SetPropagatorType(AgEVePropagatorType.ePropagatorJ4Perturbation)

        kep = sat.Propagator.InitialState.Representation.ConvertTo(AgEOrbitStateType.eOrbitStateClassical)

        kep.SizeShapeType = AgEClassicalSizeShape.eSizeShapeSemimajorAxis
        kep.Orientation.AscNodeType = AgEOrientationAscNode.eAscNodeRAAN
        kep.LocationType = AgEClassicalLocation.eLocationTrueAnomaly

        kep.SizeShape.SemiMajorAxis = satelliteLocations[j][0]
        kep.SizeShape.Eccentricity = satelliteLocations[j][1]
        kep.Orientation.Inclination = satelliteLocations[j][2]
        kep.Orientation.ArgOfPerigee = satelliteLocations[j][3]
        kep.Orientation.AscNode.Value = satelliteLocations[j][4]
        kep.Location.Value = satelliteLocations[j][5]

        ##Sensor
        sensor = sat.Children.New(AgESTKObjectType.eSensor,f"Sensor{j}")
        sensor.CommonTasks.SetPatternRectangular(20,50)
        
        ###These are for light constraints but shouldn't be necessary anymore
        #acon = sensor.AccessConstraints
        #light = acon.AddConstraint(AgEAccessConstraints.eCstrLighting)
        #light.Condition = AgECnstrLighting.eDirectSun

        sat.Propagator.InitialState.Representation.Assign(kep)
        sat.Propagator.Propagate()

        
        const.Objects.AddObject(sat)  

    stkRoot.EndUpdate()

    coverageDef.AssetList.Add("Constellation/SatConstellation")
    #comput the access and create FOM-Maximum Revisit Time
    chain = scenario.Children.New(AgESTKObjectType.eChain,"Chain")
    chain.Objects.AddObject(const)
    
    chain.ComputeAccess()
    coverageDef.ComputeAccesses()

    fom = coverageDef.Children.New(AgESTKObjectType.eFigureOfMerit,"FigureOfMerit")
    fom.SetDefinitionType(AgEFmDefinitionType.eFmRevisitTime)
    fom.Definition.SetComputeType(AgEFmCompute.eMaximum)

    fomDataProvider = fom.DataProviders.GetDataPrvFixedFromPath("Overall Value")
    fomResults = fomDataProvider.Exec()

    maximumRT =  (fomResults.DataSets.GetDataSetByName("Maximum").GetValues()[0]/3600)
    
    #unload all of the satellites
    for j in scenario.Children:
        j.Unload()

    return maximumRT




def plotWithAnnotate(results):
    x = results[:,1]
    y = results[:,2]
    names = []
    for i in range(len(results)):
        names.append("%ikm:(%i,%i,%i)"%(results[i][0][0],results[i][0][1],results[i][0][2],results[i][0][3]))
    #c = np.random.randint(1,5,size=15)

    #norm = plt.Normalize(1,4)
    #cmap = plt.cm.RdYlGn

    fig,ax = plt.subplots()
    sc = plt.scatter(x,y)

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
    
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        #text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
        #                      " ".join([names[n] for n in ind["ind"]]))
        text = "{}".format(" ".join([names[n] for n in ind["ind"]]))
        annot.set_text(text)
        #annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        annot.get_bbox_patch().set_alpha(0.4)
    

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)


    plt.title("Cost (USD) vs Revist Time (Hrs) for different ")
    plt.xlabel("Revist Time (hr)")
    plt.ylabel("Cost (USD)")
    plt.show()

def csvOut(results):
    f = open("results.csv","w")
    for i in range(len(results)):
        lab = results[i][0]
        rt = results[i][1]
        usd = results[i][2]
        c =","
        s = str(lab[0])+c+str(lab[1])+c+str(lab[2])+c+str(lab[3])+c+str(rt)+c+str(usd)+"\n"
        f.write(s)
    f.close()


def constellationTradeStudy():
    """
    Perform the trade study to select the walker consteltaion
    """
    #start/finish walker constellations
    o = np.array([2,1,1])
    f = np.array([20,10,1])
    iteration = 1
    maxIterations = (900-500)/50*(np.prod(f-o+np.array([1,1,1])))

    #Basic orbital parameters
    #a = Re + 700            #Semimajor Axis
    e = 0                   #eccentricity
    #inc = SSOinclination(700) #inclination
    w = 0                   #argOfPerigee (doesn't really exist)

    satUSD = lambda n,alt:n* (0.00000000271436403509*alt**3 - 0.00000397319078947367*alt**2 + 0.00231994517543880000*alt - 0.16038157894742600000)


    results = []

    averageTime = 0.
    

    #Number of satellites
    for l in range(500,905,50):
        a = Re+l
        inc = SSOinclination(l)
        for i in range(o[0],f[0]+1):
        
            #Number of planes
            for j in range(o[1],i+1):
                if j > f[1]:
                    break
            
                currentConst = []
                #Relative spacing
                for k in range(o[2],j+1):
                    if k > f[2]:
                        break
                    print("Start ",iteration,"of %i: %i km (%i,%i,%i)"%(maxIterations,l,i,j,k))
                    istart = time()
                    walkerOEs = OEfromWalker(i,j,k)
                    for sat in walkerOEs:
                        currentConst.append([a,e,inc,w,sat[0],sat[1]])

                    RT = findMaxRT_STK(currentConst,500)
                    results.append([[l,i,j,k],RT,satUSD(i,l)])
                    
                    ifin = time()
                    tookTime = (ifin-istart)/60
                    averageTime = (averageTime *(iteration-1) + tookTime)/iteration
                    iteration+=1
                    print("Finished. Took:",tookTime,"Estimated Time remaining (min):",averageTime*(maxIterations-iteration))
                    
    results = np.array(results)
    try:
        print(results)
    except:
        pass
    try:    
        csvOut(results)
    except:
        pass
    try:
        plotWithAnnotate(results)
    except:
        pass

if __name__=="__main__":

    startSTK = True

    if startSTK:
        stk = STKEngine.StartApplication(noGraphics=True)
        stkRoot = stk.NewObjectRoot()

        #Create Scenario
        stkRoot.NewScenario("ConstellationDesign")
        scenario = stkRoot.CurrentScenario

        #Set Time
        scenario.SetTimePeriod("1 Nov 2022 16:00:00","7 Nov 2022 16:00:00")

    ###############################
    #Actual Code#
    constellationTradeStudy()
    #print(SSOinclination(700))


    ###############################
    #shutdown STK
    try:
        stkRoot.CloseScenario()
        stk.ShutDown()
    except:
        pass