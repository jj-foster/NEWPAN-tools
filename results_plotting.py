import matplotlib.pyplot as plt
import numpy as np

from velcal_vis_2D import contour, pcolourmesh, limit, read_velcal, plot_geom
from velcal_vis_1D import read_vel, normalize_line_length
from qo_vis import read_qo
from grid_generate import grid_type_coords
from STL_read import get_facets, facet_to_coords
from surface_variable_2D import read_exp2d, plot_exp2d

plt.rcParams["font.family"] = "Arial"
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["font.size"] = 14
plt.rcParams["figure.dpi"] = 200


def blo_tests():

    vel_files = [
        "results/EDF_blo/EDF_blo_wake.vel1",
        "results/EDF_blo/EDF_blo_wake_cut.vel1"
    ]
    geom_files = [
        "data/EDF_blockage.json",
        "data/EDF_nacelle.json",
        "data/EDF_blo.json"
    ]

    titles = [
        "(a) Base case wake relaxation.",
        "(b) CUT file implemented."
    ]

    variable = "u"

    plane = "xz"
    bounds = [-5, 5]
    levels = 50

    # init figure
    fig = plt.figure()
    axes = fig.subplots(nrows=1, ncols=2, sharey=True)

    cs = []
    for i, f in enumerate(vel_files):
        ax = axes[i]

        velcal_data = read_velcal(f)

        x, y, z = limit(
            x=velcal_data[plane[0]],
            y=velcal_data[plane[1]],
            z=velcal_data[variable],
            vmin=bounds[0],
            vmax=bounds[1]
        )

        # Contour plot
        c = contour(ax, x, y, z, cmap="coolwarm", levels=levels, centered=True)
        # c = pcolourmesh(ax,x,y,z,cmap="coolwarm",centered=True)
        cs.append(c)

        # Inlet/exit labels
        # ax.plot(
        #     [0.008,0.008],[0.01788941,0.0428],
        #     color='k',linestyle="--",linewidth="2", label="BLO Inlet")
        # ax.plot(
        #     [0.008,0.008],[-0.01788941,-0.0428],
        #     color='k',linestyle="--",linewidth="2")
        ax.plot(
            [0.1279963, 0.1279963], [0.025, 0.03587086],
            color='k', linestyle="-", linewidth="2", label="BLO Outlet")
        ax.plot(
            [0.1279963, 0.1279963], [-0.025, -0.03587086],
            color='k', linestyle="-", linewidth="2")

        ax.set_aspect("equal")
        ax.set_xlabel("x (m)")

        ax.set_xlim((0.1, 0.24))

        ax.text(0.5, -0.25, titles[i], size=11,
                ha="center", transform=ax.transAxes)

        # ax.set_title(titles[i])

    plot_geom(axes, geom_files)

    axes[0].legend(
        facecolor="white", framealpha=1, fancybox=False, edgecolor="black")

    axes[0].set_ylabel("z (m)")

    cbar = fig.colorbar(cs[0], ax=axes.ravel().tolist(), shrink=0.7)
    cbar.set_label("u (m/s)")

    # plt.tight_layout()
    plt.show()

def qo_test_1D():
    vel_files = [
        "results/wing_qo/2_points.vel1",
        "results/wing_qo/4_points.vel1"
    ]

    qo_coords = [
        [[-5,0],[1,0]],
        [[-6,-2,2,6],[1,0,1,0]]
    ]

    fig = plt.figure()
    axes = fig.subplots(nrows=1, ncols=2, sharey=True)

    for i, f in enumerate(vel_files):
        x, y, z, u, v, w, Cp = read_vel(f)
        # x = normalize_line_length(x,y,z)



        ax = axes[i]

        # ax.plot(x, u, color='k', label=r"$u$", linestyle="-")
        # ax.plot(x, v, color='k', label=r"$v$", linestyle="--")
        ax.plot(x, w, color='k', label="$w$", linestyle="-")

        ax.set_xlabel("x (m)")

        try:
            ax.scatter(
                qo_coords[i][0], qo_coords[i][1], marker="o",
                edgecolor="k",facecolor="none", label=r"QO $\Delta w$"
            )
        except IndexError:
            pass

        ax.set_box_aspect(1)

    axes[0].set_ylabel("$w$ (m/s)")
    axes[0].legend(frameon=True, facecolor="white", edgecolor="black",
                   fancybox=False, framealpha=1, loc="upper left")

    plt.show()

