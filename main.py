import logging
import time
from fsi import *
from gui import *
import vtk
import Tkinter
import tkFileDialog
import tkColorChooser
import ttk
from vtk.tk.vtkTkRenderWindowInteractor import vtkTkRenderWindowInteractor
import sys
import tkFont
from PIL import Image, ImageTk
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
import os.path
import getpass




sys.dont_write_bytecode = True

#
def main():
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" \
          ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n" \
          "FSIViewer - simple visualizer for FSI data\n\n" \
          ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" \
          ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n" \
          "Copyright (C) 2015 Andreas Hessenthaler\n" \
          "                   University of Stuttgart\n" \
          "                   hessenthaler@mechbau.uni-stuttgart.de\n\n" \
          ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" \
          ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n" \
          "This program is free software: you can redistribute it and/" \
          "or modify it under the terms of the\n" \
          "GNU Lesser General Public License as published by the Free " \
          "Software Foundation, either version 3\n" \
          "of the License, or (at your option) any later version.\n\n" \
          "This program is distributed in the hope that it will be use" \
          "ful, but WITHOUT ANY WARRANTY; without\n" \
          "even the implied warranty of MERCHANTABILITY or FITNESS FOR" \
          " A PARTICULAR PURPOSE.  See the GNU\n" \
          "Lesser General Public License for more details.\n\n" \
          "You should have received a copy of the GNU Lesser General " \
          "Public License along with this program.\n" \
          "If not, see <http://www.gnu.org/licenses/>.\n\n" \
          "Please state the original author.\n\n" \
          ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" \
          ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n" \
          "File I/O:\n" \
          " Numpy: http://www.numpy.org/\n" \
          " Cython: http://cython.org/\n" \
          "GUI:\n" \
          " Tkinter: http://www.tkdocs.com/tutorial/index.html\n" \
          " Silk icon set 1.3 by Mark James: http://www.famfamfam.com/lab/icons/silk/\n" \
          " VTK: http://www.vtk.org/\n\n" \
          "Make sure that the following packages are installed:\n" \
          "gcc\n" \
          "python2.x\n" \
          "python-tk\n" \
          "python-imaging-tk\n" \
          "python-dev\n" \
          "python-numpy\n" \
          "cython\n" \
          "vtk\n\n" \
          "Note: This software has been developed with VTK 5.8.0\n" \
          "You are using VTK", vtk.vtkVersion().GetVTKVersion(), \
          "\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" \
          ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n" \
    
    # create window
    window = gui()
    window.root = Tkinter.Tk()
    
    # initialise visualization
    visualization = fsi()
    # set username and read configuration
    visualization.username = getpass.getuser()
    if (os.path.exists("config/"+visualization.username+".config")):
        print "User-specific configuration file found:\n", \
            " config/"+visualization.username+".config", \
            "\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" \
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
        visualization.readConfiguration( \
            "config/"+visualization.username+".config")
    elif (os.path.exists("config/default.config")):
        print "Default configuration file found:\n", \
            ". /config/default.config", \
            "\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" \
            ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
        visualization.readConfiguration( \
            "config/default.config")
    else:
        print "No configuration file found. Please create one."
    
    # get vtk version
    visualization.vtkVersionMajor = vtk.vtkVersion().GetVTKMajorVersion()
    visualization.vtkVersionMinor = vtk.vtkVersion().GetVTKMinorVersion()
    visualization.vtkVersionBuild = vtk.vtkVersion().GetVTKBuildVersion()
    
    # set debug level
    if visualization.DEBUG: logging.basicConfig(level=logging.DEBUG)
    else: logging.basicConfig(level=logging.INFO)
    
    
    window.configureRoot()
    window.configureGUI()
    window.mainframe = ttk.Frame(window.root, borderwidth=5, style='My.TFrame')
    window.configureMainframe()
    window.toolbar = ttk.Frame(window.mainframe, borderwidth=5, style='My.TFrame')
    window.configureToolbar(visualization.installDirectory)
    window.loadBtn = ttk.Button(window.toolbar, image=window.useLoadIcon, \
        command=lambda:visualization.defineSequence(window), style='My.TButton')
    window.loadBtn.pack(side=Tkinter.LEFT, fill=Tkinter.X, padx=1)
    window.refreshConfigBtn = ttk.Button(window.toolbar, \
        image=window.useRefreshConfigIcon, \
        command=visualization.refreshConfiguration, \
        style='My.TButton')
    window.refreshConfigBtn.pack(side=Tkinter.LEFT, fill=Tkinter.X, padx=1)
    window.quitBtn = ttk.Button(window.toolbar, image=window.useQuitIcon, \
        command=quit, style='My.TButton')
    window.quitBtn.pack(side=Tkinter.LEFT, fill=Tkinter.X, padx=1)
    
    ## tabs
    window.notebook = ttk.Notebook(window.mainframe, style='My.TNotebook')
    window.configureNotebook()
    # fluid tab
    window.subframeF = ttk.Frame(window.notebook, style='My.TNotebook.Tab')
    window.subframeF.pack()
    window.notebook.add(window.subframeF, text="F", state="disabled")
    visualization.showF = Tkinter.StringVar()
    visualization.showF.set("vel")
    ttk.Radiobutton(window.subframeF, text="pressure", \
        command=visualization.updateFluid, \
        variable=visualization.showF, value="presF", \
        style='My.TRadiobutton').grid(column=0, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text="velocity", \
        command=visualization.updateFluid, \
        variable=visualization.showF, value="vel", \
        style='My.TRadiobutton').grid(column=0, row = 1, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text="domain velocity", \
        command=visualization.updateFluid, \
        variable=visualization.showF, value="wel", \
        style='My.TRadiobutton').grid(column=0, row = 2, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text="vorticity", \
        command=visualization.updateFluid, \
        variable=visualization.showF, value="vort", \
        style='My.TRadiobutton').grid(column=0, row = 3, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text="tet quality", \
        command=visualization.updateFluid, \
        variable=visualization.showF, value="quality", \
        style='My.TRadiobutton').grid(column=0, row = 4, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text="directional scalar", \
        command=visualization.updateFluid, \
        variable=visualization.showF, value="phi", \
        style='My.TRadiobutton').grid(column=0, row = 5, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text="none", \
        command=visualization.updateFluid, \
        variable=visualization.showF, value="none", \
        style='My.TRadiobutton').grid(column=0, row = 6, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    
    ttk.Separator(window.subframeF, orient=Tkinter.HORIZONTAL).grid(column=0, \
        row = 7, sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    
    visualization.clipFnormal = Tkinter.StringVar()
    visualization.clipFnormal.set('-1')
    ttk.Radiobutton(window.subframeF, text='full', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value="-1", \
        style='My.TRadiobutton').grid(column=0, row = 8, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text='clip w/ normal x (elem)', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value="xe", \
        style='My.TRadiobutton').grid(column=0, row = 9, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text='clip w/ normal y (elem)', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value="ye", \
        style='My.TRadiobutton').grid(column=0, row = 10, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text="clip w/ normal z (elem)", \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value='ze', \
        style='My.TRadiobutton').grid(column=0, row = 11, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text='clip w/ normal x', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value='x', \
        style='My.TRadiobutton').grid(column=0, row = 17, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text='clip w/ normal y', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value='y', \
        style='My.TRadiobutton').grid(column=0, row = 18, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text='clip w/ normal z', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value='z', \
        style='My.TRadiobutton').grid(column=0, row = 19, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text='plane w/ normal x', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value='a', \
        style='My.TRadiobutton').grid(column=0, row = 20, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text='plane w/ normal y', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value='b', \
        style='My.TRadiobutton').grid(column=0, row = 21, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text='plane w/ normal z', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value='c', \
        style='My.TRadiobutton').grid(column=0, row = 22, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    
    ttk.Radiobutton(window.subframeF, text='vortex structure', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value='vortex-structure', \
        style='My.TRadiobutton').grid(column=0, row = 23, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
#    ttk.Separator(window.subframeF, orient=Tkinter.HORIZONTAL).grid(column=0, \
#        row = 23, sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    
    visualization.boolEdgesF = Tkinter.BooleanVar()
    visualization.boolEdgesF.set(False)
    ttk.Checkbutton(window.subframeF, \
        variable=visualization.boolEdgesF, text='Show tri/tet edges', \
        command=visualization.edgesOnOffF, \
        style='My.TCheckbutton').grid(column=0, row = 24, \
        sticky=(Tkinter.W, Tkinter.E))
    
    ttk.Separator(window.subframeF, orient=Tkinter.HORIZONTAL).grid(column=0, \
        row = 25, sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    visualization.boolShowScalarBarF = Tkinter.BooleanVar()
    visualization.boolShowScalarBarF.set(False)
    ttk.Checkbutton(window.subframeF, \
        variable=visualization.boolShowScalarBarF, text='Show scalarbar', \
        command=visualization.scalarBarOnOffF, \
        style='My.TCheckbutton').grid(column=0, row = 26, \
        sticky=(Tkinter.W, Tkinter.E))
    
    window.componentFrameF = ttk.Frame(window.subframeF, style='My.TFrame')
    window.componentFrameF.grid(column=0, row=27, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    ttk.Label(window.componentFrameF, width=15, text="Use component:", \
        style='My.TLabel').grid(column=0, row=0, sticky=Tkinter.S)
    
    visualization.componentDropDownF = ttk.Combobox(window.componentFrameF, \
        justify=Tkinter.LEFT, width=10)
    visualization.componentDropDownF.grid(column=1, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    visualization.componentDropDownF.bind('<<ComboboxSelected>>', \
        visualization.componentUpdateF)
    visualization.componentDropDownF['values'] = \
        ("magnitude", "x", "y", "z")
    visualization.componentDropDownF.set("magnitude")
    
    ttk.Checkbutton(window.componentFrameF, \
        variable=visualization.boolAutoRangeF, text='Auto-range', \
        command=lambda:visualization.enableUserRangeF(window), \
        style='My.TCheckbutton').grid(column=0, row=1, \
        sticky=(Tkinter.W, Tkinter.E))
    window.entryMinF = ttk.Entry(window.componentFrameF, width=5, \
        textvariable=visualization.userMinF, \
        justify=Tkinter.RIGHT, state=["disabled"])
    window.entryMinF.grid(column=0, row=2, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    window.entryMaxF = ttk.Entry(window.componentFrameF, width=5, \
        textvariable=visualization.userMaxF, \
        justify=Tkinter.RIGHT, state=["disabled"])
    window.entryMaxF.grid(column=1, row=2, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    
    
    visualization.boolShowOutlineF = Tkinter.BooleanVar()
    visualization.boolShowOutlineF.set(False)
    ttk.Checkbutton(window.subframeF, \
        variable=visualization.boolShowOutlineF, text='Show outline', \
        command=visualization.outlineOnOffF, \
        style='My.TCheckbutton').grid(column=0, row = 28, \
        sticky=(Tkinter.W, Tkinter.E))
    
    ttk.Separator(window.subframeF, orient=Tkinter.HORIZONTAL).grid(column=0, \
        row = 29, sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    
    labelsDropDown = ttk.Combobox(window.subframeF, \
        textvariable=visualization.labelVar)
    labelsDropDown.grid(column=0, row = 30, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
#    labelsDropDown.bind('<<ComboboxSelected>>', modifyLabelF)
    labelsDropDown['values'] = ('No label', 'Node ID', 'Node coordinates', 'Cell ID', 'Pressure', 'Velocity')
    labelsDropDown.set('no label')
    
    ttk.Radiobutton(window.subframeF, text='plane w/ normal x (resample)', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value='i', \
        style='My.TRadiobutton').grid(column=0, row = 31, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text='plane w/ normal y (resample)', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value='j', \
        style='My.TRadiobutton').grid(column=0, row = 32, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeF, text='plane w/ normal z (resample)', \
        command=visualization.updateFluid, \
        variable=visualization.clipFnormal, value='k', \
        style='My.TRadiobutton').grid(column=0, row = 33, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    
    # solid tab
    window.subframeS = ttk.Frame(window.notebook, style='My.TNotebook.Tab')
    window.subframeS.pack()
    window.notebook.add(window.subframeS, text="S", state="disabled")
    visualization.showS = Tkinter.StringVar()
    visualization.showS.set("disp")
    ttk.Radiobutton(window.subframeS, text="pressure", \
        command=visualization.updateSolid, \
        variable=visualization.showS, value="presS", \
        style='My.TRadiobutton').grid(column=0, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeS, text="displacement", \
        command=visualization.updateSolid, \
        variable=visualization.showS, value="disp", \
        style='My.TRadiobutton').grid(column=0, row = 1, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeS, text="velocity", \
        command=visualization.updateSolid, \
        variable=visualization.showS, value="vel", \
        style='My.TRadiobutton').grid(column=0, row = 2, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeS, text="Cauchy stress", \
        command=visualization.updateSolid, \
        variable=visualization.showS, value="cauchy", \
        style='My.TRadiobutton').grid(column=0, row = 3, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeS, text="tet quality", \
        command=visualization.updateSolid, \
        variable=visualization.showS, value="quality", \
        style='My.TRadiobutton').grid(column=0, row = 4, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeS, text="none", \
        command=visualization.updateSolid, \
        variable=visualization.showS, value="none", \
        style='My.TRadiobutton').grid(column=0, row = 5, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Separator(window.subframeS, \
        orient=Tkinter.HORIZONTAL).grid(column=0, row = 6, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    visualization.boolEdgesS = Tkinter.BooleanVar()
    visualization.boolEdgesS.set(False)
    ttk.Checkbutton(window.subframeS, \
        variable=visualization.boolEdgesS, text='Show tri/tet edges', \
        command=visualization.edgesOnOffS, \
        style='My.TCheckbutton').grid(column=0, row = 7, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    visualization.boolShowScalarBarS = Tkinter.BooleanVar()
    visualization.boolShowScalarBarS.set(False)
    ttk.Checkbutton(window.subframeS, \
        variable=visualization.boolShowScalarBarS, text='Show scalarbar', \
        command=visualization.scalarBarOnOffS, \
        style='My.TCheckbutton').grid(column=0, row = 8, \
        sticky=(Tkinter.W, Tkinter.E))
    
    window.componentFrameS = ttk.Frame(window.subframeS, style='My.TFrame')
    window.componentFrameS.grid(column=0, row=9, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    ttk.Label(window.componentFrameS, width=15, text="Use component:", \
        style='My.TLabel').grid(column=0, row=0, sticky=Tkinter.S)
    visualization.componentDropDownS = ttk.Combobox(window.componentFrameS, \
        justify=Tkinter.LEFT, width=10)
    visualization.componentDropDownS.grid(column=1, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    visualization.componentDropDownS.bind('<<ComboboxSelected>>', \
        visualization.componentUpdateS)
    visualization.componentDropDownS['values'] = \
        ("magnitude", "x", "y", "z")
    visualization.componentDropDownS.set("magnitude")
    
    ttk.Checkbutton(window.componentFrameS, \
        variable=visualization.boolAutoRangeS, text='Auto-range', \
        command=lambda:visualization.enableUserRangeS(window), \
        style='My.TCheckbutton').grid(column=0, row=1, \
        sticky=(Tkinter.W, Tkinter.E))
    window.entryMinS = ttk.Entry(window.componentFrameS, width=5, \
        textvariable=visualization.userMinS, \
        justify=Tkinter.RIGHT, state=["disabled"])
    window.entryMinS.grid(column=0, row=2, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    window.entryMaxS = ttk.Entry(window.componentFrameS, width=5, \
        textvariable=visualization.userMaxS, \
        justify=Tkinter.RIGHT, state=["disabled"])
    window.entryMaxS.grid(column=1, row=2, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    
    visualization.boolShowOutlineS = Tkinter.BooleanVar()
    visualization.boolShowOutlineS.set(False)
    ttk.Checkbutton(window.subframeS, \
        variable=visualization.boolShowOutlineS, text='Show outline', \
        command=visualization.outlineOnOffS, \
        style='My.TCheckbutton').grid(column=0, row = 16, \
        sticky=(Tkinter.W, Tkinter.E))
    visualization.boolShowOnReferenceS = Tkinter.BooleanVar()
    visualization.boolShowOnReferenceS.set(False)
    ttk.Checkbutton(window.subframeS, \
        variable=visualization.boolShowOnReferenceS, text='Use reference configuration', \
        command=visualization.referenceOnOffS, \
        style='My.TCheckbutton').grid(column=0, row = 17, \
        sticky=(Tkinter.W, Tkinter.E))
    
    ttk.Separator(window.subframeS, orient=Tkinter.HORIZONTAL).grid(column=0, \
        row = 18, sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    
    window.nodeFrameS = ttk.Frame(window.subframeS, style='My.TFrame')
    window.nodeFrameS.grid(column=0, row=19, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    nodeButtonS = ttk.Button(window.nodeFrameS, \
        command=visualization.updateNodeS, \
        text="Track node:", style='My.TButton')
    nodeButtonS.grid(column=0, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    window.entryNodeS = ttk.Entry(window.nodeFrameS, width=6, \
        textvariable=visualization.nodeS, \
        justify=Tkinter.RIGHT)
    window.entryNodeS.grid(column=1, row=0, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E, Tkinter.N))
    ttk.Entry(window.nodeFrameS, width=8, \
        textvariable=visualization.nodeSrefX, \
        justify=Tkinter.RIGHT).grid( \
        column=0, row=1, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E, Tkinter.N))
    ttk.Entry(window.nodeFrameS, width=8, \
        textvariable=visualization.nodeSrefY, \
        justify=Tkinter.RIGHT).grid( \
        column=0, row=2, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E, Tkinter.N))
    ttk.Entry(window.nodeFrameS, width=8, \
        textvariable=visualization.nodeSrefZ, \
        justify=Tkinter.RIGHT).grid( \
        column=0, row=3, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E, Tkinter.N))
    ttk.Entry(window.nodeFrameS, width=8, \
        textvariable=visualization.nodeSx, \
        justify=Tkinter.RIGHT).grid( \
        column=1, row=1, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E, Tkinter.N))
    ttk.Entry(window.nodeFrameS, width=8, \
        textvariable=visualization.nodeSy, \
        justify=Tkinter.RIGHT).grid( \
        column=1, row=2, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E, Tkinter.N))
    ttk.Entry(window.nodeFrameS, width=8, \
        textvariable=visualization.nodeSz, \
        justify=Tkinter.RIGHT).grid( \
        column=1, row=3, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E, Tkinter.N))
    
    
    # interface tab
    window.subframeI = ttk.Frame(window.notebook, style='My.TNotebook.Tab')
    window.subframeI.pack()
    window.notebook.add(window.subframeI, text="I", state="disabled")
    visualization.showI = Tkinter.StringVar()
    visualization.showI.set("lm")
    
    ttk.Radiobutton(window.subframeI, text='Lagrange multiplier', \
        command=visualization.updateInterface, \
        variable=visualization.showI, value='lm', \
        style='My.TRadiobutton').grid(column=0, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Radiobutton(window.subframeI, text='none', \
        command=visualization.updateInterface, \
        variable=visualization.showI, value='none', \
        style='My.TRadiobutton').grid(column=0, row = 3, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Separator(window.subframeI, \
        orient=Tkinter.HORIZONTAL).grid(column=0, row = 4, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    
    visualization.boolEdgesI = Tkinter.BooleanVar()
    visualization.boolEdgesI.set(False)
    ttk.Checkbutton(window.subframeI, \
        variable=visualization.boolEdgesI, text='Show tri/tet edges', \
        command=visualization.edgesOnOffI, \
        style='My.TCheckbutton').grid(column=0, row = 5, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    
    visualization.boolShowScalarBarI = Tkinter.BooleanVar()
    visualization.boolShowScalarBarI.set(False)
    ttk.Checkbutton(window.subframeI, \
        variable=visualization.boolShowScalarBarI, text='Show scalarbar', \
        command=visualization.scalarBarOnOffI, \
        style='My.TCheckbutton').grid(column=0, row = 6, \
        sticky=(Tkinter.W, Tkinter.E))
    
    window.componentFrameI = ttk.Frame(window.subframeI, style='My.TFrame')
    window.componentFrameI.grid(column=0, row=7, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    ttk.Label(window.componentFrameI, width=15, text="Use component:", \
        style='My.TLabel').grid(column=0, row=0, sticky=Tkinter.S)
    visualization.componentDropDownI = ttk.Combobox(window.componentFrameI, \
        justify=Tkinter.LEFT, width=10)
    visualization.componentDropDownI.grid(column=1, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    visualization.componentDropDownI.bind('<<ComboboxSelected>>', \
        visualization.componentUpdateI)
    visualization.componentDropDownI['values'] = \
        ("magnitude", "x", "y", "z")
    visualization.componentDropDownI.set("magnitude")
    
    ttk.Checkbutton(window.componentFrameI, \
        variable=visualization.boolAutoRangeI, text='Auto-range', \
        command=lambda:visualization.enableUserRangeI(window), \
        style='My.TCheckbutton').grid(column=0, row=1, \
        sticky=(Tkinter.W, Tkinter.E))
    window.entryMinI = ttk.Entry(window.componentFrameI, width=5, \
        textvariable=visualization.userMinI, \
        justify=Tkinter.RIGHT, state=["disabled"])
    window.entryMinI.grid(column=0, row=2, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    window.entryMaxI = ttk.Entry(window.componentFrameI, width=5, \
        textvariable=visualization.userMaxI, \
        justify=Tkinter.RIGHT, state=["disabled"])
    window.entryMaxI.grid(column=1, row=2, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    
    visualization.boolShowOutlineI = Tkinter.BooleanVar()
    visualization.boolShowOutlineI.set(False)
    ttk.Checkbutton(window.subframeI, \
        variable=visualization.boolShowOutlineI, text='Show outline', \
        command=visualization.outlineOnOffI, \
        style='My.TCheckbutton').grid(column=0, row = 16, \
        sticky=(Tkinter.W, Tkinter.E))
    
    # viewer tab
    window.subframeV = ttk.Frame(window.notebook, style='My.TNotebook.Tab')
    window.subframeV.pack()
    window.notebook.add(window.subframeV, text="Viewer      ", state="normal")
    
    visualization.backgroundDropDown = ttk.Combobox(window.subframeV)
    visualization.backgroundDropDown.grid(column=0, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    visualization.backgroundDropDown.bind('<<ComboboxSelected>>', \
        visualization.modifyBackground)
    visualization.backgroundDropDown['values'] = \
        ('black background', 'black-white background', \
         'white background', 'white-black background', \
         'custom background', 'custom-white background')
    visualization.backgroundDropDown.set('black-white background')
    ttk.Button(window.subframeV, \
        command=lambda:visualization.modifyCamera(window), \
        text="Modify camera view", style='My.TButton').grid(column=0, row = 2, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    ttk.Button(window.subframeV, \
        command=visualization.screenshot, \
        text="Screenshot", style='My.TButton').grid(column=0, row = 4, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    #ttk.Separator(window.subframeV, orient=Tkinter.HORIZONTAL).grid(column=0, \
    #    row = 5, sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    fromFrame = ttk.Frame(window.subframeV, style='My.TFrame')
    fromFrame.grid(column=0, row=7, sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    toFrame   = ttk.Frame(window.subframeV, style='My.TFrame')
    toFrame.grid(column=0, row=8, sticky=(Tkinter.W, Tkinter.N, Tkinter.E))
    visualization.animateFromStr = Tkinter.StringVar()
    visualization.animateToStr   = Tkinter.StringVar()
    visualization.animateFromStr.set(str(visualization.animateFromT))
    visualization.animateToStr.set(str(visualization.animateToT))
    ttk.Label(fromFrame, width=7, text="from:", \
        style='My.TLabel').grid(column=0, row=0, sticky=Tkinter.S)
    ttk.Entry(fromFrame, width=10, textvariable=visualization.animateFromStr, \
        justify=Tkinter.RIGHT).grid(column=1, row=0, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    ttk.Label(toFrame, width=7, text="to:  ", \
        style='My.TLabel').grid(column=0, row=0, sticky=Tkinter.S)
    ttk.Entry(toFrame, width=10, textvariable=visualization.animateToStr, \
        justify=Tkinter.RIGHT).grid(column=1, row=0, \
        sticky=(Tkinter.W, Tkinter.N, Tkinter.E))
    screenshotFrame = ttk.Frame(window.subframeV, style='My.TFrame')
    screenshotFrame.grid(column=0, row=9, sticky=(Tkinter.W, Tkinter.E))
    visualization.screenshotFolderStr = Tkinter.StringVar()
    visualization.screenshotFolderStr.set("png/")
    ttk.Label(screenshotFrame, width=7, text="folder:", \
        style='My.TLabel').grid(column=0, row=0, sticky=Tkinter.S)
    ttk.Entry(screenshotFrame, width=10, \
        textvariable=visualization.screenshotFolderStr, \
        justify=Tkinter.RIGHT).grid(column=1, row=0, \
        sticky=(Tkinter.W, Tkinter.S, Tkinter.E))
    animateSaveFrame = ttk.Frame(window.subframeV)
    animateSaveFrame.grid(column=0, row=10, sticky=(Tkinter.W, Tkinter.E))
    animateButton = ttk.Button(animateSaveFrame, \
        command=visualization.animate, \
        text="Animate", style='My.TButton')
    animateButton.grid(column=0, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    saveButton = ttk.Button(animateSaveFrame, \
        command=visualization.animateNsave, \
        text="Animate & save", style='My.TButton')
    saveButton.grid(column=1, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    phasesFrame = ttk.Frame(window.subframeV, style='My.TFrame')
    phasesFrame.grid(column=0, row=15, sticky=(Tkinter.W, Tkinter.E))
    probeButtonI = ttk.Button(phasesFrame, \
        command=lambda:visualization.phaseIorII(window, 1), \
        text="Phase I", style='My.TButton').grid(column=0, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    probeButtonII = ttk.Button(phasesFrame, \
        command=lambda:visualization.phaseIorII(window, 2), \
        text="Phase II", style='My.TButton').grid(column=1, row = 0, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    
    
    ttk.Button(window.subframeV, \
        command=lambda:visualization.displayPoints(window), \
        text="Display points", style='My.TButton').grid(column=0, row = 20, \
        sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    
    visualization.boolShowPoints = Tkinter.BooleanVar()
    visualization.boolShowPoints.set(False)
    visualization.showPointsCheckbutton = ttk.Checkbutton(window.subframeV, \
        variable=visualization.boolShowPoints, text='Show points', \
        command=visualization.pointsOnOff, \
        style='My.TCheckbutton').grid(column=0, row = 21, \
        sticky=(Tkinter.W, Tkinter.E))
    
    visualization.configureCamera()
    visualization.renderer = vtk.vtkRenderer()
    visualization.configureRenderer()
    visualization.addSphere()
    
    visualization.renderWindow = vtk.vtkRenderWindow()
    visualization.renderWindow.AddRenderer(visualization.renderer)
    
    visualization.renderWidget = vtkTkRenderWindowInteractor(window.mainframe, \
        rw=visualization.renderWindow)
    visualization.renderWidget.grid(column=2, row=0, rowspan=window.gridy-2, \
        columnspan=window.gridx-2, \
        sticky = (Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
    visualization.renderWidget.focus()
    
    # create slider for modifying current time
    visualization.timeSlider = Tkinter.Scale(window.mainframe, \
        from_=visualization.fromT, to=visualization.toT, \
        resolution=visualization.increment, \
        orient=Tkinter.HORIZONTAL, \
        showvalue=0, state=Tkinter.DISABLED, \
        background=window.linuxMintHEX, foreground='black', \
        relief='flat', borderwidth=0)
    visualization.timeSlider.set(visualization.currentT)
    visualization.timeSlider.grid(padx=0, pady=5, column=2, row=window.gridy-1, \
        columnspan=window.gridx-3, sticky = (Tkinter.W, Tkinter.E))
    visualization.timeLabelText = Tkinter.StringVar()
    visualization.timeLabelText.set(str(visualization.currentT))
    # toolbar for +/- increments
    toolbarPM = ttk.Frame(window.mainframe, style='My.TFrame', \
        height=5, width=45)
    toolbarPM.grid(row=window.gridy-1, column=window.gridx-1, \
        sticky=(Tkinter.W, Tkinter.E))
    toolbarPMlabel = ttk.Label(toolbarPM, \
        textvariable=visualization.timeLabelText, width=6, style='My.TLabel')
    toolbarPMlabel.grid(row=0, column=0, padx=5)
    buttonMinus = ttk.Button(toolbarPM, text='-', \
        command=visualization.previousT, \
        style='My.TButton')
    buttonMinus.grid(row=0, column=1)
    buttonPlus = ttk.Button(toolbarPM, text='+', \
        command=visualization.nextT, \
        style='My.TButton')
    buttonPlus.grid(row=0, column=2)
    # progress bar
    visualization.progress = ttk.Progressbar(window.mainframe, \
        orient=Tkinter.HORIZONTAL, mode='determinate')
    visualization.progress.grid(column=0, row=window.gridy-1, \
        sticky = (Tkinter.W, Tkinter.E))
    visualization.progress.grid_remove()
    # renderWindowInteractor
    visualization.interactor = \
        visualization.renderWidget.GetRenderWindow().GetInteractor()
    visualization.interactorStyle = vtk.vtkInteractorStyleTrackballCamera()
    visualization.interactor.SetInteractorStyle(visualization.interactorStyle)
    visualization.interactor.AddObserver("KeyPressEvent", visualization.keypress)
    
    
    # create a popup menu to choose colorbar map
    menu = Tkinter.Menu(window.root, tearoff=0)
    visualization.scalarBarCacheF = Tkinter.IntVar()
    visualization.scalarBarCacheF.set(visualization.ctfNumberF)
    visualization.scalarBarCacheS = Tkinter.IntVar()
    visualization.scalarBarCacheS.set(visualization.ctfNumberS)
    visualization.scalarBarCacheI = Tkinter.IntVar()
    visualization.scalarBarCacheI.set(visualization.ctfNumberI)
    menu.add_radiobutton(label="Rainbow", \
        command=lambda:visualization.nextCTF("fluid"), \
        variable=visualization.scalarBarCacheF, value=0)
    menu.add_radiobutton(label="Blue-red", \
        command=lambda:visualization.nextCTF("fluid"), \
        variable=visualization.scalarBarCacheF, value=1)
    menu.add_radiobutton(label="Blue-white-red", \
        command=lambda:visualization.nextCTF("fluid"), \
        variable=visualization.scalarBarCacheF, value=2)
    menu.add_radiobutton(label="Black-white", \
        command=lambda:visualization.nextCTF("fluid"), \
        variable=visualization.scalarBarCacheF, value=3)
    menu.add_separator()
    menu.add_radiobutton(label="Rainbow", \
        command=lambda:visualization.nextCTF("solid"), \
        variable=visualization.scalarBarCacheS, value=0)
    menu.add_radiobutton(label="Blue-red", \
        command=lambda:visualization.nextCTF("solid"), \
        variable=visualization.scalarBarCacheS, value=1)
    menu.add_radiobutton(label="Blue-white-red", \
        command=lambda:visualization.nextCTF("solid"), \
        variable=visualization.scalarBarCacheS, value=2)
    menu.add_radiobutton(label="Black-white", \
        command=lambda:visualization.nextCTF("solid"), \
        variable=visualization.scalarBarCacheS, value=3)
    menu.add_separator()
    menu.add_radiobutton(label="Rainbow", \
        command=lambda:visualization.nextCTF("interface"), \
        variable=visualization.scalarBarCacheI, value=0)
    menu.add_radiobutton(label="Blue-red", \
        command=lambda:visualization.nextCTF("interface"), \
        variable=visualization.scalarBarCacheI, value=1)
    menu.add_radiobutton(label="Blue-white-red", \
        command=lambda:visualization.nextCTF("interface"), \
        variable=visualization.scalarBarCacheI, value=2)
    menu.add_radiobutton(label="Black-white", \
        command=lambda:visualization.nextCTF("interface"), \
        variable=visualization.scalarBarCacheI, value=3)
    def popup(event):
        menu.post(event.x_root, event.y_root)
    window.root.bind("<Button-3>", popup)
    
    # render scene
    visualization.renderWidget.Render()
    
    # start main loop
    window.root.mainloop()

if __name__=="__main__":
    main()
