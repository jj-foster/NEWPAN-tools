from velcal_vis_2D import read_velcal
from scn_grid_generate import cylinder, cuboid

import numpy as np
import json

def mass_flow_rate_disk():
    
    data_file="data/EDF_wing/CT0.2_CQ0.0_w1.vel1"
    grid_def="grids/EDF_wing_xz.json"

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
        coords_gen=cuboid(grid_def_data)

    if len(vel_coords)!=len(coords_gen) or np.allclose(vel_coords,coords_gen,atol=1e-5)!=True:
        raise Exception("Velcal grid does not match given grid definition.")

    ### get grid parameters
    r_count     =   int(grid_def_data["r_count"])
    angle_count =   int(grid_def_data["angle_count"])
    d_count     =   int(grid_def_data["d_count"])
    depth       =   float(grid_def_data["depth"])
    
    if depth!=0 and d_count!=1:
        raise Exception("Grid must be 2d.")
    
    ### mdot calculation
    

if __name__=="__main__":
    mass_flow_rate_disk()