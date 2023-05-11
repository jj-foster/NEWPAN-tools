## NEWPAN stuff

(NEWPAN the panel method)

### **Grid Generate:**
- Generates various NEWPAN grid files including VELCAL .scn, QO .qo/.qom, OFFBODY .spt
- Accepts cuboid and cylindrical grids - that includes 1D lines, 2D quadrilateral or circular planes, 3D shapes.
- Multiple grids can be generated on top of each other.
- Example grid definitions given in /example grids.

### **VELCAL Vis 1D:**
- Read and plot VELCAL data on a straight line (u,v,w,Cp).

### **VELCAL Vis 2D:**
- Read and plot VELCAL data in 2D for contour plots (u,v,w,Cp).

### **Surface Variable 2D:**
- Read and plot .exp2d files from exported surface data (u,v,w,Cp,etc...)

### **Mass Flow Rate:**
- Calculates mass flow rate through a 2D grid.
- Essentially calculates the area weighted average velocity.
- Requires VELCAL data from a grid, and the grid definition file.

### **STL Read:**
- Read and plot NEWPAN exported .stl files.
- Just in case you wanted to make some really snazzy plots.