def qo_test_2D():
    vel_files = [
        "results/wing_qo/domain1.vel1"
    ]

    qo_files = [
        "results/wing_qo/domain_0ms.qo",
        "results/wing_qo/domain_1ms.qo"
    ]
    qo_markers = [
        "o",
        "s"
    ]

    variable = "w"
    plane = "xz"
    levels = 50

    # init figure
    fig,ax = plt.subplots()

    velcal_data = read_velcal(vel_files[0])
    x=velcal_data[plane[0]]
    y=velcal_data[plane[1]]
    z=velcal_data[variable]

    cs = contour(ax, x, y, z, cmap="coolwarm", levels=levels, centered=False)

    ax.set_xlabel("x (m)")
    ax.set_ylabel("z (m)")
    ax.set_aspect("equal")

    cbar = fig.colorbar(cs, ax=ax, shrink=1)
    cbar.set_label("$w$ (m/s)")

    qos = []
    for i, f in enumerate(qo_files):
        qo = read_qo(f)
        qos.append(qo)

    ax.scatter(qos[0]["x"], qos[0]["z"], marker=qo_markers[0],
                edgecolor="k",facecolor="none",label = r"$\Delta w=0$ m/s"
    )
    ax.scatter(qos[1]["x"], qos[1]["z"], marker=qo_markers[1],
                edgecolor="k",facecolor="none",label = r"$\Delta w=1$ m/s"
    )

    ax.legend(
        frameon=True, facecolor="white", edgecolor="black", 
        fancybox=False, framealpha=1
    )

    plt.show()

def qo_EDF_pos_3D():
    grids = [
        "grids/EDF_qo.json",
        "grids/EDF_bb.json",
        "grids/EDF_efflux_sleeve.json"
    ]

    stl = [
        "data/EDF.stl"
    ]

    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    xs = []
    ys = []
    zs = []

    # Plot QO points
    for grid in grids:
        coords = grid_type_coords(grid)
        for i in range(coords.shape[0]):
            xs.append(coords[i][0])
            ys.append(coords[i][1])
            zs.append(coords[i][2])

    coords0 = grid_type_coords(grids[0])
    coords1 = grid_type_coords(grids[1])
    coords2 = grid_type_coords(grids[2])

    ax.scatter(coords0[:,0],coords0[:,1],coords0[:,2],marker="^",s=2,
               depthshade=False, edgecolor='b', facecolor="none",
               linewidth=0.5, label=r"$\Delta u=1$")
    
    ax.scatter(coords1[:,0],coords1[:,1],coords1[:,2], marker=".", s=0.5,
               depthshade=False, color='k', label=r"$\Delta u=0$")
    
    ax.scatter(coords2[:,0],coords2[:,1],coords2[:,2], marker="o", s=2,
               depthshade=False, edgecolor='k', facecolor="none", linewidth=0.5)

    # Plot STL
    facets = get_facets(stl[0])
    edf_x,edf_y,edf_z = facet_to_coords(facets)
    ax.plot(edf_x,edf_y,edf_z,color="r",linewidth=0.05, label="EDF")
    
    # Plot bounding box lines
    bb_coords = grid_type_coords(grids[1])
    corner1 = [min(bb_coords[:,0]),min(bb_coords[:,1]),min(bb_coords[:,2])]
    corner2 = [max(bb_coords[:,0]),min(bb_coords[:,1]),min(bb_coords[:,2])]
    corner3 = [max(bb_coords[:,0]),max(bb_coords[:,1]),min(bb_coords[:,2])]
    corner4 = [max(bb_coords[:,0]),max(bb_coords[:,1]),max(bb_coords[:,2])]
    corner5 = [min(bb_coords[:,0]),max(bb_coords[:,1]),max(bb_coords[:,2])]
    corner6 = [min(bb_coords[:,0]),min(bb_coords[:,1]),max(bb_coords[:,2])]
    corner7 = [min(bb_coords[:,0]),max(bb_coords[:,1]),min(bb_coords[:,2])]
    corner8 = [max(bb_coords[:,0]),min(bb_coords[:,1]),max(bb_coords[:,2])]

    ax.plot(
        [corner1[0],corner2[0]],[corner1[1],corner2[1]],
        [corner1[2],corner2[2]],color="k",linestyle="--")
    ax.plot(
        [corner2[0],corner3[0]],[corner2[1],corner3[1]],
        [corner2[2],corner3[2]],color="k",linestyle="--")
    ax.plot(
        [corner3[0],corner4[0]],[corner3[1],corner4[1]],
        [corner3[2],corner4[2]],color="k",linestyle="--")
    ax.plot(
        [corner4[0],corner5[0]],[corner4[1],corner5[1]],
        [corner4[2],corner5[2]],color="k",linestyle="--")
    ax.plot(
        [corner5[0],corner6[0]],[corner5[1],corner6[1]],
        [corner5[2],corner6[2]],color="k",linestyle="--")
    ax.plot(
        [corner6[0],corner1[0]],[corner6[1],corner1[1]],
        [corner6[2],corner1[2]],color="k",linestyle="--",
        label=r"Bounding box $\Delta u=0$")

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_zlabel("z (m)")

    ax.set_box_aspect((np.ptp(xs), np.ptp(ys), np.ptp(zs)))
    ax.legend(
        frameon=True, facecolor="white", edgecolor="black", 
        fancybox=False, framealpha=1, loc="upper left"
    )
    ax.set_proj_type("ortho")
    
    """
    # Make background transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # make the grid lines transparent
    ax.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    ax.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    """

    plt.tight_layout()
    plt.show()

