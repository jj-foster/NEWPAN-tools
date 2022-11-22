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

    origin      =   np.array(data["origin"])
    axis        =   np.array(data["axis"])
    r1          =   float(data["r1"])
    r2          =   float(data["r2"])
    depth       =   float(data["depth"])
    r_count     =   int(data["r_count"])
    angle_count =   int(data["angle_count"])
    d_count     =   int(data["d_count"])
    r1_taper_angle = float(data["r1_taper_angle"])
    r2_taper_angle = float(data["r2_taper_angle"])

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
        
        r1_=r1+d*np.sin(np.deg2rad(r1_taper_angle))
        r2_=r2+d*np.sin(np.deg2rad(r2_taper_angle))
        r_steps=np.linspace(r1_,r2_,r_count)

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

def export_grid(run,wake,coords,file_type):
    
    if file_type==".scn":
        lines=[f"{run} {wake}\n"]
    elif file_type==".qo" or file_type==".qom" or file_type==".qpt":
        lines=[f"{int(len(coords))}\n"]
    else:
        raise Exception(f"{file_type} is not a valid file type.")

    for coord in coords:
        lines.append(f"{' '.join([str(x) for x in coord.tolist()])}\n")
    
    with open(f"{directory}{proj_name}{file_type}",'w') as f:
        f.writelines(lines)

    return None

def const_qo(coords):

    du  = np.full(len(coords),0)
    dv  = np.full(len(coords),0)
    dw  = np.full(len(coords),0)
    dcp = np.full(len(coords),-10)
    
    coords=coords.T

    # coords = np.append(coords,du,axis=0)
    # coords = np.append(coords,dv,axis=0)
    # coords = np.append(coords,dw,axis=0)
    # coords = np.append(coords,dcp,axis=0)
    
    coords=coords.tolist()
    coords.append(du)
    coords.append(dv)
    coords.append(dw)
    coords.append(dcp)
    
    coords=np.array(coords).T

    return coords

if __name__=="__main__":

    proj_name="wing"
    directory="D:\\Documents\\University\\NEWPAN VM\\VMDrive2_120122\\VMDrive2\\DataVM2\\Projects\\6_qo\\1_qo\\"
    grid_def="grids/wing_qo_xz.json"

    run=1
    wake=0

    plot=True
    export=True

    file_type=".qpt"

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
        if file_type==".qo" or file_type==".qom":
            coords=const_qo(coords)
            
        export_grid(run,wake,coords,file_type)

    if plot==True:
        plot_grid(coords)
    