"""
Use for only one geometry. Multiple wakes are accepted but labels must be input manually.
"""

import pandas as pd
import matplotlib.pyplot as plt

data_files=[
    "data/nacelle_cp.exp2d",
    "data/nacelle_wake_cp.exp2d"
]
variable='Cp'
units='m'

#############   read data   #############

curve_data=[]
curve_columns=[]
for file in data_files:

    with open(file,'r') as f:
        lines=f.readlines()

    i=0
    point_data=[]
    while i<len(lines):

        if lines[i][0]=="#":
            points=int(lines[i+1])

            columns=lines[i+2].strip().split()[1:]
            curve_columns.append(columns)

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

for curve in data:
    xs=curve['X'].tolist()
    y1s=curve[variable].tolist()

    ax1.plot(xs,y1s,marker='.',label=variable)

y2s=curve['Y'].tolist()
ax2.plot(xs,y2s,color='k',label='Geometry')


ax1.set_xlabel(f"x ({units})")
ax2.set_ylabel(f"y ({units})")
ax1.set_ylabel(variable)

ax2.set_aspect('equal')
ax1.legend(["no wake","wake relaxation 1"])

if variable=="Cp":
    ax1.invert_yaxis()

plt.show()