def qo_EDF_pos_2D():
    grids = [
        "grids/EDF_qo.json",
        "grids/EDF_bb.json",
        "grids/EDF_efflux_sleeve.json"
    ]

    stl = [
        "data/EDF.stl"
    ]

    fig,(ax1,ax2) = plt.subplots(1, 2, figsize=(12,6))

    xs = []
    ys = []
    zs = []

    # Plot QO points
    for grid in grids:
        coords = grid_type_coords(grid)
        for i in range(coords.shape[0]):
            xs.append(coords[i][0])
            ys.append(coords[i][1])
            zs.append(coords[i][2])

    coords0 = grid_type_coords(grids[0])
    coords1 = grid_type_coords(grids[1])
    coords2 = grid_type_coords(grids[2])

    def plot_qo(axis1:int, axis2:int, ax):
        if ax==ax2:
            s=40
        else:
            s=20

        ax.scatter(coords0[:,axis1],coords0[:,axis2],marker="x",s=s,
                   color='b', linewidth=0.5,
                   label=r"$\Delta u=1$")
        
        ax.scatter(coords1[:,axis1],coords1[:,axis2], marker="o", s=s,
                   edgecolor='k', facecolor="none", label=r"$\Delta u=0$")
        
        ax.scatter(coords2[:,axis1],coords2[:,axis2], marker="o", s=s,
                   edgecolor='k', facecolor="none", linewidth=0.5)

    plot_qo(0,2,ax1)
    plot_qo(1,2,ax2)

    # Plot STL
    facets = get_facets(stl[0])
    edf_x,edf_y,edf_z = facet_to_coords(facets)

    ax1.plot(edf_x,edf_z,color="r",linewidth=0.1, label="Ducted Fan")
    ax2.plot(edf_y,edf_z,color="r",linewidth=0.1, label="Ducted Fan")
    
    # Plot bounding box lines
    bb_coords = grid_type_coords(grids[1])
    corner1 = [min(bb_coords[:,0]),min(bb_coords[:,1]),min(bb_coords[:,2])]
    corner2 = [max(bb_coords[:,0]),min(bb_coords[:,1]),min(bb_coords[:,2])]
    corner3 = [max(bb_coords[:,0]),max(bb_coords[:,1]),min(bb_coords[:,2])]
    corner4 = [max(bb_coords[:,0]),max(bb_coords[:,1]),max(bb_coords[:,2])]
    corner5 = [min(bb_coords[:,0]),max(bb_coords[:,1]),max(bb_coords[:,2])]
    corner6 = [min(bb_coords[:,0]),min(bb_coords[:,1]),max(bb_coords[:,2])]
    corner7 = [min(bb_coords[:,0]),max(bb_coords[:,1]),min(bb_coords[:,2])]
    corner8 = [max(bb_coords[:,0]),min(bb_coords[:,1]),max(bb_coords[:,2])]

    def plot_bb_lines(axis1:int,axis2:int,ax):
        ax.plot(
            [corner1[axis1],corner2[axis1]],[corner1[axis2],corner2[axis2]]
            ,color="k",linestyle="--")
        ax.plot(
            [corner2[axis1],corner3[axis1]],[corner2[axis2],corner3[axis2]],
            color="k",linestyle="--")
        ax.plot(
            [corner3[axis1],corner4[axis1]],[corner3[axis2],corner4[axis2]],
            color="k",linestyle="--")
        ax.plot(
            [corner4[axis1],corner5[axis1]],[corner4[axis2],corner5[axis2]],
            color="k",linestyle="--")
        ax.plot(
            [corner5[axis1],corner6[axis1]],[corner5[axis2],corner6[axis2]],
            color="k",linestyle="--")
        ax.plot(
            [corner6[axis1],corner1[axis1]],[corner6[axis2],corner1[axis2]],
            color="k",linestyle="--",
            label=r"Bounding box $\Delta u=0$")

    plot_bb_lines(0,2,ax1)
    plot_bb_lines(1,2,ax2)

    ax1.set_xlabel("x (m)")
    ax1.set_ylabel("z (m)")
    ax2.set_xlabel("y (m)")
    ax2.set_ylabel("z (m)")

    ax2.set_xlim((-0.08,0.08))
    ax2.set_ylim((-0.08,0.08))

    ax1.set_aspect("equal")
    ax2.set_aspect("equal")
    ax1.set_box_aspect(1)
    ax2.set_box_aspect(1)

    lgnd = ax1.legend(
        frameon=True, facecolor="white", edgecolor="black", 
        fancybox=False, framealpha=1, loc="upper left"
    )
    lgnd.legendHandles[0]._sizes = [80]
    lgnd.legendHandles[1]._sizes = [80]
    lgnd.legendHandles[2]._sizes = [80]
    lgnd.legendHandles[3]._sizes = [80]
    
    plt.tight_layout()

    plt.savefig("C:\\Users\\Jonathan\\OneDrive - University of Surrey\\Year 4\\Individual Project\\Results\\QO Files\\EDF_schematic2.png",dpi=200)
    # plt.show()

