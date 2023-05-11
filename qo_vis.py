import numpy as np
from grid_generate import plot_grid
import matplotlib.pyplot as plt
import pandas as pd

def read_qo(qo_file:str) -> pd.DataFrame:
    """
    Read QO file into a pandas dataframe
    """
    with open(qo_file,'r') as f:
        qo=pd.read_csv(f,delim_whitespace=True,skiprows=1,header=None)

    qo.columns=["x","y","z","du","dv","dw","dcp"]

    return qo

def qo(qo_file,ax=None):

    qo = read_qo(qo_file)

    #print(len(qo))
    
    if ax==None:
        fig,ax=plt.subplots()

    plot_grid(qo[["x","y","z"]].to_numpy(),ax=ax)

    # check for duplicates
    duplicates=qo.duplicated(["x","y","z"],keep="first")
    print(qo[duplicates])

    return ax

if __name__=="__main__":

    proj_dir="D:\\Documents\\University\\NEWPAN VM\\VMDrive2_120122\\VMDrive2\\DataVM2\\Projects\\6_qo\\4_qo_EDF_outline\\"
    proj_name="wing"
    qo_file=proj_dir+proj_name+".qo"

    qo(qo_file)
    plt.show()
