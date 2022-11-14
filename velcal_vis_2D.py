import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shutil

def read_velcal(file):

    data=pd.read_csv(file,skiprows=2,skip_blank_lines=True,delim_whitespace=True,header=None)
    data.columns=["x","y","z","u","v","w","Cp"]
    data=data.apply(lambda x: pd.to_numeric(x, errors='coerce'))#.dropna()

    data.fillna(10000,inplace=True)
    
    data=data.reset_index()

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
        xs,ys=data["x"].to_numpy(),data["z"].to_numpy()
    elif plane.upper()=="XY":
        xs,ys=data["x"],data["y"]
    elif plane.upper()=="YZ":
        xs,ys=data["y"],data["z"]
    else:
        raise ValueError("Invalid plane.")

    fig1=plot(xs,ys,data["u"],"u",50,vmin=-3,vmax=3)
    # fig2=plot(xs,ys,data["v"],"v",50,vmin=-5,vmax=5)
    # fig3=plot(xs,ys,data["w"],"w",50,vmin=-5,vmax=5)
    fig4=plot(xs,ys,data["Cp"],"Cp",50,vmin=-2,vmax=5)

    plt.show()

if __name__=="__main__":   

    # proj_dir="D:\\Documents\\University\\NEWPAN VM\\VMDrive2_120122\\VMDrive2\\DataVM2\\Projects\\3_EDF\\3_EDFActuatorDisk_wake\\"
    # proj_name="EDF"
    # vel_file0=proj_dir+proj_name+".vel1"

    # vel_file="data/EDF_actuator/EDF_CT1.vel1"
    # shutil.copy(vel_file0,vel_file)

    vel_file="data/EDF_actuator/EDF_CT1.vel1"

    plane="xz"

    data=read_velcal(vel_file)
    contours_2d(data,plane)