def qo_EDF_vel():
    grids = [
        "grids/EDF_qo.json",
        "grids/EDF_bb.json",
        "grids/EDF_efflux_sleeve.json"
    ]

    vel_files = [
        "results/EDF_qo/qo_cylinder.vel1"
    ]
    geom_files = [
        "data/EDF_blockage.json",
        "data/EDF_nacelle.json"
    ]

    variable = "u"

    plane = "xz"
    # bounds = [-5, 5]
    levels = 50

    # init figure
    fig,ax=plt.subplots()

    velcal_data = read_velcal(vel_files[0])
    x=velcal_data[plane[0]]
    y=velcal_data[plane[1]]
    z=velcal_data[variable]

    # Contour plot
    c = contour(ax, x, y, z, cmap="coolwarm", levels=levels, centered=True)
    # c = pcolourmesh(ax,x,y,z,cmap="coolwarm",centered=True)

    plot_geom([ax], geom_files)

    # Plot QO points
    coords0 = grid_type_coords(grids[0])
    coords1 = grid_type_coords(grids[1])
    coords2 = grid_type_coords(grids[2])

    coords0 = np.array([c for c in coords0 if c[1]==0])
    coords1 = np.array([c for c in coords1 if c[1]==0])
    coords2 = np.array([c for c in coords2 if c[1]==0])

    ax.scatter(coords0[:,0],coords0[:,2],marker="x",
                color='b', linewidth=1,s=10,
                label=r"$\Delta u=1$")
    
    ax.scatter(coords1[:,0],coords1[:,2], marker=".",
                edgecolor='k', facecolor="none",label=r"$\Delta u=0$")
    
    ax.scatter(coords2[:,0],coords2[:,2], marker=".",
                edgecolor='k', facecolor="none", linewidth=0.5)


    ax.set_aspect("equal")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("z (m)")
    ax.set_xlim((-0.25,0.45))
    ax.set_ylim((-0.25,0.25))

    lgnd = ax.legend(
        facecolor="white", framealpha=1, fancybox=False, edgecolor="black",
        loc="upper left", fontsize=10)
    lgnd.legendHandles[0]._sizes = [50]
    lgnd.legendHandles[1]._sizes = [50]

    cbar = fig.colorbar(c, ax=ax, shrink=0.70)
    cbar.set_label(r"$u$ (m/s)")

    plt.tight_layout()

