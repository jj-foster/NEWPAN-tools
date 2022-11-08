"""
Use for only one geometry. Multiple wakes are accepted but labels must be input manually.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

data_files=[
    "data/EDF_wing/CT0.0_CQ0.0_w1.exp2d",
    "data/EDF_wing/CT0.1_CQ0.0_w1.exp2d",
    "data/EDF_wing/CT0.2_CQ0.0_w1.exp2d",
    "data/EDF_wing/CT0.5_CQ0.0_w1.exp2d",
    "data/EDF_wing/CT3.0_CQ0.0_w1.exp2d",
]
variable='Cp'
units='m'

#############   read data   #############

curve_data=[]
curve_columns=[]
curve_names=[]
for file in data_files:
    file_name=os.path.splitext(file)[0].split("/")[-1]

    with open(file,'r') as f:
        lines=f.readlines()

    i=0
    point_data=[]
    curve_count=0
    while i<len(lines):

        if lines[i][0]=="#":
            points=int(lines[i+1])
            
            columns=lines[i+2].strip().split()[1:]
            curve_columns.append(columns)

            curve_names.append(f"{file_name}_{curve_count}")
            curve_count+=1

            i+=3

            continue
        
        j=0
        point_data=[]
        while j<points:
            line=lines[i+j].strip().split()
            line=list(map(float,line))

            point_data.append(line)

            j+=1
            
        curve_data.append(point_data)
        i+=points

data=[]
for i,curve in enumerate(curve_data):
    data.append(pd.DataFrame(
        curve,
        columns=curve_columns[i]
    ))

#############   plot   #############

fig,ax1=plt.subplots()
ax2=ax1.twinx()

for i,curve in enumerate(data):
    xs=curve['X'].tolist()
    y1s=curve[variable].tolist()

    """
    if curve_names[i][:2]=="cl":
        color='r'
    else:
        color='b'

    if curve_names[i][-1]=="0":
        marker='o'
    else:
        marker='D'

    ax1.plot(xs,y1s,marker=marker,color=color,label=curve_names[i])
    """

    ax1.plot(xs,y1s,marker='o',label=curve_names[i])

y2s=curve['Y'].tolist()
ax2.plot(xs,y2s,color='k',label='Geometry')


ax1.set_xlabel(f"x ({units})")
ax2.set_ylabel(f"y ({units})")
ax1.set_ylabel(variable)

ax2.set_aspect('equal')
ax1.legend()

if variable=="Cp":
    ax1.invert_yaxis()

plt.show()