import matplotlib.pyplot as plt
import numpy as np

data="data/EDF_blo.vel1"
plane="xz"

with open(data,'r') as f:
    lines=f.readlines()

lines=lines[2:]

x=np.zeros((len(lines)))
y=np.zeros((len(lines)))
z=np.zeros((len(lines)))
u=np.zeros((len(lines)))
v=np.zeros((len(lines)))
w=np.zeros((len(lines)))
Cp=np.zeros((len(lines)))

for i,line in enumerate(lines):
    line_=line.strip().split()
    
    x[i]=float(line_[0])
    y[i]=float(line_[1])
    z[i]=float(line_[2])
    u[i]=float(line_[3])
    v[i]=float(line_[4])
    w[i]=float(line_[5])
    Cp[i]=float(line_[6])

if plane.upper()=="XZ":
    xs,ys=x,z
elif plane.upper()=="XY":
    xs,ys=x,y
elif plane.upper()=="YZ":
    xs,ys=y,z
else:
    raise ValueError("Invalid plane.")

def plot(xs,ys,z,title,contours,vmin=None,vmax=None):
    # limit
    if vmin==None:
        vmin=min(z)
    if vmax==None:
        vmax=max(z)

    z_=[]
    for i,_ in enumerate(xs):
        if z[i]<vmin:
            z_.append(vmin)
        elif z[i]>vmax:
            z_.append(vmax)
        else:
            z_.append(z[i])

    # plot
    fig,ax=plt.subplots()
    cs=ax.tricontourf(xs,ys,z_,contours)
    cbar=fig.colorbar(cs,label=title)
    ax.set_aspect('equal')
    ax.set_title(title)

    return plt

fig1=plot(xs,ys,u,"u",50,vmin=-2,vmax=2)
# fig2=plot(xs,ys,v,"v",50,vmin=-5,vmax=5)
# fig3=plot(xs,ys,w,"w",50,vmin=-5,vmax=5)
fig4=plot(xs,ys,Cp,"Cp",50,vmin=-5,vmax=5)

plt.show()