def qo_EDF_vel_1D():
    vel_files = [
        "results/EDF_qo/efflux_z.vel1"
    ]

    qo_coords = [
        [[-0.2,0.2],[1,1]],
        [[-0.03045,0.03045],[2,2]],
        [[-0.03401454,0.03401454], [1,1]]
    ]

    fig,ax = plt.subplots()

    x, y, z, u, v, w, Cp = read_vel(vel_files[0])
    # x = normalize_line_length(x,y,z)

    ax.plot(z, u, color='k', label=r"$u$", linestyle="-")

    ax.set_xlabel("z (m)")

    ax.scatter(
        qo_coords[0][0], qo_coords[0][1], marker="o",
        edgecolor="k",facecolor="none", label=r"Bounding box QO $\Delta u=0$"
    )
    ax.scatter(
        qo_coords[2][0], qo_coords[2][1], marker="s",
        edgecolor="k",facecolor="none", label=r"Efflux 'sleeve' QO $\Delta u=0$"
    )
    ax.scatter(
        qo_coords[1][0], qo_coords[1][1], marker="x",
        color='k', label=r"Efflux QO $\Delta u=1$",
        linewidth=1
    )

    ax.set_box_aspect(1)

    ax.set_ylabel("$u$ (m/s)")
    ax.legend(frameon=True, facecolor="white", edgecolor="black",
                   fancybox=False, framealpha=0.8, loc="upper left",
                   ncols=1, columnspacing=0.2, fontsize=9)

    plt.tight_layout()

    pass

def prop_vel_1D():
    vel_files = [
        "results/wing_actuator/CT1_CQ0.2/x=-1.vel1"
    ]

    titles = [
        r"$x=-1.0$"
    ]

    fig,ax = plt.subplots()

    for i, f in enumerate(vel_files):
        x, y, z, u, v, w, Cp = read_vel(f)

        ax.plot(y,u,color='k',linestyle="-",label=r"$u$")
        ax.plot(y,v,color='k',linestyle=":",label=r"$v$")
        ax.plot(y,w,color='k',linestyle="--",label=r"$w$")

    ax.legend(frameon=False)

    ax.set_xlabel("y (m)")
    ax.set_ylabel("Velocity (m/s)")

    ax.set_box_aspect(1)

def prop_vel_zy():
    vel_files = [
        # "results/wing_actuator/CT1_CQ0/zy_x=-2.1.vel1"
        # "results/wing_actuator/CT1_CQ0/zy_x=-1.vel1"
        "results/wing_actuator/CT1_CQ0/zy_x=1.5.vel1"
    ]

    variable = "Cp"
    plane = "zy"
    levels = 50

    radius = 0.5

    # init figure
    fig,ax = plt.subplots()

    # plot actuator disk
    theta = np.linspace(0,2*np.pi,51)
    x_d = []
    y_d = []
    for t in theta:
        x_d.append(radius * np.sin(t))
        y_d.append(radius * np.cos(t))
    
    ax.plot(x_d,y_d,color='k',linestyle="--",label="Propeller disk")

    velcal_data = read_velcal(vel_files[0])
    x=velcal_data[plane[0]]
    y=velcal_data[plane[1]]
    z=velcal_data[variable]

    cs = contour(
        ax, x, y, z, cmap="coolwarm", levels=levels, centered=True, at=0
    )

    ax.set_xlabel("y (m)")
    ax.set_ylabel("z (m)")
    ax.set_aspect("equal")

    cbar = fig.colorbar(cs, ax=ax, shrink=1)
    cbar.set_label("$u$ (m/s)")

    ax.legend(frameon=True, facecolor="white", edgecolor="black",
                   fancybox=False, framealpha=1, fontsize=11)

