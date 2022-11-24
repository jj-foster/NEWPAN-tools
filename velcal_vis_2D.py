import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import pandas as pd
import shutil
import json

def read_velcal(file):

    data=pd.read_csv(file,skiprows=2,skip_blank_lines=True,delim_whitespace=True,header=None)
    data.columns=["x","y","z","u","v","w","Cp"]
    data=data.apply(lambda x: pd.to_numeric(x, errors='coerce'))#.dropna()

    data.fillna(10000,inplace=True)
    
    data=data.reset_index()

    return data

def plot(xs,ys,z,title,contours,plane,vmin=None,vmax=None):
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

    return ax

def contours_2d(data,plane):
    
    if plane.upper()=="XZ":
        xs,ys=data["x"].to_numpy(),data["z"].to_numpy()
    elif plane.upper()=="XY":
        xs,ys=data["x"],data["y"]
    elif plane.upper()=="YZ":
        xs,ys=data["y"],data["z"]
    else:
        raise ValueError("Invalid plane.")

    axes=[]
    axes.append(plot(xs,ys,data["u"],"u",50,plane,vmin=-2,vmax=2))
    # axes.append(plot(xs,ys,data["v"],"v",50,plane,vmin=-5,vmax=5))
    # axes.append(plot(xs,ys,data["w"],"w",50,plane,vmin=-5,vmax=5))
    # axes.append(plot(xs,ys,data["Cp"],"Cp",50,plane)#,vmin=-10,vmax=1))

    return axes

def plot_geom(axes:list[plt.axes], geom_files:list):
    """
    Only works with symmetry in xy plane for now. Not general!
    """
    for geom_file in geom_files:
        with open(geom_file,'r') as f:
            geom_data=json.load(f)
        
        sym_plane=geom_data["symmetry"]
        coords=np.stack((
            geom_data["x"],
            geom_data["y"],
            geom_data["z"],
        ),axis=1)

        if sym_plane!=[]:
            n=coords.shape[0]
            coords_sym=np.zeros(coords.shape)

            for i in range(n):
                coords_sym[i,0]=coords[i,0]
                coords_sym[i,1]=-coords[i,1]
                coords_sym[i,2]=-coords[i,2]

        for ax in axes:
            ax.fill(coords[:,0],coords[:,2],color='white')
            if sym_plane!=[]:
                ax.fill(coords_sym[:,0],coords_sym[:,2],color='white')

if __name__=="__main__":  

    # proj_dir="D:\\Documents\\University\\NEWPAN VM\\VMDrive2_120122\\VMDrive2\\DataVM2\\Projects\\3_EDF\\4_EDF_qo\\"
    # proj_name="EDF"
    # vel_file0=proj_dir+proj_name+".vel1"

    # vel_file="results/EDF_qo/6.vel1"
    # shutil.copy(vel_file0,vel_file)

    vel_file="results/EDF_qo/6.vel1"

    plane="xz"

    data=read_velcal(vel_file)
    contour_axes=contours_2d(data,plane)

    plot_geom(contour_axes,["data/EDF_blockage.json","data/EDF_nacelle.json"])
    
    plt.show()