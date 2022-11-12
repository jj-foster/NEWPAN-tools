import matplotlib.pyplot as plt
import numpy as np

data="data/wing_actuator/actuator_line_section2.vel1"

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

lengths=[]
total_len=0
for i,_ in enumerate(x):
    if i==0:
        dx=0
    else:
        dx=np.linalg.norm(np.array([x[i],y[i],z[i]])-np.array([x[i-1],y[i-1],z[i-1]]))

    total_len+=dx
    lengths.append(total_len)

xs=[]
for length in lengths:
    xs.append(length/total_len)

xs=y

def plot(xs,ys,series,ax=None,vmin=None,vmax=None):
    # limit
    if vmin==None:
        vmin=min(ys)
    if vmax==None:
        vmax=max(ys)

    ys_=[]
    for i,_ in enumerate(xs):
        if ys[i]<vmin:
            ys_.append(vmin)
        elif ys[i]>vmax:
            ys_.append(vmax)
        else:
            ys_.append(ys[i])

    # plot
    if ax==None:
        fig,ax=plt.subplots()
    
    ax.plot(xs,ys,label=series)

    return plt

fig,ax=plt.subplots()

plot(xs,u,"u",ax=ax)#,vmin=-0.5,vmax=2)
plot(xs,v,"v",ax=ax)
plot(xs,w,"w",ax=ax)
plot(xs,Cp,"Cp",ax=ax)#,vmin=-5,vmax=5)

ax.legend()
#ax.set_xlabel("x/X")

plt.show()