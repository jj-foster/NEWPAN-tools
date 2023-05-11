"""
Use for only one geometry. Multiple wakes are accepted but labels must be input manually.
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def read_exp2d(data_files:list):

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

def plot_exp2d(data:list,curve_names:list,variable:str,units:str):

    fig,ax1=plt.subplots()
    ax2=ax1.twinx()

    for i,curve in enumerate(data):
        xs=curve['X'].tolist()
        y1s=curve[variable].tolist()

        ax1.plot(xs,y1s,color='k',linestyle=LINESTYLES[i],label=curve_names[i])

    y2s=curve['Y'].tolist()
    ax2.plot(xs,y2s,color='k',label='Nacelle')

    ax1.set_xlabel(f"x ({units})")
    ax2.set_ylabel(f"y ({units})")
    ax1.set_ylabel(variable)

    ax2.set_aspect('equal')
    ax2.set_box_aspect(1)

    if variable=="Cp":
        ax1.invert_yaxis()

        
    lines1,labels1=ax1.get_legend_handles_labels()
    lines2,labels2=ax2.get_legend_handles_labels()
    ax2.legend(lines1+lines2,labels1+labels2,frameon=False,loc="upper left")

    return plt

if __name__=="__main__":
   
    data_files=["data/nacelle_cp.exp2d"]

    variable='Cp'
    units='m'
    
    data,curve_names=read_exp2d(data_files)

    fig=plot_exp2d(data,curve_names,variable,units)
    plt.show()