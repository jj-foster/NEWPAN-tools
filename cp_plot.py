"""
Use for only one geometry. Multiple wakes are accepted but labels must be input manually.
"""

import pandas as pd
import matplotlib.pyplot as plt

data_file="data/nacelle_cp.exp2d"
variable='Cp'
units='m'

#############   read data   #############

with open(data_file,'r') as f:
    lines=f.readlines()

i=0
curve_data=[]
point_data=[]
while i<len(lines):

    if lines[i][0]=="#":
        points=int(lines[i+1])
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
for curve in curve_data:
    data.append(pd.DataFrame(
        curve,
        columns=[
            'x','y','Cp','dCp','Q','phi','u','v','w','Theta','H','Cf','DStar','critk1','critk2','ibl'
        ]
    ))

#############   plot   #############

fig,ax1=plt.subplots()
ax2=ax1.twinx()

for curve in data:
    xs=curve['x'].tolist()
    y1s=curve[variable].tolist()

    ax1.scatter(xs,y1s,marker='o',label=variable)

y2s=curve['y'].tolist()
ax2.plot(xs,y2s,color='k',label='Geometry')


ax1.set_xlabel(f"x ({units})")
ax2.set_ylabel(f"y ({units})")
ax1.set_ylabel(variable)

ax2.set_aspect('equal')

if variable=="Cp":
    ax1.invert_yaxis()
plt.show()