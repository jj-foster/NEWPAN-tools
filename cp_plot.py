import pandas as pd
import matplotlib.pyplot as plt

data_file="nacelle_cp2.exp2d"
axes=['x','Cp']

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

fig,ax=plt.subplots()

for curve in data:
    xs=curve[axes[0]].tolist()
    ys=curve[axes[1]].tolist()

    ax.plot(xs,ys)

ax.set_xlabel(axes[0])
ax.set_ylabel(axes[1])

plt.gca().invert_yaxis()
plt.show()