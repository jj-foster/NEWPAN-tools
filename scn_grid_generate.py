import numpy as np
import json

proj_name="EDF_wing"
directory="D:/Documents/University/NEWPAN VM/VMDrive2_120122/VMDrive2/DataVM2/Projects/5_EDF_wing/"
grid_def="grids/EDF_wing_xz.json"

run=1
wake=1

####################################################################################

with open(grid_def,'r') as f:
    data=json.load(f)

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

lines=[
    f"{run} {wake}\n"
]

for i in xs:
    for j in ys:
        for k in zs:
            lines.append(f"{i} {j} {k}\n")

with open(f"{directory}{proj_name}.scn",'w') as f:
    f.writelines(lines)