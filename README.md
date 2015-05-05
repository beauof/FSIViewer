# FSIViewer
FSIViewer - simple visualizer for FSI data

!===============================================================================================

To install, open a shell in the installation directory and do: make user && make

Now, you should be able to start the visualizer with:
    python main.py

In the subdirectory, there is a default and personal configuration file of the following format:
!===============================================================================================
Installation directiory of FSI visualizer
Default directory
Data folder (where you keep your *.D files)
Mesh folder (where you keep your *.X/*.T files)
Filename for fluid space *.D files
Filename for velocity *.D files
Filename for fluid pressure *.D files
Filename for fluid vorticity *.D files (note: filename if file exists, otherwise computed & saved as filename)
Do we have to transform the fluid pressure back to include hydrostatic pressure contributions?
Filename for solid space *.D files
Filename for displacement *.D files
Filename for solid pressure *.D files
Is current configuration the reference configuration + displacement variable?
Topology file prefix (fluid)
Topology file prefix (solid)
Set visualizer output to DEBUG
Fluid density in format 1.0e-3
Gravitational acceleration in x-direction in format 1.0e-3
Gravitational acceleration in y-direction in format 1.0e-3
Gravitational acceleration in z-direction in format 1.0e-3
Visualize fluid
Visualize solid
Visualize interface
Filename for domain velocity *.D files
!===============================================================================================

Further, cython files (*.pyx) can be profiled e.g.:
  cython -a cythonfile.pyx
  firefox cythonfile.html &


