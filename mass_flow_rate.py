from velcal_vis_2D import read_velcal
from grid_generate import cylinder, cuboid_filled

import numpy as np
import json
import shutil
from typing import Tuple

def mass_flow_rate_disk(data_file: str, grid_def: str) -> Tuple[float]:
    
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

    mdot: float = 0
    line_count: int = 0
    for i in range(r_count):
        for j in range(angle_count):

            u[i,j]=vel_data["u"][line_count]
            v[i,j]=vel_data["v"][line_count]
            w[i,j]=vel_data["w"][line_count]

            if np.isnan(u[i,j]):
                u[i,j]=0
            if np.isnan(v[i,j]):
                v[i,j]=0
            if np.isnan(w[i,j]):
                w[i,j]=0

            Cp[i,j]=vel_data["Cp"][line_count]
            # V[i,j]=np.sqrt(u[i,j]**2+v[i,j]**2+w[i,j]**2)

            line_count+=1

            if i==0 or j==0:
                continue
            
            # mdot calculation - assumes constant density

            AU: float =(r_steps[i]**2-r_steps[i-1]**2)*((u[i,j]+u[i,j-1]+u[i-1,j]+u[i-1,j-1])/4)
            mdot_=AU*np.pi*angle_steps[1]/(2*np.pi)

            mdot+=mdot_
    
    u_avg: float = round(np.mean(u[:,0]), 4-int(np.floor(np.log10(abs(np.mean(u[:,0])))))-1)
    # u_avg=0
    mdot: float = round(mdot, 4-int(np.floor(np.log10(abs(mdot))))-1)

    return mdot,u_avg
    
if __name__=="__main__":

    dir_="D:/Documents/University/NEWPAN VM/VMDrive2_120122/VMDrive2/DataVM2/Projects/8_Pereira_J_2008/PROP/LR13-D10-d0.1-D31/cases/"
    vel_files=[
        "D:/Documents/University/NEWPAN VM/VMDrive2_120122/VMDrive2/DataVM2/Projects/8_Pereira_J_2008/PROP/LR13-D10-d0.6-L72/0V-0A-0.0211CT/0V-0A-CT.vel1",
        # dir_+"0V-0A/0V-0A.vel1",
        # dir_+"3V-0A/3V-0A.vel1",
        # dir_+"3V-30A/3V-30A.vel1",
        # dir_+"3V-60A/3V-60A.vel1",
        # dir_+"3V-90A/3V-90A.vel1",
    ]
    # grid_def="grids/Pereira, 2008/SHROUD_outlet.json"
    grid_def = "grids/Pereira, 2008/SHROUD_outlet_L72.json"

    for i,_ in enumerate(vel_files):
        mdot,u_avg=mass_flow_rate_disk(vel_files[i],grid_def)
        print(f"u_avg: {u_avg}\nmdot: {mdot}")
