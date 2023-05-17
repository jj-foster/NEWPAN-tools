import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import ticker
import numpy as np
import pandas as pd
import shutil
import json

plt.rcParams["font.family"]="Arial"
plt.rcParams["mathtext.fontset"]="cm"
plt.rcParams["font.size"]=11

def read_velcal(file:str) -> pd.DataFrame:

    data=pd.read_csv(
        file,skiprows=2,skip_blank_lines=True,delim_whitespace=True,header=None
    )
    data.columns=["x","y","z","u","v","w","Cp"]
    data["V"] = np.sqrt(data["u"]**2 + data["v"]**2 + data["w"]**2)

    #data=data.apply(lambda x: pd.to_numeric(x, errors='coerce'))#.dropna()

    #data.fillna(10000,inplace=True)
    
    #data=data.reset_index()

    return data

def pcolourmesh(ax,x,y,z,cmap,centered:bool=True, at:float=1):
    vmin = min(z)
    vmax = max(z)

    df = pd.DataFrame(dict(x=x,y=y,z=z))
    xcol,ycol,zcol = "x","y","z"
    df = df.sort_values(by = [xcol, ycol])
    xvals = df[xcol].unique()
    yvals = df[ycol].unique()
    zvals = df[zcol].values.reshape(len(xvals), len(yvals)).T

    # plot

    if centered:
        cs=ax.pcolormesh(
            xvals,yvals,zvals,cmap=cmap, norm=colors.CenteredNorm(vcenter=at)
        )
    else:
        levels_ = ticker.MaxNLocator(nbins=50).tick_values(z.min(),z.max())
        cmap = plt.get_cmap(cmap)
        # bounds = np.linspace(vmin,vmax,20)
        norm = colors.BoundaryNorm(levels_, ncolors = cmap.N, clip = True)

        cs=ax.pcolormesh(
            xvals,yvals,zvals,cmap=cmap, norm=norm
        )

    return cs

def contour(ax,x,y,z,cmap:str,levels:int,centered:bool=True, at:float=1):

    if centered:
        cs = ax.tricontourf(
            x,y,z,levels,cmap=cmap, norm=colors.CenteredNorm(vcenter=at)
        )
    else:
        cs = ax.tricontourf(x,y,z,levels,cmap=cmap)

    return cs

def limit(x:np.ndarray,y:np.ndarray,z:np.ndarray,vmin=None, vmax=None):
    if vmin==None:
        vmin=min(z)
    if vmax==None:
        vmax=max(z)

    z_=[]
    for i,_ in enumerate(x):
        if z[i] < vmin:
            z_.append(vmin + 0.01)
        elif z[i] > vmax:
            z_.append(vmax - 0.01)
        else:
            z_.append(z[i])

    z = np.array(z_)

    return x,y,z

def plot_geom(axes:list[plt.axes], geom_files:list, fill:bool = True):
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
            if fill == True:
                ax.fill(coords[:,0],coords[:,2],color='white')
                if sym_plane!=[]:
                    ax.fill(coords_sym[:,0],coords_sym[:,2],color='white')

            else:
                lines, = ax.plot(coords[:,0],coords[:,2],color='k',label="")
                if sym_plane!=[]:
                    ax.plot(coords_sym[:,0],coords_sym[:,2],color='k')

                return lines

if __name__=="__main__":  

    vel_file = "results/pereira_J/6_blo_actuator_blunt/test.vel1"
    
    dir_="D:/Documents/University/NEWPAN VM/VMDrive2_120122/VMDrive2/DataVM2/Projects/8_Pereira_J_2008/PROP/LR13-D10-d0.1-D31/cases/"
    directory = dir_ + "0V-0A/"
    proj_name = "xz_contours"
    shutil.copy(directory + proj_name + ".vel1",vel_file)

    plane="xz"
    variable="V"
    levels = 50
    bounds = [0,10]

    ############################################################################

    data=read_velcal(vel_file)
    x,y,z = limit(
        x=data[plane[0]],
        y=data[plane[1]],
        z=data[variable] * 3.048,
        vmin=bounds[0],
        vmax=bounds[1]
    )

    fig,ax=plt.subplots()
    # cs = contour(ax,x,y,z,cmap="coolwarm",levels=levels,centered=True,at=0)
    cs = pcolourmesh(ax,x,y,z,"coolwarm",centered=False,at=0)

    plot_geom([ax],["data/SHROUD_BLO_ACTUATOR.json"])

    ax.set_xlabel(f"{plane[0]} (m)")
    ax.set_ylabel(f"{plane[1]} (m)")
    ax.set_aspect("equal")
    # ax.set_box_aspect(1)

    cbar = fig.colorbar(cs,ax=ax,shrink=1)
    cbar.set_label(f"{variable}")

    # plt.legend(facecolor="white",framealpha=1,fancybox=False,edgecolor="black")
    plt.show()