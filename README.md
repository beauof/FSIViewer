# FSIViewer
FSIViewer - simple visualizer for FSI data  <br />
 <br />
!=============================================================================================== <br />
 <br />
To install, open a shell in the installation directory and do: <br />
    make user && make <br />
 <br />
Now, you should be able to start the visualizer with: <br />
    python main.py <br />
 <br />
In the subdirectory, there is a default and personal configuration file of the following format: <br />
!=============================================================================================== <br />
Installation directiory of FSI visualizer <br />
Default directory <br />
Data folder (where you keep your *.D files) <br />
Mesh folder (where you keep your *.X/*.T files) <br />
Filename for fluid space *.D files <br />
Filename for velocity *.D files <br />
Filename for fluid pressure *.D files <br />
Filename for fluid vorticity *.D files (note: filename if file exists, otherwise computed & saved as filename) <br />
Do we have to transform the fluid pressure back to include hydrostatic pressure contributions? <br />
Filename for solid space *.D files <br />
Filename for displacement *.D files <br />
Filename for solid pressure *.D files <br />
Is current configuration the reference configuration + displacement variable? <br />
Topology file prefix (fluid) <br />
Topology file prefix (solid) <br />
Set visualizer output to DEBUG <br />
Fluid density in format 1.0e-3 <br />
Gravitational acceleration in x-direction in format 1.0e-3 <br />
Gravitational acceleration in y-direction in format 1.0e-3 <br />
Gravitational acceleration in z-direction in format 1.0e-3 <br />
Visualize fluid <br />
Visualize solid <br />
Visualize interface <br />
Filename for domain velocity *.D files <br />
!=============================================================================================== <br />
 <br />
Further, cython files (*.pyx) can be profiled e.g.: <br />
  cython -a cythonfile.pyx <br />
  firefox cythonfile.html & <br />
 <br />