def prop_vel_xy():
    vel_files = [
        "results/wing_actuator/CT1_CQ0/xy.vel1"
    ]

    variable = "u"
    plane = "xy"
    levels = 50

    # init figure
    fig,ax = plt.subplots()

    velcal_data = read_velcal(vel_files[0])
    x=velcal_data[plane[0]]
    y=velcal_data[plane[1]]
    z=velcal_data[variable]

    cs = contour(
        ax, x, y, z, cmap="coolwarm", levels=levels, centered=True, at=1
    )

    ax.fill([0,1,1,0], [-3,-3,3,3], color="white")   # wing
    ax.plot(
        [-2,-2], [-0.5,0.5], color='k', linestyle="--", label="Propeller")

    ax.plot(
        [-1,-1],[-1,1],color='k',linestyle=":",
        label="Velocity profile sample line"
    )

    ax.set_xlabel("x (m)")
    ax.set_ylabel("z (m)")
    ax.set_aspect("equal")

    cbar = fig.colorbar(cs, ax=ax, shrink=1)
    cbar.set_label("$u$ (m/s)")

    ax.legend(frameon=True, facecolor="white", edgecolor="black",
                   fancybox=False, framealpha=1, fontsize=11)

def nacelle_schematic():
    geom_file = "data/EDF_nacelle.json"

    grids = [
        "grids/EDF_inlet.json",
        "grids/EDF_outlet.json"
    ]

    fig,ax = plt.subplots()
    
    nacelle_line = plot_geom([ax], [geom_file], fill=False)
    nacelle_line.set_label("Nacelle")

    coords = []
    for i, grid in enumerate(grids):
        coords_:np.ndarray = grid_type_coords(grid)

        coords.append(coords_[coords_[:,1]==0])

    ax.scatter(
        coords[0][:,0], coords[0][:,2],color='k',marker = "o",
        edgecolor='k',facecolor="none",label="Inlet Measurement"
    )
    ax.scatter(
        coords[1][:,0], coords[1][:,2],color='k',marker = "^",
        edgecolor='k',facecolor="none",label="Outlet Measurement"
    )

    ax.plot(
        [0.1279963,0.1279963],[0.0358,-0.0358],color='k',linestyle="--",
        label="Propeller"
    )

    ax.set_xlabel("x (m)")
    ax.set_ylabel("z (m)")

    ax.legend(frameon=False)
    ax.set_aspect("equal")
    ax.set_box_aspect(1)

def nacelle_inout_v_profile():
    vel_files = [
        "results/EDF_actuator/mass_flow/wake_2/CT1_inlet.vel1",
        "results/EDF_actuator/mass_flow/wake_2/CT1_outlet.vel1",
        "results/EDF_actuator/mass_flow/wake_2/CT0_inlet.vel1",
        "results/EDF_actuator/mass_flow/wake_2/CT0_outlet.vel1"
    ]

    titles = [
        r"Inlet $C_T=1$",
        r"Outlet $C_T=1$",
        r"Inlet $C_T=0$",
        r"Outlet $C_T=0$"
    ]

    Rs = [0.0428,0.03587086,0.0428,0.03587086]

    markers = ["o","^", 's', 'x']

    fig,ax = plt.subplots()

    for i,f in enumerate(vel_files):
        x,y,z,u,v,w,Cp = read_vel(f)
        coords = np.array([x,y,z,u,v,w]).T
        coords = coords[coords[:,1]==0] # get only points in y axis
        coords = coords[coords[:,2].argsort()] # sort by z

        V = [np.sqrt(coords[j,3]**2+coords[j,4]**2+coords[j,5]**2) for j in range(len(coords))]
        R = Rs[i]
        rR = [coords[j,2]/R for j in range(len(coords))]

        u = coords[:,3]
        v = coords[:,4]
        w = coords[:,5]

        # ax.scatter(rR,u,marker=markers[i],edgecolor='k',facecolor="none",
        #            label=titles[i])
        # ax.scatter(rR,u,marker=markers[i],color='k',label=titles[i])
        ax.plot(rR,u,color='k',linestyle="-")
        
    ax.legend(frameon=False)
    ax.set_box_aspect(1)

    ax.set_ylabel("Velocity Magnitude (m/s)")
    ax.set_xlabel("r/R")

