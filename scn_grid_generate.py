import numpy as np
import json
import matplotlib.pyplot as plt

def cuboid(data):
    corner = np.array(data["corner"])
    delta = np.array(data["delta"])
    x_count,y_count,z_count = data["count"]

    x0,y0,z0=corner
    x1,y1,z1=corner+delta

    if x_count>0:
        xs=np.linspace(x0,x1,x_count)
    else:
        xs=[x0]
    if y_count>0:
        ys=np.linspace(y0,y1,y_count)
    else:
        ys=[y0]
    if z_count>0:
        zs=np.linspace(z0,z1,z_count)
    else:
        zs=[z0]

    if 0 not in [x_count,y_count,z_count]:
        raise ValueError("2D planes only")

    coords=[]
    for i in xs:
        for j in ys:
            for k in zs:
                coords.append([i,j,k])

    coords=np.array(coords)

    return coords

def cylinder(data):

    origin  =   np.array(data["origin"])
    axis    =   np.array(data["axis"])
    r1      =   float(data["r1"])
    r2      =   float(data["r2"])
    depth   =   float(data["depth"])
    r_count =   int(data["r_count"])
    angle_count =   int(data["angle_count"])
    d_count =   int(data["d_count"])

    r_steps=np.linspace(r1,r2,r_count)
    angle_steps=np.linspace(0,2*np.pi,angle_count+1)
    d_steps=np.linspace(0,depth,d_count)

    v1=np.array([0,0,1])   # v1 aligned with z
    v2=np.cross(v1,axis)

    coords=[]
    # 1. circle, 2. radial, 3. depth
    for d in d_steps:
        if depth!=0:
            centre=origin+axis*depth*d/depth
        else:
            centre=origin
        
        for r in r_steps:
            for a in angle_steps:
                coord=list(centre+r*(np.cos(a)*v1+np.sin(a)*v2))
                #if coord not in coords:
                coords.append(coord)

    coords=np.array(coords)
    coords=np.around(coords,10)

    return coords

def plot_grid(coords):

    fig=plt.figure()

    # check if x,y, or z are const
    const_check=np.all(coords==coords[0,:],axis=0)

    if True in const_check:
        # plots in 2d, excluding first column that is const.
        zero_index=np.where(const_check==True)[0][0]
        coords=np.delete(coords,zero_index,axis=1)

        ax=plt.axes()
        ax.scatter(coords[:,0],coords[:,1],color='k',marker='.')
        ax.set_aspect('equal')

    else:
        ax=plt.axes(projection='3d')

        ax.scatter(coords[:,0],coords[:,1],coords[:,2],color='k',marker='.')

        # sets plot aspect ratio
        ax.set_box_aspect((np.ptp(coords[:,0]),np.ptp(coords[:,1]),np.ptp(coords[:,2])))

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

    plt.show()

def export_grid(run,wake,coords):
    lines=[
        f"{run} {wake}\n"
    ]

    for coord in coords:
        lines.append(f"{coord[0]} {coord[1]} {coord[2]}\n")
    
    with open(f"{directory}{proj_name}.scn",'w') as f:
        f.writelines(lines)

    return None

if __name__=="__main__":

    proj_name="EDF"
    directory="D:\\Documents\\University\\NEWPAN VM\\VMDrive2_120122\\VMDrive2\\DataVM2\\Projects\\3_EDF\\3_EDFActuatorDisk_wake\\"
    grid_def="grids/EDF_outlet.json"

    run=1
    wake=1

    plot=False
    export=True

    ####################################################################################

    with open(grid_def,'r') as f:
        data=json.load(f)

    if data["type"]=="cylinder":
        coords=cylinder(data)

    elif data["type"]=="cuboid":
        coords=cuboid(data)

    else:
        raise ValueError("Invalid grid type.")

    if export==True:
        export_grid(run,wake,coords)
    if plot==True:
        plot_grid(coords)
    