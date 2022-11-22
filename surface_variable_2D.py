"""
Use for only one geometry. Multiple wakes are accepted but labels must be input manually.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np
from shapely import ops

def read(data_files:list):

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

    return data, curve_names

def plot(data:list,curve_names:list,variable:str,units:str):

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

    return plt

def intersecting_area(xs:list,ys:list,plot=False):

    # snip ends of curves to match in x
    if xs[0]!=xs[-1]:
        x_min=min([xs[0],xs[-1]])
        xs[0]=x_min
        xs[1]=x_min

    # split curve into 2 surfaces
    split_i=xs.index(min(xs))
    xy0=np.array([xs[:split_i+1], ys[:split_i+1]]).T
    xy0=np.flip(xy0,axis=0)
    xy1=np.array([xs[split_i:], ys[split_i:]]).T
    
    polygon_pts=[]
    for xy in xy0:
        polygon_pts.append([xy[0],xy[1]])
    for xy in xy1[::-1]:
        polygon_pts.append([xy[0],xy[1]])
        
    polygon_pts.append([xy0[0][0],xy0[0][1]])   # append start of curve at end (closes polygon)
    
    # poly0=[]
    # poly1=[]
    # for xy in xy0:
    #     poly0.append([xy[0],xy[1]])
    # for xy in xy1:
    #     poly1.append([xy[0],xy[1]])
    
    line_non_simple=ops.LineString(polygon_pts)
    mls=ops.unary_union(line_non_simple)

    areas=[]
    for polygon in ops.polygonize(mls):
        areas.append(polygon.area)
        
    area_sum=areas[0]-areas[1]

    if plot==True:
        fig,ax=plt.subplots()
        ax.invert_yaxis()

        for polygon in ops.polygonize(mls):
            ax.plot(*polygon.exterior.xy)
            centroid=polygon.centroid.xy
            ax.text(centroid[0][0],centroid[1][0],f"{round(polygon.area,4)}")


    return area_sum

if __name__=="__main__":
    
    # data_files=[
    #     "data/EDF_wing/CT0.0_CQ0.0_w1.exp2d",
    #     "data/EDF_wing/CT0.1_CQ0.0_w1.exp2d",
    #     "data/EDF_wing/CT0.2_CQ0.0_w1.exp2d",
    #     "data/EDF_wing/CT0.5_CQ0.0_w1.exp2d",
    #     "data/EDF_wing/CT3.0_CQ0.0_w1.exp2d",
    # ]
    data_files=["data/nacelle_cp.exp2d"]

    variable='Cp'
    units='m'
    
    data,curve_names=read(data_files)

    area=intersecting_area(data[0]['X'].to_list(),data[0]['Cp'].to_list(),plot=True)
    print(f"Area: {area}")

    fig=plot(data,curve_names,variable,units)
    plt.show()