import matplotlib.pyplot as plt
import numpy as np


def plotWithAnnotate(results):
    x = results[:,1]
    y = results[:,2]
    names = []
    c = []
    for i in range(len(results)):
        #print(results[i])
        names.append("(%i,%i,%i)"%(results[i][1],results[i][2],results[i][3]))
        #c.append(results[i][0][0])

    #norm = plt.Normalize(1,4)
    cmap = plt.cm.RdYlGn

    fig,ax = plt.subplots()
    sc = plt.scatter(x,y,cmap=cmap)

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


results = (readCSV())
print(len(results))
plotWithAnnotate(results)