def nacelle_2D_vel():
    
    vel_files = [
        "results/EDF_actuator/mass_flow/no_wake/CT0_2D.vel1"
    ]
    geom_files = [
        "data/EDF_nacelle.json"
    ]

    variable = "u"

    plane = "xz"
    levels = 50

    # init figure
    fig,ax=plt.subplots()

    velcal_data = read_velcal(vel_files[0])
    x=velcal_data[plane[0]]
    y=velcal_data[plane[1]]
    z=velcal_data[variable]

    # Contour plot
    # c = contour(
    #     ax, x, y, z, cmap="coolwarm", levels=levels, centered=True, at=0)
    c = pcolourmesh(ax,x,y,z,cmap="coolwarm",centered=True,at=0)

    plot_geom([ax], geom_files)

    ax.plot(
        [0.1279963,0.1279963],[0.0358,-0.0358],color='k',linestyle="--",
        label="Propeller"
    )
    ax.set_aspect("equal")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("z (m)")
    ax.set_xlim((-0.1,0.4))
    ax.set_ylim((-0.1,0.1))

    cbar = fig.colorbar(c, ax=ax, shrink=0.70)
    cbar.set_label(r"$u$ (m/s)")

    ax.legend(frameon=True, facecolor="white", edgecolor="black",
                   fancybox=False, framealpha=1)


    plt.tight_layout()

def nacelle_mass_flow():
    # inlet 
    mdot_wakes = [
        [0.004943,0.002749,0.002754],[0.004967,0.002787,0.002792],
        [0.00474,0.002594,0.002598],[0.005966,0.003832,0.003838]
    ]

    # inlet & outlet, CT=0, 0.5, 1
    mdot_CT = [
        [0.002754,0.002778,0.002792],[0.002598,0.003263,0.003838]
    ]

    fig,(ax1,ax2) = plt.subplots(ncols=2,nrows=1,sharey=True)

    # wake relaxations
    ax1.plot([0,1,2],mdot_wakes[0],color='k',linestyle='-',marker='o',
             label=r"Inlet, $C_T=0$")
    # ax1.plot([0,1,2],mdot_wakes[1],color='k',linestyle='-',marker='^',
    #          label=r"Inlet, $C_T=1$")
    ax1.plot([0,1,2],mdot_wakes[2],color='r',linestyle='-',marker='^',
             label=r"Outlet, $C_T=0$")
    # ax1.plot([0,1,2],mdot_wakes[3],color='r',linestyle='-',marker='^',
    #          label=r"Outlet, $C_T=1$")
    
    # CT
    ax2.plot([0,0.5,1],mdot_CT[0],color='k',linestyle='-', marker='o',
             label=r"Inlet, $n_{wake}=2$")
    ax2.plot([0,0.5,1],mdot_CT[1],color='r',linestyle='-', marker='^',
             label=r"Outlet, $n_{wake}=2$")

    ax1.set_ylabel(r"$\dot{m}$ (kg/s)")
    ax1.set_xlabel(r"$n_{wake}$ (0=No Wake)")
    ax2.set_xlabel(r"$C_T$")

    ax1.ticklabel_format(style="sci",axis="y",useMathText=True,scilimits=(0,0))
    ax2.ticklabel_format(style="sci",axis="y",useMathText=True,scilimits=(0,0))

    ax1.legend(frameon=False)
    ax2.legend(frameon=False)

    ax1.set_box_aspect(1)
    ax2.set_box_aspect(1)

def nacelle_cp():
    data_files = [
        "results/EDF_actuator/mass_flow/no_wake/CT0_Cp.exp2d",
        "results/EDF_actuator/mass_flow/wake_2/CT0_Cp.exp2d",
        "results/EDF_actuator/mass_flow/wake_2/CT1_Cp.exp2d"
    ]

    curve_names = [
        r"$n_{wake}=0$, $C_T=0$",
        r"$n_{wake}=2$, $C_T=0$",
        r"$n_{wake}=2$, $C_T=1$"
    ]
    colours = ["r","xkcd:azure","lime"]
    markers = ["o","^","s"]
    linestyles = ["--","-.",":"]

    variable = "Cp"
    units = "m"
    data,_ = read_exp2d(data_files)

    fig,ax1 = plt.subplots()
    ax2=ax1.twinx()

    for i, curve in enumerate(data):
        xs = curve["X"].tolist()
        y1s = curve[variable].tolist()

        ax1.plot(
            xs,y1s,color=colours[i],label=curve_names[i],
            linestyle=linestyles[i],linewidth=1
        )

    y2s = curve["Y"].tolist()
    ax2.plot(xs,y2s,color='k',label="Nacelle")

    ax1.set_xlabel("x (m)")
    ax2.set_ylabel("y (m)")
    ax1.set_ylabel(r"$Cp$")

    ax2.set_aspect("equal")
    ax2.set_box_aspect(1)

    ax1.invert_yaxis()
    
    lines1,labels1=ax1.get_legend_handles_labels()
    lines2,labels2=ax2.get_legend_handles_labels()
    ax2.legend(lines1+lines2,labels1+labels2,frameon=False)

