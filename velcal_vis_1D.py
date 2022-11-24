import matplotlib.pyplot as plt
import numpy as np
import shutil

proj_dir="D:\\Documents\\University\\NEWPAN VM\\VMDrive2_120122\\VMDrive2\\DataVM2\\Projects\\6_qo\\2_qo\\"
proj_name="wing"
vel_file0=proj_dir+proj_name+".vel1"

vel_file="results/wing_qo/line_4_0.5du.vel1"
shutil.copy(vel_file0,vel_file)

# vel_file="results/wing_qo/line_5_1du.vel1"

with open(vel_file,'r') as f:
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

#xs=y
xs=x

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
plot(xs,w,"w",ax=ax,vmin=-5,vmax=5)
#plot(xs,Cp,"Cp",ax=ax)#,vmin=-5,vmax=5)

ax.scatter([-5,-2.5,0,2.5],[1,0,0.5,0],color='k')

ax.set_yticks(np.arange(-5, 5+1, 1.0))
ax.set_xlabel("x (m)")
ax.set_ylabel("V (m/s)")
ax.set_box_aspect(1)
#ax.set_xlabel("x/X")

ax.legend()
plt.show()