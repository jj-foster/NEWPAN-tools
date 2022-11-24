from velcal_vis_2D import read_velcal
from grid_generate import cylinder, cuboid

import numpy as np
import json
import shutil

def mass_flow_rate_disk(data_file,grid_def):
    
    vel_data=read_velcal(data_file)
    
    vel_coords=np.stack((vel_data["x"],vel_data["y"],vel_data["z"]),axis=1)

    ### check if x,y, or z are const
    const_check=np.all(vel_coords==vel_coords[0,:],axis=0)
    if len(np.where(const_check==True)[0])!=1:
        raise Exception("Data must be 2d.")

    ### check if data coords match generated coords
    with open(grid_def,'r') as f:
        grid_def_data=json.load(f)
    
    if grid_def_data["type"]=="cylinder":
        coords_gen=cylinder(grid_def_data)
    elif grid_def_data["type"]=="cuboid":
        raise Exception("Grid must be of cylinder type.")

    if len(vel_coords)!=len(coords_gen) or np.allclose(vel_coords,coords_gen,atol=1e-5)!=True:
        raise Exception("Velcal grid does not match given grid definition.")

    ### get grid parameters
    r1          =   float(grid_def_data["r1"])
    r2          =   float(grid_def_data["r2"])
    depth       =   float(grid_def_data["depth"])
    r_count     =   int(grid_def_data["r_count"])
    angle_count =   int(grid_def_data["angle_count"])
    d_count     =   int(grid_def_data["d_count"])
    
    if depth!=0 and d_count!=1:
        raise Exception("Grid must be 2d.")
    
    ### restructure velocity and cp data according to grid def
    r_steps=np.linspace(r1,r2,r_count)
    angle_steps=np.linspace(0,2*np.pi,angle_count+1)

    u=np.zeros((r_count,angle_count))
    v=np.zeros((r_count,angle_count))
    w=np.zeros((r_count,angle_count))
    V=np.zeros((r_count,angle_count))
    Cp=np.zeros((r_count,angle_count))

    mdot=0
    line_count=0
    for i in range(r_count):
        for j in range(angle_count):

            u[i,j]=vel_data["u"][line_count]
            v[i,j]=vel_data["v"][line_count]
            w[i,j]=vel_data["w"][line_count]
            Cp[i,j]=vel_data["Cp"][line_count]
            V[i,j]=np.sqrt(u[i,j]**2+v[i,j]**2+w[i,j]**2)

            line_count+=1

            if i==0 or j==0:
                continue
            
            # mdot calculation - assumes constant density

            AU=(r_steps[i]**2-r_steps[i-1]**2)*((V[i,j]+V[i,j-1]+V[i-1,j]+V[i-1,j-1])/4)
            mdot+=AU*np.pi*angle_steps[1]/(2*np.pi)
    
    u_avg=round(np.mean(V[:,0]), 4-int(np.floor(np.log10(abs(np.mean(V[:,0])))))-1)
    mdot=round(mdot, 4-int(np.floor(np.log10(abs(mdot))))-1)

    return mdot,u_avg
    
if __name__=="__main__":
    
    # proj_dir="D:\\Documents\\University\\NEWPAN VM\\VMDrive2_120122\\VMDrive2\\DataVM2\\Projects\\3_EDF\\3_EDFActuatorDisk_wake\\"
    # proj_name="EDF"
    # vel_file=proj_dir+proj_name+".vel1"

    # relocate="results/EDF_actuator/EDF_inlet.vel1"
    # shutil.copy(vel_file,relocate)

    vel_file="results/EDF_actuator/EDF_inlet.vel1"
    grid_def="grids/EDF_inlet.json"

    mdot,u_avg=mass_flow_rate_disk(vel_file,grid_def)
    print(f"u_avg: {u_avg}\nmdot: {mdot}")