#################### Literature Review Plots ####################

def zhang_et_al():
    Cl_d0=[-0.079022069,0.126719175,0.224352311,0.288208327,0.331787409,0.358481262,0.385168452,0.415234021,0.441921211,0.45847993,0.468275228]
    Cl_d15=[0.248108926,0.363086233,0.475037821,0.559757943,0.620272315,0.668683812,0.708018154,0.762481089,0.819969743,0.871406959,0.883509834]
    Cl_d30=[0.451515152,0.551515152,0.660606061,0.760606061,0.842424242,0.909090909,0.96969697,1.039393939,1.112121212,1.175757576,1.2]
    Cd_d0=[0.158893915,0.168721102,0.171856414,0.171631746,0.161339177,0.14994935,0.119557085,0.066834498,0.065488501,0.042925489,0.037106205]
    Cd_d15=[0.16696703,0.182015479,0.189434536,0.187029079,0.181365355,0.170255891,0.155857566,0.138200974,0.118372205,0.085456831,0.076519544]
    Cd_d30=[0.191610284,0.219756428,0.260893099,0.28579161,0.29661705,0.299864682,0.299864682,0.298782138,0.292286874,0.28579161,0.282543978]
    throttle = [0,10,20,30,40,50,60,70,80,90,100]

    fig,(ax1,ax2) = plt.subplots(ncols=2,nrows=1,sharey=False)

    ax1.plot(throttle,Cl_d0, linewidth=1,markersize=4,color='red',
             marker='o',label=r"$\delta =0\degree$",
             markeredgecolor="red",markerfacecolor="none")
    ax1.plot(throttle,Cl_d15,linewidth=1,markersize=4,color='xkcd:azure',
             marker='^',label=r"$\delta =15\degree$",
             markeredgecolor="xkcd:azure",markerfacecolor="none")
    ax1.plot(throttle,Cl_d30,linewidth=1,markersize=4,color='lime',
             marker='s',label=r"$\delta =30\degree$",
             markeredgecolor="lime",markerfacecolor="none")
    ax2.plot(throttle,Cd_d0, linewidth=1,markersize=4,color='red',
             marker='o',label=r"$\delta =0\degree$",
             markeredgecolor="red",markerfacecolor="none")
    ax2.plot(throttle,Cd_d15,linewidth=1,markersize=4,color='xkcd:azure',
             marker='^',label=r"$\delta =15\degree$",
             markeredgecolor="xkcd:azure",markerfacecolor="none")
    ax2.plot(throttle,Cd_d30,linewidth=1,markersize=4,color='lime',
             marker='s',label=r"$\delta =30\degree$",
             markeredgecolor="lime",markerfacecolor="none")

    ax1.text(0.5, -0.25, "(a) Lift Coefficient", size=11, ha="center", transform=ax1.transAxes)
    ax2.text(0.5, -0.25, "(b) Drag Coefficient", size=11, ha="center", transform=ax2.transAxes)

    ax1.set_xlabel("Throttle (%)")
    ax2.set_xlabel("Throttle (%)")
    ax1.set_ylabel(r"$C_L$")
    ax2.set_ylabel(r"$C_D$")

    ax1.legend(frameon=False)
    # ax2.legend(frameon=False)

    ax1.set_box_aspect(1)
    ax2.set_box_aspect(1)

if __name__ == "__main__":
    # blo_tests()
    # qo_test_1D()
    # qo_test_2D()
    # qo_EDF_pos_3D()
    # qo_EDF_pos_2D()
    # qo_EDF_vel()
    # qo_EDF_vel_1D()
    # prop_vel_1D()
    # prop_vel_zy()
    # prop_vel_xy()
    # nacelle_schematic()
    # nacelle_inout_v_profile()
    # nacelle_2D_vel()
    nacelle_mass_flow()
    # nacelle_cp()

    # zhang_et_al()

    plt.tight_layout()
    plt.show()