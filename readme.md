## NEWPAN Tools

(NEWPAN the panel method)

### **Grid Generate:**
- Generates various NEWPAN grid files including VELCAL .scn, QO .qo/.qom, OFFBODY .spt
- Accepts cuboid and cylindrical grids - that includes 1D lines, 2D quadrilateral or circular planes, 3D shapes.
- Multiple grids can be generated on top of each other.
- Example grid definitions given in /example grids.

### **VELCAL Vis 1D:**
- Read and plot VELCAL data on a straight line (u,v,w,Cp).

![image](https://github.com/jj-foster/NEWPAN-tools/assets/79290428/4c70f22b-5147-4850-8f8a-fdafeb7e74fc)

### **VELCAL Vis 2D:**
- Read and plot VELCAL data in 2D for contour plots (u,v,w,Cp).

![image](https://github.com/jj-foster/NEWPAN-tools/assets/79290428/2d58aa80-7389-449b-b6d3-2dbaeb59aa42)

### **Surface Variable 2D:**
- Read and plot .exp2d files from exported surface data (u,v,w,Cp,etc...)

![image](https://github.com/jj-foster/NEWPAN-tools/assets/79290428/c4ccded9-6bfc-4cbc-8e9e-0923d28d7e1c)

### **Mass Flow Rate:**
- Calculates mass flow rate through a 2D grid.
- Essentially calculates the area weighted average velocity.
- Requires VELCAL data from a grid, and the grid definition file.

### **STL Read:**
- Read and plot GEMS exported .stl files.
- Just in case you wanted to make some really snazzy plots.

![image](https://github.com/jj-foster/NEWPAN-tools/assets/79290428/f71f15cb-0456-4b0c-9787-067528e533a2)

