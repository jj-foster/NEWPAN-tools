import numpy as np

proj_name="EDF"
directory="D:/Documents/University/NEWPAN VM/VMDrive2_120122/VMDrive2/DataVM2/Projects/3_EDF/1_EDFActuatorDisk/"

run=1
wake=1

corner=np.array([-0.1,0,-0.1])
delta=np.array([0.6,0,0.2])

x_count=300
y_count=0
z_count=300

####################################################################################

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
#with open('a.txt','w') as f:
    f.writelines(lines)