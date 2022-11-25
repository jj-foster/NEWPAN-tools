import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib import cm, colors

def cuboid_filled(data:dict)->np.ndarray:
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

    if 0 not in [x_count,y_count,z_count] and 1 not in [x_count,y_count,z_count]:
        raise ValueError("2D planes only")

    coords=[]
    for i in xs:
        for j in ys:
            for k in zs:
                coords.append([i,j,k])

    coords=np.array(coords)

    return coords

def cuboid_empty(data:dict)->np.ndarray:
    corner = np.array(data["corner"])
    delta = np.array(data["delta"])
    x_count,y_count,z_count = data["count"]

    # determines dimensions of bounding box
    D=0
    for i in [x_count,y_count,z_count]:
        if i>1:
            D+=1

    """
         B2-C2      y  z
      /  A2-D2      | / 
    B1-C1  /        |___x 
    A1-D1
    """
    A1=corner
    B1=corner + np.array([0,delta[1],0])
    C1=corner + np.array([delta[0],delta[1],0])
    D1=corner + np.array([delta[0],0,0])
    A2=A1     + np.array([0,0,delta[2]])
    B2=B1     + np.array([0,0,delta[2]])
    C2=C1     + np.array([0,0,delta[2]])
    D2=D1     + np.array([0,0,delta[2]])

    # 2D ie. a rectangular ring.
    if D==2:
        coords=[]
        coords.append(np.linspace(A1,B1,y_count))
        coords.append(np.linspace(B1,C1,x_count))
        coords.append(np.linspace(C1,D1,y_count))
        coords.append(np.linspace(D1,A1,x_count))
        coords.append(np.linspace(A1,A2,z_count))
        coords.append(np.linspace(B1,B2,z_count))
        coords.append(np.linspace(C1,C2,z_count))
        coords.append(np.linspace(D1,D2,z_count))
        coords.append(np.linspace(A2,B2,y_count))
        coords.append(np.linspace(B2,C2,x_count))
        coords.append(np.linspace(C2,D2,y_count))
        coords.append(np.linspace(D2,A2,x_count))

        coords_=[]
        for a in coords:
            for b in a:
                if list(b) not in coords_:
                    coords_.append(list(b))
                
        coords=np.array(coords_)
    
    # 3D ie. a box.
    elif D==3:

        def replace(array,x,i):
            array[:,i]+=x
            return array

        bottom={"corner":A1,"delta":[delta[0],delta[1],0],"count":[x_count,y_count,1]}    # A1B1C1D1 surface
        coords_bottom=cuboid_filled(bottom)
        coords_top=replace(coords_bottom.copy(),delta[2],2)

        front={"corner":A1,"delta":[delta[0],0,delta[2]],"count":[x_count,1,z_count]}    # A1A2D2D1 surface
        coords_front=cuboid_filled(front)
        coords_back=replace(coords_front.copy(),delta[1],1)

        left={"corner":A1,"delta":[0,delta[1],delta[2]],"count":[1,y_count,z_count]}    # A1A2B2B1 surface
        coords_left=cuboid_filled(left)
        coords_right=replace(coords_left.copy(),delta[0],0)

        coords=np.concatenate((
            coords_bottom,
            coords_top,
            coords_front,
            coords_back,
            coords_left,
            coords_right
        ))

        coords_=[]
        for coord in coords:
            if list(coord) not in coords_:
                coords_.append(list(coord))
        coords=np.array(coords_)

    else:
        raise Exception("Grid definition error: 1D not supported for empty cuboids.")

    return coords

def cylinder(data:dict)->np.ndarray:

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

