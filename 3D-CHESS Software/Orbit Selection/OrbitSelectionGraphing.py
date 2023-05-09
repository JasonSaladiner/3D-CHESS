import matplotlib.pyplot as plt
import numpy as np


def plotWithAnnotate(results):
    x = results[:,4]
    y = results[:,5]
    alt = results[:,0]
    sats = results[:,1]
    planes = results[:,2]
    #f = results[:,3]
    names = []
    for i in range(len(results)):
        names.append("%ikm:(%i,%i,%i)"%(alt[i],sats[i],planes[i],1))
    
    c = planes
    norm = plt.Normalize(np.amin(c),np.amax(c))
    cmap = plt.cm.PuOr_r

    fig,ax = plt.subplots()
    sc = plt.scatter(x,y,c=c,cmap=cmap,norm=norm)
    cb = plt.colorbar(orientation='vertical')
    cb.set_label(label="Planes",size=30)
    cb.ax.tick_params(labelsize=20)
    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    
    
    def perm_annot(ind):
        #pos = []
        for i in range(len(ind)):
            annot = ax.annotate("", xy=(0,0), xytext=(-40,-40),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
            pos = sc.get_offsets()[ind[i]]
            annot.xy = pos
            #text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
            #                      " ".join([names[n] for n in ind["ind"]]))
            text = "{}".format(" ".join([names[ind[i]]]))
            annot.set_text(text)
            #annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
            annot.get_bbox_patch().set_alpha(0.4)
            annot.set_visible(True)

    def update_annot(ind):
    
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        #text = "{}, {}".format(" ".join(list(map(str,ind["ind"]))), 
        #                      " ".join([names[n] for n in ind["ind"]]))
        text = "{}".format(" ".join([names[n] for n in ind["ind"]]))
        annot.set_text(text)
        #annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        annot.get_bbox_patch().set_alpha(0.4)
    
    allind = [48,26,13,774]

    perm_annot(allind)
    fig.canvas.draw_idle()
        
    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            print(ind)
            #for n in ind["ind"]:
            #    allind["ind"].append(n)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    #annot.set_visible(False)
                    fig.canvas.draw_idle()

    #fig.canvas.mpl_connect("motion_notify_event", hover)
    fig.canvas.mpl_connect("button_press_event",hover)
    
    
    plt.suptitle("Cost (USD) vs Revisit Time (Hrs) for different constellations",size=40)
    plt.xlabel("Revist Time (hr)",size=30)
    plt.ylabel("Cost (USD)",size=30)
    plt.show()

def readCSV():
    data = []
    f = open("results.csv",'r')
    lines = f.readlines()
    for line in lines:
        row = line.strip('\n').split(',')
        trow = []
        for i in row:
            trow.append(float(i))
        data.append(trow)

    return np.array(data)



def SSOinclination(alt:float) -> float:
    """
    SSO inclination will return the required Sun-Synchronous Inclination (degrees) as a functino of altitude (in KM) using J2 pertubation
    Inputs:
        -Altitude in KM
    Output:
        -Inclination in degrees
    """
    from math import pi,sqrt,acos
    Re = 6378.1     #Radius of Earth in KM
    mu = 3.986e14   #Mu of earth in m^3/s^2

    J2 = 1.08262668e-3
    omegaDot = 2*pi/365/86400

    a = (alt+Re)*1000
    n = sqrt(mu/pow(a,3))
    return acos(-2/3 * omegaDot/n/J2 * pow(a/Re/1000,2))*180/pi
#print(SSOinclination(500))
results = (readCSV())

AltFront = [[500,10,5],[500,7,7],[500,5,5],[750,3,3]]
ci = []
Front = AltFront
for point in Front:
    Awhere = np.argwhere(results[:,0]==point[0])
    Swhere = np.argwhere(results[:,1]==point[1])
    Pwhere = np.argwhere(results[:,2]==point[2])
    ascom = []
    aspcom = []
    for a in Awhere:
        for s in Swhere:
            if a ==s:
                ascom.append(a)
    for c in ascom:
        for p in Pwhere:
            if c==p:
                aspcom.append(c)
    ci.append(aspcom)


print(ci)

plotWithAnnotate(results)