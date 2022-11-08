import matplotlib.pyplot as plt
import numpy as np

def read_velcal(file):

    with open(file,'r') as f:
        lines=f.readlines()

    lines=lines[2:]

    data={
        "x":np.zeros((len(lines))),
        "y":np.zeros((len(lines))),
        "z":np.zeros((len(lines))),
        "u":np.zeros((len(lines))),
        "v":np.zeros((len(lines))),
        "w":np.zeros((len(lines))),
        "Cp":np.zeros((len(lines)))
    }

    for i,line in enumerate(lines):
        line_=line.strip().split()
        
        data["x"][i]=float(line_[0])
        data["y"][i]=float(line_[1])
        data["z"][i]=float(line_[2])
        data["u"][i]=float(line_[3])
        data["v"][i]=float(line_[4])
        data["w"][i]=float(line_[5])
        data["Cp"][i]=float(line_[6])

    return data

def plot(xs,ys,z,title,contours,vmin=None,vmax=None):
    # limit
    if vmin==None:
        vmin=min(z)
    if vmax==None:
        vmax=max(z)

    z_=[]
    for i,_ in enumerate(xs):
        if z[i]<vmin:
            z_.append(vmin)
        elif z[i]>vmax:
            z_.append(vmax)
        else:
            z_.append(z[i])

    # plot
    fig,ax=plt.subplots()
    
    cs=ax.tricontourf(xs,ys,z_,contours,cmap='jet')
    cbar=fig.colorbar(cs,label=title)

    ax.set_aspect('equal')
    ax.set_title(title)
    ax.set_xlabel(plane[0])
    ax.set_ylabel(plane[1])

    return plt

def contours_2d(data,plane):
    
    if plane.upper()=="XZ":
        xs,ys=data["x"],data["z"]
    elif plane.upper()=="XY":
        xs,ys=data["x"],data["y"]
    elif plane.upper()=="YZ":
        xs,ys=data["y"],data["z"]
    else:
        raise ValueError("Invalid plane.")

    fig1=plot(xs,ys,data["u"],"u",50,vmin=-2,vmax=2)
    # fig2=plot(xs,ys,data["v"],"v",50,vmin=-5,vmax=5)
    # fig3=plot(xs,ys,data["w"],"w",50,vmin=-5,vmax=5)
    fig4=plot(xs,ys,data["Cp"],"Cp",50,vmin=-3,vmax=5)

    plt.show()

if __name__=="__main__":   

    data_file="data/EDF_wing/CT0.2_CQ0.0_w1.vel1"
    plane="xz"

    data=read_velcal(data_file)
    contours_2d(data,plane)