def plot_grid(coords,dV=None):
    if dV!=None:
        cmap=cm.jet
        minV=coords[:,3+dV].min()
        maxV=coords[:,3+dV].max()
        norm=colors.BoundaryNorm(
            np.linspace(minV,maxV,np.unique(coords[:,3+dV]).shape[0]+1),
            cmap.N,
            extend='neither'
        )

    fig=plt.figure()

    # check if x,y, or z are const
    const_check=np.all(coords==coords[0,:],axis=0)[:3]

    if True in const_check:
        # plots in 2d, excluding first column that is const.
        zero_index=np.where(const_check==True)[0][0]
        coords=np.delete(coords,zero_index,axis=1)

        ax=plt.axes()
        if dV!=None:
            for coord in coords:
                ax.scatter(coord[0],coord[1],color=cmap(norm(coords[3+dV])),marker='.')
        else:
            ax.scatter(coords[:,0],coords[:,1],color='k',marker='.')
        ax.set_aspect('equal')

    else:
        ax=plt.axes(projection='3d')

        if dV!=None:
            for coord in coords:
                a=cmap(norm(coord[3+dV]))
                ax.scatter(coord[0],coord[1],coord[2],color=a,marker='.')
        else:
            ax.scatter(coords[:,0],coords[:,1],coords[:,2],color='k',marker='.')

        # sets plot aspect ratio
        ax.set_box_aspect((np.ptp(coords[:,0]),np.ptp(coords[:,1]),np.ptp(coords[:,2])))

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        plt.tight_layout()

    if dV!=None:
        sm=plt.cm.ScalarMappable(cmap=cmap,norm=norm)
        plt.colorbar(sm,ax=ax,label="dV",pad=0.10)

    plt.show()

def export_grid(run,wake,coords,file_type):
    
    if file_type==".scn":
        lines=[f"{run} {wake}\n"]
    elif file_type==".qo" or file_type==".qom" or file_type==".qpt":
        coords_=[]
        for coord in coords:
            if list(coord) not in coords_:
                coords_.append(list(coord))
        coords=np.array(coords_)

        lines=[f"{int(len(coords))}\n"]
    else:
        raise Exception(f"{file_type} is not a valid file type.")

    for coord in coords:
        lines.append(f"{' '.join([str(x) for x in coord.tolist()])}\n")
    
    with open(f"{directory}{proj_name}{file_type}",'w') as f:
        f.writelines(lines)

    return None

def const_qo(coords,dV):

    du  = np.full(len(coords),dV[0])
    dv  = np.full(len(coords),dV[1])
    dw  = np.full(len(coords),dV[2])
    dcp = np.full(len(coords),dV[3])
    
    coords=coords.T

    coords=coords.tolist()
    coords.append(du)
    coords.append(dv)
    coords.append(dw)
    coords.append(dcp)
    
    coords=np.array(coords).T

    return coords

if __name__=="__main__":

    proj_name="EDF"
    directory="D:\\Documents\\University\\NEWPAN VM\\VMDrive2_120122\\VMDrive2\\DataVM2\\Projects\\3_EDF\\4_EDF_qo\\"

    grid_def=["grids/EDF_bb.json","grids/EDF_efflux_sleeve.json","grids/EDF_qo.json"]

    run=1
    wake=1

    plot=True
    export=True

    file_type=".qo"

    ####################################################################################

    coords=[]
    for grid in grid_def:

        with open(grid,'r') as f:
            data=json.load(f)

        if data["type"]=="cylinder":
            coords_=cylinder(data)
        elif data["type"]=="cuboid":
            if data["filled"]==True:
                coords_=cuboid_filled(data)
            else:
                coords_=cuboid_empty(data)
        else:
            raise ValueError("Invalid grid type.")

        if file_type==".qo" or file_type==".qom":
            coords_=const_qo(coords_,data["qo"])
        
        coords.append(coords_)

    coords=np.concatenate([coords[i] for i in range(len(coords))])
        
    if plot==True:
        if file_type==".qo" or file_type==".qom":
            plot_grid(coords,dV=0)
        else:
            plot_grid(coords)
    
    if export==True:
        export_grid(run,wake,coords,file_type)
