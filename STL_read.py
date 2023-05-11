import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt

def get_facets(file:str) -> np.ndarray:

    with open(file,'r') as f:
        lines = f.readlines()

    lines_ = []
    for line in lines:
        line_ = line
        line_ = line_.strip()
        line_ = line_.split()

        lines_.append(line_)
    lines = lines_

    facets = []

    i = 0
    while i < len(lines):

        if lines[i][0] == "vertex":
            facets.append([
            [float(lines[i][1]), float(lines[i+1][1]), float(lines[i+2][1])],
            [float(lines[i][2]), float(lines[i+1][2]), float(lines[i+2][2])],
            [float(lines[i][3]), float(lines[i+1][3]), float(lines[i+2][3])]
            ])

            i+=7
        else:
            i+=1

    facets = np.array(facets)

    return facets

def facet_to_coords(facets:np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = []
    y = []
    z = []

    for facet in facets:
        for point in facet[0]:
            x.append(point)
        for point in facet[1]:
            y.append(point)
        for point in facet[2]:
            z.append(point)

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)

    return x,y,z

if __name__ == "__main__":
    stl_file = "data/EDF.stl"

    facets = get_facets(stl_file)
    x,y,z = facet_to_coords(facets)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.plot(x,y,z,color='r',linewidth=0.05)
    ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))

    plt.show()
    
