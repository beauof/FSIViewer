# FSIViewer
FSIViewer - simple visualizer for FSI data  <br />
 <br />
!=============================================================================================== <br />
 <br />
The software has only been tested with Linux operating systems. <br />
 <br />
Make sure that the following packages are installed: <br />
gcc <br />
python2.x <br />
python-tk <br />
python-imaging-tk (or: python-pil.imagetk) <br />
python-dev <br />
python-numpy <br />
cython <br />
vtk6 <br />
libvtk6-dev <br />
 <br />
Note: This software has been developed with VTK 5.8.0. It was tested with VTK 6.2.0. <br />
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
!=============================================================================================== <br />
 <br />
Further, cython files (*.pyx) can be profiled e.g.: <br />
  cython -a cythonfile.pyx <br />
  firefox cythonfile.html & <br />
!=============================================================================================== <br />
!=============================================================================================== <br />
 <br />
 <br />
Known bugs:
 <br />
 <br />
!=============================================================================================== <br />
 <br />
ImportError: No module named vtkCommonCorePython <br />
 <br />
Add the following two lines to your ~/.bashrc:
 <br />
export LD_LIBRARY_PATH=/usr/lib/python2.7/dist-packages/vtk:$LD_LIBRARY_PATH
 <br />
export PYTHONPATH=/usr/lib/python2.7/dist-packages/vtk:$PYTHONPATH
 <br />
!=============================================================================================== <br />
 <br />
_tkinter.TclError: couldn't load file "libvtkRenderingPythonTkWidgets-6.2.so": libvtkRenderingPythonTkWidgets-6.2.so: cannot open shared object file: No such file or directory
 <br />
 <br />
In: /usr/lib/python2.7/dist-packages/vtk (or similar, depending on your installation), do:
 <br />
sudo ln -s libvtkRenderingPythonTkWidgets.x86_64-linux-gnu.so libvtkRenderingPythonTkWidgets-6.2.so
 <br />
 <br />
