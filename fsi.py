import Tkinter
import ttk
import tkFileDialog
import tkColorChooser
import readCheartData
import organiseData
import vtk
import numpy
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
import sys
import logging
import time
import os.path

sys.dont_write_bytecode = True

# provides a class that contains variables for FSI visualizations
class fsi(object):
    
    def __init__(self):
        super(fsi,self).__init__()
        # default values
        self.username           = "user"
        self.visualizeFluid     = True
        self.visualizeSolid     = True
        self.visualizeInterface = False
        self.boolUpdateVel    = True
        self.boolUpdateWel    = True
        self.boolUpdatePresF  = True
        self.boolUpdateSpaceF = True
        self.boolUpdateVort   = True
        self.boolUpdatePhiF   = True
        self.boolUpdateDisp   = True
        self.boolUpdateSolVel = True
        self.boolUpdatePresS  = True
        self.boolUpdateSpaceS = True
        self.boolUpdateQualityF = True
        self.boolUpdateQualityS = True
        self.boolUpdateSpaceI = True
        self.boolUpdateLMult  = True
        self.DEBUG            = True
        self.installDirectory = ""
        self.baseDirectory    = ""
        self.dataFolder       = "data/"
        self.meshFolder       = "meshes/"
        self.submitFolder     = "submit/"
        self.installDirectoryStr = []
        self.baseDirectoryStr    = []
        self.dataFolderStr       = []
        self.meshFolderStr       = []
        self.filenameSpaceF   = "FluidSpace-"
        self.filenameVel      = "Vel-"
        self.filenameWel      = "Wel-"
        self.filenameVort      = "Vort-"
        self.filenamePresF    = "FluidPres-"
        self.filenameQualityF = "FluidMeshQuality-"
        self.filenamePhiF     = "phi-"
        self.boolEffectiveG   = []
        self.filenameSpaceS   = "SolidSpace-"
        self.filenameDisp     = "Disp-"
        self.filenameSolVel   = "SolVel-"
        self.filenamePresS    = "SolidPres-"
        self.filenameQualityS = "SolidMeshQuality-"
        self.filenameSpaceI   = "BndrySpace-"
        self.filenameLM       = "LMult-"
        self.filenameTopoLinF = "domainF_lin_FE.T"
        self.filenameTopoQuadF = "domainF_quad_FE.T"
        self.filenameTopoLinS = "domainS_lin_FE.T"
        self.filenameTopoQuadS = "domainS_quad_FE.T"
        self.filenameTopoQuadI = "lm_quad_FE.T"
        self.currentT         = 1
        self.currentIndexT    = 0
        self.fromT            = 1
        self.toT              = 1
        self.animateFromT     = 1
        self.animateToT       = 1
        self.increment        = 1
        self.fromTStr         = []
        self.toTStr           = []
        self.incrementStr     = []
        self.animateFromStr   = []
        self.animateToStr     = []
        self.animateIncrementStr = []
        self.screenshotFolderStr = []
        self.filenameSuffix   = ".D"
        self.PO               = 0.0
        self.popup            = []
        self.camera           = []
        self.renderer         = []
        self.renderWindow     = []
        self.renderWidget     = []
        self.numberOfDimensions = 3
        self.ugridF           = []
        self.ugridS           = []
        self.ugridI           = []
        self.sgridF           = []
        self.sgridS           = []
        self.ugridCellsF      = []
        self.ugridCellsS      = []
        self.cellTypesF       = []
        self.cellTypesVort    = []
        self.cellTypesS       = []
        self.cellTypesI       = []
        self.tempElemF        = []
        self.tempElemS        = []
        self.tempElemI        = []
        self.tempMappingF     = []
        self.tempMappingS     = []
        self.tempMappingI     = []
        self.densityF         = 1.0
        self.gravity_x        = 0.0
        self.gravity_y        = 0.0
        self.gravity_z        = 0.0
        self.boolShowVel      = False
        self.boolShowWel      = False
        self.boolShowPresF    = True
        self.boolShowVort     = False
        self.boolShowPhiF     = False
        self.boolShowQualityF = False
        self.boolShowDisp     = False
        self.boolShowSolVel   = False
        self.boolShowPresS    = True
        self.boolShowQualityS = False
        self.boolShowLMult    = True
        self.colorCompF       = -1
        self.colorCompS       = -1
        self.colorCompI       = -1
        self.colorCompFstr    = []
        self.colorCompSstr    = []
        self.colorCompIstr    = []
        self.boolShowScalarBar = []
        self.boolMagnification = False
        self.magnification    = 4
        self.boolClipF        = False
        self.boolClipMeshF    = False
        self.boolPlaneF       = False
        self.boolEdgesF       = []
        self.boolEdgesS       = []
        self.boolEdgesI       = []
        self.boolAutoRangeF   = []
        self.boolAutoRangeS   = []
        self.boolAutoRangeI   = []
        self.userMinScalarBarF = 0.0
        self.userMaxScalarBarF = 1.0
        self.userMinScalarBarS = 0.0
        self.userMaxScalarBarS = 1.0
        self.userMinScalarBarI = 0.0
        self.userMaxScalarBarI = 1.0
        self.minPressureF     = 0.0
        self.maxPressureF     = 1.0
        self.minMagVel        = 0.0
        self.maxMagVel        = 1.0
        self.minVel0          = 0.0
        self.maxVel0          = 1.0
        self.minVel1          = 0.0
        self.maxVel1          = 1.0
        self.minVel2          = 0.0
        self.maxVel2          = 1.0
        self.minMagWel        = 0.0
        self.maxMagWel        = 1.0
        self.minWel0          = 0.0
        self.maxWel0          = 1.0
        self.minWel1          = 0.0
        self.maxWel1          = 1.0
        self.minWel2          = 0.0
        self.maxWel2          = 1.0
        self.minMagVort       = 0.0
        self.maxMagVort       = 1.0
        self.minVort0         = 0.0
        self.maxVort0         = 1.0
        self.minVort1         = 0.0
        self.maxVort1         = 1.0
        self.minVort2         = 0.0
        self.maxVort2         = 1.0
        self.minPhiF          = 0.0
        self.maxPhiF          = 1.0
        self.userMinF         = []
        self.userMaxF         = []
        self.minPressureS     = 0.0
        self.maxPressureS     = 1.0
        self.minMagDisp       = 0.0
        self.maxMagDisp       = 1.0
        self.minDisp0         = 0.0
        self.maxDisp0         = 1.0
        self.minDisp1         = 0.0
        self.maxDisp1         = 1.0
        self.minDisp2         = 0.0
        self.maxDisp2         = 1.0
        self.minMagSolVel     = 0.0
        self.maxMagSolVel     = 1.0
        self.minSolVel0       = 0.0
        self.maxSolVel0       = 1.0
        self.minSolVel1       = 0.0
        self.maxSolVel1       = 1.0
        self.minSolVel2       = 0.0
        self.maxSolVel2       = 1.0
        self.userMinS         = 0.0
        self.userMaxS         = 1.0
        self.minMagLMult      = 0.0
        self.maxMagLMult      = 1.0
        self.minLMult0        = 0.0
        self.maxLMult0        = 1.0
        self.minLMult1        = 0.0
        self.maxLMult1        = 1.0
        self.minLMult2        = 0.0
        self.maxLMult2        = 1.0
        self.userMinI         = 0.0
        self.userMaxI         = 1.0
        self.movePlaneByX     = 1.0
        self.movePlaneByY     = 1.0
        self.movePlaneByZ     = 1.0
        self.minXF            = 0.0
        self.maxXF            = 1.0
        self.minYF            = 0.0
        self.maxYF            = 1.0
        self.minZF            = 0.0
        self.maxZF            = 1.0
        self.minXS            = 0.0
        self.maxXS            = 1.0
        self.minYS            = 0.0
        self.maxYS            = 1.0
        self.minZS            = 0.0
        self.maxZS            = 1.0
        self.minXI            = 0.0
        self.maxXI            = 1.0
        self.minYI            = 0.0
        self.maxYI            = 1.0
        self.minZI            = 0.0
        self.maxZI            = 1.0
        self.hexx             = "#000000"
        self.cameraUp0        = 0.0
        self.cameraUp1        = 1.0
        self.cameraUp2        = 0.0
        self.cameraUp0Str     = []
        self.cameraUp1Str     = []
        self.cameraUp2Str     = []
        self.cameraPos0       = -10.0#-2
        self.cameraPos1       = 0.0#2
        self.cameraPos2       = 0.0#2
        self.cameraPos0Str    = []
        self.cameraPos1Str    = []
        self.cameraPos2Str    = []
        self.ctfNumberF       = 0
        self.ctfNumberS       = 0
        self.ctfNumberI       = 0
        self.numberOfCTFs     = 4
        self.labelVar         = 'no label'
        self.firstLabel       = True
        self.currentClipX     = 0.0
        self.currentClipY     = 0.0
        self.currentClipZ     = 0.0
        self.screenshotCounter = 0
        self.sphereSource     = []
        self.sphereMapper     = []
        self.sphereActor      = []
        self.showF            = []
        self.showS            = []
        self.showI            = []
        self.clipFnormal      = []
        self.backgroundColor  = []
        self.window2imageFilter = []
        self.pngWriter        = []
        self.backgroundDropDown        = []
        self.customBG0        = 0.0
        self.customBG1        = 0.0
        self.customBG2        = 0.0
        self.rgb              = []
        self.bgColorNumber    = 0
        self.cameraWindow     = []
        self.timeLabelText    = []
        self.interactor       = []
        self.progress         = []
        self.interactorStyle  = []
        self.scalarBarCacheF  = []
        self.scalarBarCacheS  = []
        self.scalarBarCacheI  = []
        self.currentCTFF      = []
        self.currentCTFS      = []
        self.currentCTFI      = []
        self.dataSetMapperF   = []
        self.dataSetMapperS   = []
        self.dataSetMapperI   = []
        self.dataSetActorF    = []
        self.dataSetActorS    = []
        self.dataSetActorI    = []
        self.scalarBarF       = []
        self.scalarBarS       = []
        self.scalarBarI       = []
        self.coordScalarBarF  = []
        self.coordScalarBarS  = []
        self.coordScalarBarI  = []
        self.timeSlider       = []
        self.boolShowOutlineF = []
        self.boolShowOutlineS = []
        self.boolShowOutlineI = []
        self.outlineF         = []
        self.outlineMapperF   = []
        self.outlineActorF    = []
        self.outlineS         = []
        self.outlineMapperS   = []
        self.outlineActorS    = []
        self.outlineI         = []
        self.outlineMapperI   = []
        self.outlineActorI    = []
        self.extractF         = []
        self.extractS         = []
        self.extractI         = []
        self.linearSubdivisionF = []
        self.linearSubdivisionS = []
        self.linearSubdivisionI = []
        self.dsmFnumberOfSubdivisions = 2
        self.dsmSnumberOfSubdivisions = 2
        self.dsmInumberOfSubdivisions = 2
        self.boolFirstExec    = True
        self.gradientFilterF  = []
        self.meshQualityF     = []
        self.meshQualityS     = []
        self.meshQualityI     = []
        self.minQualityF      = 0.0
        self.maxQualityF      = 1.0
        self.minQualityS      = 0.0
        self.maxQualityS      = 1.0
        self.minQualityI      = 0.0
        self.maxQualityI      = 1.0
        self.clippingPlaneF   = []
        self.linearSubdivisionClipF = []
        self.extractGridClipF = []
        self.clipF            = []
        self.extractClipF     = []
        self.clipMapperF      = []
        self.clipActorF       = []
        self.linearSubdivisionClipFpreserve = []
        self.extractGridClipFpreserve = []
        self.extractClipFpreserve     = []
        self.clipMapperFpreserve      = []
        self.clipActorFpreserve       = []
        self.boolVarDispSpace = []
        self.clipFnumberOfSubdivisions = 2
        self.currentPlaneOriginX = self.minXF+0.5*(self.maxXF-self.minXF)
        self.currentPlaneOriginY = self.minYF+0.5*(self.maxYF-self.minYF)
        self.currentPlaneOriginZ = self.minZF+0.5*(self.maxZF-self.minZF)
        self.slicePlaneF      = []
        self.planeCutF        = []
        self.cutMapperF       = []
        self.cutActorF        = []
        self.parallelProjection = []
        self.fluidPoints      = []
        self.planeSourceF     = []
        self.probeFilterF     = []
        self.probeMapperF     = []
        self.probeActorF      = []
        self.numberOfCellsF   = -1
        self.numberOfCellsS   = -1
        self.numberOfCellsI   = -1
        self.numberOfNodesF   = -1
        self.numberOfNodesS   = -1
        self.numberOfNodesI   = -1
        self.qualityMeasureF  = 0
        self.qualityMeasureS  = 0
        self.qualityMeasureI  = 0
        self.meshTypeF        = []
        self.meshTypeS        = []
        self.meshTypeI        = []
        self.samplePointsF    = []
        self.samplePolyDataF  = []
        self.enclosedSamplePointsF = []
        self.surfaceF         = []
        self.pointsInsideF    = []
        self.polyDataForDelaunayF  = []
        self.delnyF           = []
        self.probeFilterF     = []
        self.ugridProbeF      = []
        self.numSampleFX      = 101
        self.numSampleFY      = 101
        self.numSampleFZ      = 101
        self.sampleTol        = 1.0e-4
        self.sampleFdx        = 1
        self.sampleFdy        = 1
        self.sampleFdz        = 1
        
        
    
    # key bindings
    def keypress(self, arg2, event):
        key = arg2.GetKeySym()
        if key == 'q': # exit
            quit()
        elif key == 'plus': # move plane up
            self.movePlaneUp()
        elif key == 'minus': # move plane down
            self.movePlaneDown()
        elif key == 'numbersign': # reset plane position
            self.resetPlane()
    
    # reset plane
    def resetPlane(self):
        self.currentPlaneOriginX = self.minXF+0.5*(self.maxXF-self.minXF)
        self.currentPlaneOriginY = self.minYF+0.5*(self.maxYF-self.minYF)
        self.currentPlaneOriginZ = self.minZF+0.5*(self.maxZF-self.minZF)
        self.updateFluid()
    
    # move cut planes for slicing/clipping 3D volume
    def movePlaneUp(self):
        if not(self.clipFnormal.get() == "-1"):
            if ((self.clipFnormal.get() == "x") \
                or (self.clipFnormal.get() == "xe") \
                or (self.clipFnormal.get() == "a")) \
                and (self.maxXF >= self.currentPlaneOriginX + self.movePlaneByX):
                self.currentPlaneOriginX += self.movePlaneByX
            elif ((self.clipFnormal.get() == "y") \
                or (self.clipFnormal.get() == "ye") \
                or (self.clipFnormal.get() == "b")) \
                and (self.maxYF >= self.currentPlaneOriginY + self.movePlaneByY):
                self.currentPlaneOriginY += self.movePlaneByY
            elif ((self.clipFnormal.get() == "z") \
                or (self.clipFnormal.get() == "ze") \
                or (self.clipFnormal.get() == "c")) \
                and (self.maxZF >= self.currentPlaneOriginZ + self.movePlaneByZ):
                self.currentPlaneOriginZ += self.movePlaneByZ
            elif ((self.clipFnormal.get() == "i") \
                or (self.clipFnormal.get() == "j") \
                or (self.clipFnormal.get() == "k")) \
                and (self.maxZF >= self.currentPlaneOriginZ + self.movePlaneByZ):
                self.currentPlaneOriginZ += self.movePlaneByZ
        self.updateFluid()
    
    # move cut planes for slicing/clipping 3D volume
    def movePlaneDown(self):
        if not(self.clipFnormal.get() == "-1"):
            if ((self.clipFnormal.get() == "x") \
                or (self.clipFnormal.get() == "xe") \
                or (self.clipFnormal.get() == "a")) \
                and (self.minXF <= self.currentPlaneOriginX - self.movePlaneByX):
                self.currentPlaneOriginX -= self.movePlaneByX
            elif ((self.clipFnormal.get() == "y") \
                or (self.clipFnormal.get() == "ye") \
                or (self.clipFnormal.get() == "b")) \
                and (self.minYF <= self.currentPlaneOriginY - self.movePlaneByY):
                self.currentPlaneOriginY -= self.movePlaneByY
            elif ((self.clipFnormal.get() == "z") \
                or (self.clipFnormal.get() == "ze") \
                or (self.clipFnormal.get() == "c")) \
                and (self.minZF <= self.currentPlaneOriginZ - self.movePlaneByZ):
                self.currentPlaneOriginZ -= self.movePlaneByZ
            elif ((self.clipFnormal.get() == "i") \
                or (self.clipFnormal.get() == "j") \
                or (self.clipFnormal.get() == "k")) \
                and (self.maxZF <= self.currentPlaneOriginZ - self.movePlaneByZ):
                self.currentPlaneOriginZ -= self.movePlaneByZ
        self.updateFluid()
    
    # slice a 3D volume
    def sliceFxyz(self):
        if self.slicePlaneF == []:
            self.slicePlaneF = vtk.vtkPlane()
        self.slicePlaneF.SetOrigin(self.currentPlaneOriginX, \
            self.currentPlaneOriginY, \
            self.currentPlaneOriginZ)
        if self.clipFnormal.get() == "a":
            self.slicePlaneF.SetNormal(1.0, 0.0, 0.0)
        elif self.clipFnormal.get() == "b":
            self.slicePlaneF.SetNormal(0.0, 1.0, 0.0)
        elif self.clipFnormal.get() == "c":
            self.slicePlaneF.SetNormal(0.0, 0.0, 1.0)
        if self.planeCutF == []:
            self.planeCutF = vtk.vtkCutter()
        self.planeCutF.SetInput(self.ugridF)
        self.planeCutF.SetCutFunction(self.slicePlaneF)
        self.planeCutF.Update()
        if self.cutMapperF == []:
            self.cutMapperF = vtk.vtkPolyDataMapper()
        self.cutMapperF.SetInputConnection(self.planeCutF.GetOutputPort())
        self.cutMapperF.SetLookupTable(self.currentCTFF)
        self.scalarBarOnOffF()
        if self.boolShowPresF:
            self.cutMapperF.SetScalarModeToUsePointData()
            self.cutMapperF.SetUseLookupTableScalarRange(True)
        elif self.boolShowVel:
            self.cutMapperF.SetScalarModeToUsePointFieldData()
            self.cutMapperF.SelectColorArray("velocity")
        elif self.boolShowWel:
            self.cutMapperF.SetScalarModeToUsePointFieldData()
            self.cutMapperF.SelectColorArray("welocity")
        elif self.boolShowVort:
            self.cutMapperF.SetScalarModeToUsePointFieldData()
            self.cutMapperF.SelectColorArray("vorticity")
        elif self.boolShowQualityF:
            self.cutMapperF.SetScalarModeToUseCellFieldData()
            self.cutMapperF.SelectColorArray("Quality")
            self.cutMapperF.SetUseLookupTableScalarRange(True)
        elif self.boolShowPhiF:
            self.cutMapperF.SetScalarModeToUsePointFieldData()
            self.cutMapperF.SelectColorArray("phi")
            self.cutMapperF.SetUseLookupTableScalarRange(True)
        self.cutActorF = vtk.vtkActor()
        self.cutActorF.SetMapper(self.cutMapperF)
    
    # slice a 3D volume but sample data with regular set of points
    def structuredGridSliceF(self):
        # create sample points 
        if self.samplePointsF == []:
            self.samplePointsF = vtk.vtkPoints()
        if self.clipFnormal.get() == "i":
            numCells0 = self.numSampleFY - 1
            numCells1 = self.numSampleFZ - 1
            samplePointsFnumpy = \
                numpy.zeros((self.numSampleFY*self.numSampleFZ, 3))
            globalIDs = numpy.zeros((self.numSampleFY*self.numSampleFZ))
            for i in range(self.numSampleFY):
                for j in range(self.numSampleFZ):
                    samplePointsFnumpy[i+j*self.numSampleFY, :] = [ \
                        self.currentPlaneOriginX, \
                        self.sampleTol+self.minYF+i*self.sampleFdy, \
                        self.sampleTol+self.minZF+j*self.sampleFdz]
                    globalIDs[i+j*self.numSampleFY] = i+j*self.numSampleFY
        elif self.clipFnormal.get() == "j":
            numCells0 = self.numSampleFX - 1
            numCells1 = self.numSampleFZ - 1
            samplePointsFnumpy = \
                numpy.zeros((self.numSampleFX*self.numSampleFZ, 3))
            globalIDs = numpy.zeros((self.numSampleFX*self.numSampleFZ))
            for i in range(self.numSampleFX):
                for j in range(self.numSampleFZ):
                    samplePointsFnumpy[i+j*self.numSampleFX, :] = [ \
                        self.sampleTol+self.minXF+i*self.sampleFdx, \
                        self.currentPlaneOriginY, \
                        self.sampleTol+self.minZF+j*self.sampleFdz]
                    globalIDs[i+j*self.numSampleFX] = i+j*self.numSampleFX
        elif self.clipFnormal.get() == "k":
            numCells0 = self.numSampleFX - 1
            numCells1 = self.numSampleFY - 1
            samplePointsFnumpy = \
                numpy.zeros((self.numSampleFX*self.numSampleFY, 3))
            globalIDs = numpy.zeros((self.numSampleFX*self.numSampleFY))
            for i in range(self.numSampleFX):
                for j in range(self.numSampleFY):
                    samplePointsFnumpy[i+j*self.numSampleFX, :] = [ \
                        self.sampleTol+self.minXF+i*self.sampleFdx, \
                        self.sampleTol+self.minYF+j*self.sampleFdy, \
                        self.currentPlaneOriginZ]
                    globalIDs[i+j*self.numSampleFX] = i+j*self.numSampleFX
        # create quadrilateral cells to display sampled data as surface
        cells = numpy.zeros((numCells0*numCells1, 4))
        for i in range(numCells0):
            for j in range(numCells1):
                cells[i+j*numCells0, :] = [ \
                    i+j*(numCells0+1), \
                    i+j*(numCells0+1)+1, \
                    i+j*(numCells0+1)+numCells0+2, \
                    i+j*(numCells0+1)+numCells0+1]
        # now, assign points and sample data (but use global ids)
        self.samplePointsF.SetData(numpy_to_vtk(samplePointsFnumpy, \
            deep=1, array_type=vtk.VTK_DOUBLE))
        if self.samplePolyDataF == []:
            self.samplePolyDataF = vtk.vtkPolyData()
        self.samplePolyDataF.SetPoints(self.samplePointsF)
        self.samplePolyDataF.GetPointData().SetGlobalIds( \
            numpy_to_vtk(globalIDs, deep=1, array_type=vtk.VTK_INT))
        # reduce sample points --> we only want points inside the volume
        # extract surface of volume
        if self.surfaceF == []:
            self.surfaceF = vtk.vtkDataSetSurfaceFilter()
        self.surfaceF.SetInput(self.ugridF)
        # get enclosed sample points
        if self.enclosedSamplePointsF == []:
            self.enclosedSamplePointsF = vtk.vtkSelectEnclosedPoints()
        self.enclosedSamplePointsF.SetInput(self.samplePolyDataF)
        self.enclosedSamplePointsF.SetSurface(self.surfaceF.GetOutput())
        self.enclosedSamplePointsF.SetTolerance(0.00001)
        self.enclosedSamplePointsF.Update()
        # threshold points inside/outside
        if self.pointsInsideF == []:
            self.pointsInsideF = vtk.vtkThresholdPoints()
        self.pointsInsideF.SetInput(self.enclosedSamplePointsF.GetOutput())
        self.pointsInsideF.SetInputArrayToProcess(0, 0, 0, \
            vtk.vtkDataObject.FIELD_ASSOCIATION_POINTS, "SelectedPoints")
        self.pointsInsideF.ThresholdByUpper(1.0)
        self.pointsInsideF.Update()
#        if self.polyDataForDelaunayF == []:
#            self.polyDataForDelaunayF = vtk.vtkPolyData()
#        self.polyDataForDelaunayF.SetPoints(self.pointsInsideF.GetOutput().GetPoints())
        
        numKeptNodes = self.pointsInsideF.GetOutput().GetNumberOfPoints()
        keptNodes = numpy.zeros((numKeptNodes, 3))
        for i in range(numKeptNodes):
            keptNodes[i, :] = self.pointsInsideF.GetOutput().GetPoints().GetPoint(i)
        print self.pointsInsideF.GetOutput()
        #if i in keptNodes[0, :]:
            # do whatever
        
        
        
#        if self.delnyF == []:
#            self.delnyF = vtk.vtkDelaunay2D()
#        self.delnyF.SetInput(self.polyDataForDelaunayF)
#        self.delnyF.SetTolerance(0.00001)
#        self.delnyF.Update()
#        if not(self.pointsInsideF.GetOutput().GetNumberOfPoints() \
#            == self.delnyF.GetOutput().GetNumberOfPoints()):
#            print -1, -1
#            return -1
        
        # probe data set to get scalar data
        if self.probeFilterF == []:
            self.probeFilterF = vtk.vtkProbeFilter()
            self.probeFilterF.SetSource(self.ugridF)
            self.probeFilterF.SetInput(self.pointsInsideF.GetOutput())
        self.probeFilterF.Update()
        
        # create unstructured grid from probed data set
#        logging.debug("number of cells created by Delaunay triangulation: %i" \
#            % (self.delnyF.GetOutput().GetNumberOfCells()))
        if self.ugridProbeF == []:
            self.ugridProbeF = vtk.vtkUnstructuredGrid()
        self.ugridProbeF.SetPoints(self.pointsInsideF.GetOutput().GetPoints())
#        for i in range(self.delnyF.GetOutput().GetNumberOfCells()):
#            self.ugridProbeF.InsertNextCell( \
#                self.delnyF.GetOutput().GetCellType(i), \
#                self.delnyF.GetOutput().GetCell(i).GetPointIds())
        self.ugridProbeF.GetPointData().SetScalars( \
            self.probeFilterF.GetOutput().GetPointData().GetScalars())
        self.ugridProbeF.GetPointData().SetVectors( \
            self.probeFilterF.GetOutput().GetPointData().GetArray("velocity"))
        #ugridProbeF.GetPointData().AddArray( \
        #    self.probeFilterF.GetOutput().GetPointData().GetArray("vorticity"))
        
        
        if self.probeMapperF == []:
            self.probeMapperF = vtk.vtkDataSetMapper()
#        self.probeMapperF.SetInput(self.ugridProbeF)
        self.probeMapperF.SetInput(self.probeFilterF.GetOutput())
        self.scalarBarOnOffF()
        self.probeMapperF.SetLookupTable(self.currentCTFF)
        if self.boolShowPresF:
            self.probeMapperF.SetScalarModeToUsePointData()
            self.probeMapperF.SetUseLookupTableScalarRange(True)
        elif self.boolShowVel:
            self.probeMapperF.SetScalarModeToUsePointFieldData()
            self.probeMapperF.SelectColorArray("velocity")
        elif self.boolShowWel:
            self.probeMapperF.SetScalarModeToUsePointFieldData()
            self.probeMapperF.SelectColorArray("welocity")
        elif self.boolShowVort:
            self.probeMapperF.SetScalarModeToUsePointFieldData()
            self.probeMapperF.SelectColorArray("vorticity")
        elif self.boolShowQualityF:
            self.probeMapperF.SetScalarModeToUseCellFieldData()
            self.probeMapperF.SelectColorArray("Quality")
            self.probeMapperF.SetUseLookupTableScalarRange(True)
        elif self.boolShowPhiF:
            self.probeMapperF.SetScalarModeToUsePointFieldData()
            self.probeMapperF.SelectColorArray("phi")
            self.probeMapperF.SetUseLookupTableScalarRange(True)
        if self.probeActorF == []:
            self.probeActorF = vtk.vtkActor()
            self.probeActorF.SetMapper(self.probeMapperF)
    
    # clip a 3D volume slicing through elements
    def clipFxyz(self):
        if self.extractGridClipF == []:
            self.extractGridClipF = vtk.vtkBoxClipDataSet()
            self.extractGridClipF.SetInput(self.ugridF)
            
        #    clippingPlaneF = vtk.vtkPlane()
        #    clippingPlaneF.SetOrigin(self.currentPlaneOriginX, 0, 0)
        #    clippingPlaneF.SetNormal(1.0, 0.0, 0.0)
        #    clipF = vtk.vtkClipDataSet()
        #    clipF.SetInput(self.ugridF)
        #    clipF.SetClipFunction(clippingPlaneF)
        #    clipF.InsideOutOn()
        #    #clipF.SetMergeTolerance(1.0e-9)
        #    clipF.SetOutputPointPrecision(vtk.VTK_DOUBLE)
        
        if self.clipFnormal.get() == "x":
            self.extractGridClipF.SetBoxClip( \
#                self.minXF, self.currentPlaneOriginX, \
                self.currentPlaneOriginX, self.maxXF, \
                self.minYF, self.maxYF, \
                self.minZF, self.maxZF)
        elif self.clipFnormal.get() == "y":
            self.extractGridClipF.SetBoxClip( self.minXF, self.maxXF, \
                self.minYF, self.currentPlaneOriginY, \
                self.minZF, self.maxZF)
        elif self.clipFnormal.get() == "z":
            self.extractGridClipF.SetBoxClip( self.minXF, self.maxXF, \
                self.minYF, self.maxYF, \
                self.minZF, self.currentPlaneOriginZ)
        if self.extractClipF == []:
            self.extractClipF = vtk.vtkGeometryFilter()
            self.extractClipF.SetInput(self.extractGridClipF.GetOutput())
            self.extractClipF.Update()
        if self.linearSubdivisionClipF == []:
            self.linearSubdivisionClipF = vtk.vtkLinearSubdivisionFilter()
            self.linearSubdivisionClipF.SetInput(self.extractClipF.GetOutput())
            self.linearSubdivisionClipF.SetNumberOfSubdivisions( \
                self.clipFnumberOfSubdivisions)
        if self.clipMapperF == []:
            self.clipMapperF = vtk.vtkDataSetMapper()
            self.clipMapperF.SetInput(self.linearSubdivisionClipF.GetOutput())
        self.scalarBarOnOffF()
        self.clipMapperF.SetLookupTable(self.currentCTFF)
        if self.boolShowPresF:
            self.clipMapperF.SetScalarModeToUsePointData()
            self.clipMapperF.SetUseLookupTableScalarRange(True)
        elif self.boolShowVel:
            self.clipMapperF.SetScalarModeToUsePointFieldData()
            self.clipMapperF.SelectColorArray("velocity")
        elif self.boolShowWel:
            self.clipMapperF.SetScalarModeToUsePointFieldData()
            self.clipMapperF.SelectColorArray("welocity")
        elif self.boolShowVort:
            self.clipMapperF.SetScalarModeToUsePointFieldData()
            self.clipMapperF.SelectColorArray("vorticity")
        elif self.boolShowQualityF:
            self.clipMapperF.SetScalarModeToUseCellFieldData()
            self.clipMapperF.SelectColorArray("Quality")
            self.clipMapperF.SetUseLookupTableScalarRange(True)
        elif self.boolShowPhiF:
            self.clipMapperF.SetScalarModeToUsePointFieldData()
            self.clipMapperF.SelectColorArray("phi")
            self.clipMapperF.SetUseLookupTableScalarRange(True)
        if self.clipActorF == []:
            self.clipActorF = vtk.vtkActor()
            self.clipActorF.SetMapper(self.clipMapperF)
    
    # clip a 3D volume such that elements are preserved
    def clipFxyzPreserveElements(self):
        if self.clippingPlaneF == []:
            self.clippingPlaneF = vtk.vtkPlane()
        self.clippingPlaneF.SetOrigin(self.currentPlaneOriginX, \
            self.currentPlaneOriginY, \
            self.currentPlaneOriginZ)
        if self.clipFnormal.get() == "xe":
            self.clippingPlaneF.SetNormal(1.0, 0.0, 0.0)
        elif self.clipFnormal.get() == "ye":
            self.clippingPlaneF.SetNormal(0.0, 1.0, 0.0)
        elif self.clipFnormal.get() == "ze":
            self.clippingPlaneF.SetNormal(0.0, 0.0, 1.0)
        if self.extractGridClipFpreserve == []:
            self.extractGridClipFpreserve = vtk.vtkExtractGeometry()
            self.extractGridClipFpreserve.SetInput(self.ugridF)
            self.extractGridClipFpreserve.SetImplicitFunction(self.clippingPlaneF)
            self.extractGridClipFpreserve.ExtractInsideOff()
        if self.extractClipFpreserve == []:
            self.extractClipFpreserve = vtk.vtkGeometryFilter()
            self.extractClipFpreserve.SetInput(self.extractGridClipFpreserve.GetOutput())
        if self.linearSubdivisionClipFpreserve == []:
            self.linearSubdivisionClipFpreserve = vtk.vtkLinearSubdivisionFilter()
            self.linearSubdivisionClipFpreserve.SetInput(self.extractClipFpreserve.GetOutput())
            self.linearSubdivisionClipFpreserve.SetNumberOfSubdivisions( \
                self.dsmFnumberOfSubdivisions)
        if self.clipMapperFpreserve == []:
            self.clipMapperFpreserve = vtk.vtkDataSetMapper()
            self.clipMapperFpreserve.SetInput(self.linearSubdivisionClipFpreserve.GetOutput())
        self.scalarBarOnOffF()
        self.clipMapperFpreserve.SetLookupTable(self.currentCTFF)
        if self.boolShowPresF:
            self.clipMapperFpreserve.SetScalarModeToUsePointData()
            self.clipMapperFpreserve.SetUseLookupTableScalarRange(True)
        elif self.boolShowVel:
            self.clipMapperFpreserve.SetScalarModeToUsePointFieldData()
            self.clipMapperFpreserve.SelectColorArray("velocity")
        elif self.boolShowWel:
            self.clipMapperFpreserve.SetScalarModeToUsePointFieldData()
            self.clipMapperFpreserve.SelectColorArray("welocity")
        elif self.boolShowVort:
            self.clipMapperFpreserve.SetScalarModeToUsePointFieldData()
            self.clipMapperFpreserve.SelectColorArray("vorticity")
        elif self.boolShowQualityF:
            self.clipMapperFpreserve.SetScalarModeToUseCellFieldData()
            self.clipMapperFpreserve.SelectColorArray("Quality")
            self.clipMapperFpreserve.SetUseLookupTableScalarRange(True)
        elif self.boolShowPhiF:
            self.clipMapperFpreserve.SetScalarModeToUsePointFieldData()
            self.clipMapperFpreserve.SelectColorArray("phi")
            self.clipMapperFpreserve.SetUseLookupTableScalarRange(True)
        if self.clipActorFpreserve == []:
            self.clipActorFpreserve = vtk.vtkActor()
            self.clipActorFpreserve.SetMapper(self.clipMapperFpreserve)
    
    # compute mesh quality per cell
    # http://www.vtk.org/Wiki/images/6/6b/VerdictManual-revA.pdf
    def updateQualityF(self):
        logging.debug("update fluid mesh quality")
        if self.meshQualityF == [] and (self.numberOfDimensions == 2):
            self.meshQualityF = vtk.vtkMeshQuality()
            logging.debug("set input for fluid mesh quality")
            logging.debug("number of cells (lin): %i" \
                % self.ugridCellsF.GetNumberOfCells())
            self.meshQualityF.SetInput(self.ugridCellsF)
            logging.debug("set fluid mesh quality measure")
            self.meshQualityF.SetTriangleQualityMeasureToRadiusRatio()
        if self.boolUpdateQualityF:
            logging.debug("compute tet quality (fluid)")
            if self.numberOfDimensions == 3:
                filename = self.baseDirectory \
                    +self.dataFolder \
                    +self.filenameQualityF \
                    +str(self.currentT) \
                    +self.filenameSuffix
                if not(os.path.exists(filename)):
                    tempQualityF = readCheartData.computeTetQuality( \
                        vtk_to_numpy(self.ugridF.GetPoints().GetData()), \
                        self.tempElemF, \
                        self.qualityMeasureF)
                    readCheartData.writeScalars(tempQualityF, filename)
                else:
                    tempQualityF = readCheartData.readScalars(filename)
                logging.debug("compute tet quality (fluid) complete")
                self.boolUpdateQualityF = False
                self.ugridF.GetCellData().AddArray( \
                    organiseData.numpy2vtkDataArray1(tempQualityF, "Quality"))
            elif self.numberOfDimensions == 2:
                self.meshQualityF.Update()
                self.boolUpdateQualityF = False
                logging.debug("assign fluid mesh quality")
                self.ugridF.GetCellData().AddArray( \
                    self.meshQualityF.GetOutput().GetCellData().GetArray("Quality"))
            logging.debug("get range of fluid mesh quality values")
            self.minQualityF, self.maxQualityF = \
                self.ugridF.GetCellData().GetArray("Quality").GetRange()
            self.numberOfCellsF = \
                self.ugridF.GetCellData().GetArray("Quality").GetNumberOfTuples()
            logging.debug("number of cells: %i" % self.numberOfCellsF)
            logging.debug("cell quality range: [%.2f, %.2f]" \
                % (self.minQualityF, self.maxQualityF))
        logging.debug("update fluid mesh quality complete")
    
    def updateQualityS(self):
        if self.meshQualityS == [] and (self.numberOfDimensions == 2):
            self.meshQualityS = vtk.vtkMeshQuality()
            logging.debug("set input for solid mesh quality")
            logging.debug("number of cells (lin): %i" \
                % self.ugridCellsS.GetNumberOfCells())
            self.meshQualityS.SetInput(self.ugridCellsS)
            logging.debug("set solid mesh quality measure")
            self.meshQualityS.SetTriangleQualityMeasureToRadiusRatio()
        if self.boolUpdateQualityS:
            logging.debug("compute tet quality (solid)")
            if self.numberOfDimensions == 3:
                filename = self.baseDirectory \
                    +self.dataFolder \
                    +self.filenameQualityS \
                    +str(self.currentT) \
                    +self.filenameSuffix
                if not(os.path.exists(filename)):
                    if not(self.ugridS == []):
                        tempQualityS = readCheartData.computeTetQuality( \
                            vtk_to_numpy(self.ugridS.GetPoints().GetData()), \
                            self.tempElemS, \
                            self.qualityMeasureS)
                    else:
                        self.qualityMeasureS = 123456789
                        tempQualityS = readCheartData.computeTetQuality( \
                            vtk_to_numpy(self.sgridS.GetPoints().GetData()), \
                            self.tempElemS, \
                            self.qualityMeasureS)
                    readCheartData.writeScalars(tempQualityS, filename)
                else:
                    tempQualityS = readCheartData.readScalars(filename)
                logging.debug("compute tet quality (solid) complete")
                self.boolUpdateQualityS = False
                if not(self.ugridS == []):
                    self.ugridS.GetCellData().AddArray( \
                        organiseData.numpy2vtkDataArray1(tempQualityS, "Quality"))
                else:
                    self.sgridS.GetCellData().AddArray( \
                        organiseData.numpy2vtkDataArray1(tempQualityS, "Quality"))
                logging.debug("assign solid mesh quality")
            elif self.numberOfDimensions == 2:
                self.meshQualityS.Update()
                self.boolUpdateQualityS = False
                logging.debug("assign solid mesh quality")
                self.ugridS.GetCellData().AddArray( \
                    self.meshQualityS.GetOutput().GetCellData().GetArray("Quality"))
            logging.debug("get range of solid mesh quality values")
            if not(self.ugridS == []):
                self.minQualityS, self.maxQualityS = \
                    self.ugridS.GetCellData().GetArray("Quality").GetRange()
                self.numberOfCellsS = \
                    self.ugridS.GetCellData().GetArray("Quality").GetNumberOfTuples()
            else:
                self.minQualityS, self.maxQualityS = \
                    self.sgridS.GetCellData().GetArray("Quality").GetRange()
                self.numberOfCellsS = \
                    self.sgridS.GetCellData().GetArray("Quality").GetNumberOfTuples()
            logging.debug("number of cells: %i" % self.numberOfCellsS)
            logging.debug("cell quality range: [%.2f, %.2f]" \
                % (self.minQualityS, self.maxQualityS))
        logging.debug("update solid mesh quality complete")
    
    # t - dt
    def previousT(self):
        if self.currentT-self.increment >= self.fromT:
            self.currentT -= self.increment
            self.timeSlider.set(self.currentT)
            self.currentIndexT -= 1
        self.timeSliderUpdate()
    
    # t + dt
    def nextT(self):
        if self.currentT+self.increment <= self.toT:
            self.currentT += self.increment
            self.timeSlider.set(self.currentT)
            self.currentIndexT += 1
        self.timeSliderUpdate()
    
    # we need this function, otherwise the data sets are not updated if the
    # slider is moved
    def updateScaleValue(self, newvalue):
        if not(self.currentT == int(newvalue)):
            self.currentT = int(newvalue)
            self.timeSliderUpdate()
    
    # current time has changed --> update time slider and data sets
    def timeSliderUpdate(self):
        self.progress.grid()
        self.progress["value"] = 10
        self.timeLabelText.set(str(self.currentT))
        logging.debug("current time step: %i" % self.currentT)
        # new timestep --> all data sets need updates
        if self.visualizeFluid.get():
            self.boolUpdateVel    = True
            self.boolUpdateWel    = True
            self.boolUpdatePresF  = True
            self.boolUpdateSpaceF = True
            self.boolUpdateVort   = True
            self.boolUpdateQualityF = True
            self.boolUpdatePhiF   = True
        if self.visualizeSolid.get():
            self.boolUpdateDisp   = True
            self.boolUpdateSolVel = True
            self.boolUpdatePresS  = True
            self.boolUpdateSpaceS = True
            self.boolUpdateQualityS = True
        if self.visualizeInterface.get():
            self.boolUpdateSpaceI = True
            self.boolUpdateLMult  = True
        # update data sets
        if self.visualizeFluid.get():
            if not(self.showF.get() == "none"): self.updateSpaceF()
            self.progress["value"] = 10
            self.progress.update()
            if self.showF.get() == "vel": self.updateVel()
            self.progress["value"] = 30
            self.progress.update()
            if self.showF.get() == "wel": self.updateWel()
            self.progress["value"] = 40
            self.progress.update()
            if self.showF.get() == "presF": self.updatePresF()
            self.progress["value"] = 50
            self.progress.update()
            if self.showF.get() == "vort": self.updateVort()
            if self.showF.get() == "quality": self.updateQualityF()
            if self.showF.get() == "phi": self.updatePhiF()
            self.scalarBarOnOffF()
        self.progress["value"] = 70
        self.progress.update()
        if self.visualizeSolid.get():
            if not(self.showS.get() == "none"): self.updateSpaceS()
            self.progress["value"] = 80
            self.progress.update()
            if self.showS.get() == "disp": self.updateDisp()
            self.progress["value"] = 90
            self.progress.update()
            if self.showS.get() == "vel": self.updateSolVel()
            if self.showS.get() == "presS": self.updatePresS()
            if self.showS.get() == "quality": self.updateQualityS()
            self.scalarBarOnOffS()
        if self.visualizeInterface.get():
            if not(self.showI.get() == "none"): self.updateSpaceI()
            if self.showI.get() == "lm": self.updateLMult()
            self.scalarBarOnOffI()
        self.progress["value"] = 100
        self.progress.update()
        self.progress.grid_remove()
        self.renderWindow.Render()
    
    # animate time sequence
    def animate(self):
        self.animateFromT = int(self.animateFromStr.get())
        self.animateToT = int(self.animateToStr.get())
        if self.animateFromT < self.fromT:
            self.animateFromStr.set(str(self.fromT))
            self.animateFromT = self.fromT
        if self.animateToT > self.toT:
            self.animateToStr.set(str(self.toT))
            self.animateToT = self.toT
        self.currentT = self.animateFromT
        self.timeSliderUpdate()
        while self.currentT+self.increment <= self.animateToT:
            self.nextT()
    
    # animate and save time sequence
    def animateNsave(self):
        self.animateFromT = int(self.animateFromStr.get())
        self.animateToT = int(self.animateToStr.get())
        if self.animateFromT < self.fromT:
            self.animateFromStr.set(str(self.fromT))
            self.animateFromT = self.fromT
        if self.animateToT > self.toT:
            self.animateToStr.set(str(self.toT))
            self.animateToT = self.toT
        self.currentT = self.animateFromT
        self.timeSliderUpdate()
        self.screenshot()
        while self.currentT+self.increment <= self.animateToT:
            self.nextT()
            self.screenshot()
    
    # show/hide element edges
    def edgesOnOffF(self):
        self.boolEdgesF = self.dataSetActorF.GetProperty().GetEdgeVisibility()==0
        self.dataSetActorF.GetProperty().SetEdgeVisibility(self.boolEdgesF)
        self.renderWindow.Render()
    
    # show/hide element edges
    def edgesOnOffS(self):
        self.boolEdgesS = self.dataSetActorS.GetProperty().GetEdgeVisibility()==0
        self.dataSetActorS.GetProperty().SetEdgeVisibility(self.boolEdgesS)
        self.renderWindow.Render()
    
    # show/hide element edges
    def edgesOnOffI(self):
        self.boolEdgesI = self.dataSetActorI.GetProperty().GetEdgeVisibility()==0
        self.dataSetActorI.GetProperty().SetEdgeVisibility(self.boolEdgesI)
        self.renderWindow.Render()
    
    # update fluid data set mapper
    def updateFluid(self):
        if self.showF.get() == "none":
            if not(self.dataSetActorF == []):
                self.renderer.RemoveActor(self.dataSetActorF)
            if not(self.clipActorFpreserve == []):
                self.renderer.RemoveActor(self.clipActorFpreserve)
            if not(self.clipActorF == []):
                self.renderer.RemoveActor(self.clipActorF)
            if not(self.cutActorF == []):
                self.renderer.RemoveActor(self.cutActorF)
            if not(self.probeActorF == []):
                self.renderer.RemoveActor(self.probeActorF)
            self.boolShowVel   = False
            self.boolShowWel   = False
            self.boolShowPresF = False
            self.boolShowVort  = False
            self.boolShowQualityF = False
            self.boolShowPhiF  = False
            self.boolShowScalarBarF.set(False)
        else:
            if self.showF.get() == "vel":
                self.boolShowVel   = True
                self.boolShowWel   = False
                self.boolShowPresF = False
                self.boolShowVort  = False
                self.boolShowQualityF = False
                self.boolShowPhiF  = False
                self.updateVel()
            elif self.showF.get() == "wel":
                self.boolShowVel   = False
                self.boolShowWel   = True
                self.boolShowPresF = False
                self.boolShowVort  = False
                self.boolShowQualityF = False
                self.boolShowPhiF  = False
                self.updateWel()
            elif self.showF.get() == "presF":
                self.boolShowVel   = False
                self.boolShowWel   = False
                self.boolShowPresF = True
                self.boolShowVort  = False
                self.boolShowQualityF = False
                self.boolShowPhiF  = False
                self.updatePresF()
            elif self.showF.get() == "vort":
                self.boolShowVel   = False
                self.boolShowWel   = False
                self.boolShowPresF = False
                self.boolShowVort  = True
                self.boolShowQualityF = False
                self.boolShowPhiF  = False
                self.updateVort()
            elif self.showF.get() == "quality":
                self.boolShowVel   = False
                self.boolShowWel   = False
                self.boolShowPresF = False
                self.boolShowVort  = False
                self.boolShowQualityF = True
                self.boolShowPhiF  = False
                self.updateQualityF()
            elif self.showF.get() == "phi":
                self.boolShowVel   = False
                self.boolShowWel   = False
                self.boolShowPresF = False
                self.boolShowVort  = False
                self.boolShowQualityF = False
                self.boolShowPhiF  = True
                self.updatePhiF()
            if self.clipFnormal.get() == "-1":
                self.selectColorArrayF()
                if not(self.clipActorFpreserve == []):
                    self.renderer.RemoveActor(self.clipActorFpreserve)
                if not(self.clipActorF == []):
                    self.renderer.RemoveActor(self.clipActorF)
                if not(self.cutActorF == []):
                    self.renderer.RemoveActor(self.cutActorF)
                if not(self.probeActorF == []):
                    self.renderer.RemoveActor(self.probeActorF)
                self.renderer.AddActor(self.dataSetActorF)
            elif (self.clipFnormal.get() == "xe") \
                 or (self.clipFnormal.get() == "ye") \
                 or (self.clipFnormal.get() == "ze"):
                self.clipFxyzPreserveElements()
                if not(self.dataSetActorF == []):
                    self.renderer.RemoveActor(self.dataSetActorF)
                if not(self.clipActorF == []):
                    self.renderer.RemoveActor(self.clipActorF)
                if not(self.cutActorF == []):
                    self.renderer.RemoveActor(self.cutActorF)
                if not(self.probeActorF == []):
                    self.renderer.RemoveActor(self.probeActorF)
                self.renderer.AddActor(self.clipActorFpreserve)
            elif (self.clipFnormal.get() == "x") \
                 or (self.clipFnormal.get() == "y") \
                 or (self.clipFnormal.get() == "z"):
                self.clipFxyz()
                if not(self.dataSetActorF == []):
                    self.renderer.RemoveActor(self.dataSetActorF)
                if not(self.clipActorFpreserve == []):
                    self.renderer.RemoveActor(self.clipActorFpreserve)
                if not(self.cutActorF == []):
                    self.renderer.RemoveActor(self.cutActorF)
                if not(self.probeActorF == []):
                    self.renderer.RemoveActor(self.probeActorF)
                self.renderer.AddActor(self.clipActorF)
            elif (self.clipFnormal.get() == "a") \
                 or (self.clipFnormal.get() == "b") \
                 or (self.clipFnormal.get() == "c"):
                self.sliceFxyz()
                if not(self.dataSetActorF == []):
                    self.renderer.RemoveActor(self.dataSetActorF)
                if not(self.clipActorFpreserve == []):
                    self.renderer.RemoveActor(self.clipActorFpreserve)
                if not(self.clipActorF == []):
                    self.renderer.RemoveActor(self.clipActorF)
                if not(self.probeActorF == []):
                    self.renderer.RemoveActor(self.probeActorF)
                self.renderer.AddActor(self.cutActorF)
            elif (self.clipFnormal.get() == "i") \
                 or (self.clipFnormal.get() == "j") \
                 or (self.clipFnormal.get() == "k"):
                self.structuredGridSliceF()
                if not(self.dataSetActorF == []):
                    self.renderer.RemoveActor(self.dataSetActorF)
                if not(self.clipActorFpreserve == []):
                    self.renderer.RemoveActor(self.clipActorFpreserve)
                if not(self.clipActorF == []):
                    self.renderer.RemoveActor(self.clipActorF)
                if not(self.cutActorF == []):
                    self.renderer.RemoveActor(self.cutActorF)
                self.renderer.AddActor(self.probeActorF)
        self.scalarBarOnOffF()
        self.renderWindow.Render()
    
    # update solid data set mapper
    def updateSolid(self):
        if self.showS.get() == "none":
            if not(self.dataSetActorS == []):
                self.renderer.RemoveActor(self.dataSetActorS)
            self.boolShowDisp  = False
            self.boolShowSolVel = False
            self.boolShowPresF = False
            self.boolShowQualityS = False
            self.boolShowScalarBarS.set(False)
        else:
            if self.showS.get() == "disp":
                self.boolShowDisp  = True
                self.boolShowSolVel = False
                self.boolShowPresS = False
                self.boolShowQualityS = False
                self.updateDisp()
            elif self.showS.get() == "vel":
                self.boolShowDisp   = False
                self.boolShowSolVel = True
                self.boolShowPresS  = False
                self.boolShowQualityS = False
                self.updateDisp()
            elif self.showS.get() == "presS":
                self.boolShowDisp  = False
                self.boolShowSolVel = False
                self.boolShowPresS = True
                self.boolShowQualityS = False
                self.updatePresS()
            elif self.showS.get() == "quality":
                self.boolShowDisp  = False
                self.boolShowSolVel = False
                self.boolShowPresS = False
                self.boolShowQualityS = True
                self.updateQualityS()
            self.selectColorArrayS()
            self.renderer.AddActor(self.dataSetActorS)
        self.scalarBarOnOffS()
        self.renderWindow.Render()
    
    # update solid data set mapper
    def updateInterface(self):
        if self.showI.get() == "none":
            if not(self.dataSetActorI == []):
                self.renderer.RemoveActor(self.dataSetActorI)
            self.boolShowLMult  = False
            self.boolShowScalarBarI.set(False)
        else:
            if self.showI.get() == "lm":
                self.boolShowLMult  = True
                self.updateLMult()
            self.selectColorArrayI()
            self.renderer.AddActor(self.dataSetActorI)
        self.scalarBarOnOffI()
        self.renderWindow.Render()
    
    # create data set mappers for fluid and solid
    def createDataSetMappers(self):
        if self.visualizeFluid.get(): self.createDataSetMapperF()
        if self.visualizeSolid.get(): self.createDataSetMapperS()
        if self.visualizeInterface.get(): self.createDataSetMapperI()
    
    # create data set mapper for fluid
    def createDataSetMapperF(self):
        if self.extractF == []:
            self.extractF = vtk.vtkGeometryFilter()
        self.extractF.SetInput(self.ugridF)
        if self.linearSubdivisionF == []:
            self.linearSubdivisionF = vtk.vtkLinearSubdivisionFilter()
        self.linearSubdivisionF.SetInput(self.extractF.GetOutput())
        self.linearSubdivisionF.SetNumberOfSubdivisions( \
            self.dsmFnumberOfSubdivisions)
        if self.dataSetMapperF == []:
            self.dataSetMapperF = vtk.vtkDataSetMapper()
        self.dataSetMapperF.SetInput(self.linearSubdivisionF.GetOutput())
        if self.currentCTFF == []:
            self.scalarBarOnOffF()
        self.dataSetMapperF.SetLookupTable(self.currentCTFF)
        if self.dataSetActorF == []:
            self.dataSetActorF = vtk.vtkActor()
        self.dataSetActorF.SetMapper(self.dataSetMapperF)
        self.dataSetActorF.GetProperty().SetEdgeVisibility(self.boolEdgesF.get())
        self.dataSetActorF.GetProperty().SetInterpolationToGouraud()
        self.selectColorArrayF()
        self.renderer.AddActor(self.dataSetActorF)
        self.renderWindow.Render()
    
    # create data set mapper for solid
    def createDataSetMapperS(self):
        if self.extractS == []:
            self.extractS = vtk.vtkGeometryFilter()
        if not(self.ugridS == []):
            self.extractS.SetInput(self.ugridS)
        else:
            self.extractS.SetInput(self.sgridS)
        if self.linearSubdivisionS == []:
            self.linearSubdivisionS = vtk.vtkLinearSubdivisionFilter()
        self.linearSubdivisionS.SetInput(self.extractS.GetOutput())
        self.linearSubdivisionS.SetNumberOfSubdivisions( \
            self.dsmSnumberOfSubdivisions)
        if self.dataSetMapperS == []:
            self.dataSetMapperS = vtk.vtkDataSetMapper()
        self.dataSetMapperS.SetInput(self.linearSubdivisionS.GetOutput())
        if self.currentCTFS == []:
            self.scalarBarOnOffS()
        self.dataSetMapperS.SetLookupTable(self.currentCTFS)
        if self.dataSetActorS == []:
            self.dataSetActorS = vtk.vtkActor()
        self.dataSetActorS.SetMapper(self.dataSetMapperS)
        self.dataSetActorS.GetProperty().SetEdgeVisibility(self.boolEdgesS.get())
        self.dataSetActorS.GetProperty().SetInterpolationToGouraud()
        self.selectColorArrayS()
        self.renderer.AddActor(self.dataSetActorS)
        self.renderWindow.Render()
    
    # create data set mapper for solid
    def createDataSetMapperI(self):
        if self.extractI == []:
            self.extractI = vtk.vtkGeometryFilter()
        self.extractI.SetInput(self.ugridI)
        if self.linearSubdivisionI == []:
            self.linearSubdivisionI = vtk.vtkLinearSubdivisionFilter()
        self.linearSubdivisionI.SetInput(self.extractI.GetOutput())
        self.linearSubdivisionI.SetNumberOfSubdivisions( \
            self.dsmInumberOfSubdivisions)
        if self.dataSetMapperI == []:
            self.dataSetMapperI = vtk.vtkDataSetMapper()
        self.dataSetMapperI.SetInput(self.linearSubdivisionI.GetOutput())
        if self.currentCTFI == []:
            self.scalarBarOnOffI()
        self.dataSetMapperI.SetLookupTable(self.currentCTFI)
        if self.dataSetActorI == []:
            self.dataSetActorI = vtk.vtkActor()
        self.dataSetActorI.SetMapper(self.dataSetMapperI)
        self.dataSetActorI.GetProperty().SetEdgeVisibility(self.boolEdgesI.get())
        self.dataSetActorI.GetProperty().SetInterpolationToGouraud()
        self.selectColorArrayI()
        self.renderer.AddActor(self.dataSetActorI)
        self.renderWindow.Render()
    
    # select variable for color map
    def selectColorArrayF(self):
        if self.boolShowVel:
            self.dataSetMapperF.SetScalarModeToUsePointFieldData()
            self.dataSetMapperF.SelectColorArray("velocity")
            if not(self.clipMapperFpreserve == []):
                self.clipMapperFpreserve.SetScalarModeToUsePointFieldData()
                self.clipMapperFpreserve.SelectColorArray("velocity")
        elif self.boolShowWel:
            self.dataSetMapperF.SetScalarModeToUsePointFieldData()
            self.dataSetMapperF.SelectColorArray("welocity")
            if not(self.clipMapperFpreserve == []):
                self.clipMapperFpreserve.SetScalarModeToUsePointFieldData()
                self.clipMapperFpreserve.SelectColorArray("welocity")
        elif self.boolShowPresF:
            self.dataSetMapperF.SetScalarModeToUsePointData()
            self.dataSetMapperF.SetUseLookupTableScalarRange(True)
            if not(self.clipMapperFpreserve == []):
                self.clipMapperFpreserve.SetScalarModeToUsePointData()
                self.clipMapperFpreserve.SetUseLookupTableScalarRange(True)
        elif self.boolShowVort:
            self.dataSetMapperF.SetScalarModeToUsePointFieldData()
            self.dataSetMapperF.SelectColorArray("vorticity")
            if not(self.clipMapperFpreserve == []):
                self.clipMapperFpreserve.SetScalarModeToUsePointFieldData()
                self.clipMapperFpreserve.SelectColorArray("vorticity")
        elif self.boolShowQualityF:
            self.dataSetMapperF.SetScalarModeToUseCellFieldData()
            self.dataSetMapperF.SelectColorArray("Quality")
            self.dataSetMapperF.SetUseLookupTableScalarRange(True)
            if not(self.clipMapperFpreserve == []):
                self.clipMapperFpreserve.SetScalarModeToUseCellFieldData()
                self.clipMapperFpreserve.SelectColorArray("Quality")
                self.clipMapperFpreserve.SetUseLookupTableScalarRange(True)
        elif self.boolShowPhiF:
            self.dataSetMapperF.SetScalarModeToUsePointFieldData()
            self.dataSetMapperF.SelectColorArray("phi")
            self.dataSetMapperF.SetUseLookupTableScalarRange(True)
            if not(self.clipMapperFpreserve == []):
                self.clipMapperFpreserve.SetScalarModeToUsePointFieldData()
                self.clipMapperFpreserve.SelectColorArray("phi")
                self.clipMapperFpreserve.SetUseLookupTableScalarRange(True)
        self.dataSetMapperF.SetLookupTable(self.currentCTFF)
        if not(self.clipMapperFpreserve == []):
            self.clipMapperFpreserve.SetLookupTable(self.currentCTFF)
    
    # select variable for color map
    def selectColorArrayS(self):
        if self.boolShowDisp:
            self.dataSetMapperS.SetScalarModeToUsePointFieldData()
            self.dataSetMapperS.SelectColorArray("displacement")
        elif self.boolShowSolVel:
            self.dataSetMapperS.SetScalarModeToUsePointFieldData()
            self.dataSetMapperS.SelectColorArray("velocity")
        elif self.boolShowPresS:
            self.dataSetMapperS.SetScalarModeToUsePointData()
            self.dataSetMapperS.SetUseLookupTableScalarRange(True)
        elif self.boolShowQualityS:
            self.dataSetMapperS.SetScalarModeToUseCellFieldData()
            self.dataSetMapperS.SelectColorArray("Quality")
            self.dataSetMapperS.SetUseLookupTableScalarRange(True)
        self.dataSetMapperS.SetLookupTable(self.currentCTFS)
    
    # select variable for color map
    def selectColorArrayI(self):
        if self.boolShowLMult:
            self.dataSetMapperI.SetScalarModeToUsePointFieldData()
            self.dataSetMapperI.SelectColorArray("LM")
        self.dataSetMapperI.SetLookupTable(self.currentCTFI)
    
    # show outline of fluid domain
    def outlineOnOffF(self):
        if self.outlineF == []:
            self.outlineF = vtk.vtkOutlineFilter()
            self.outlineF.SetInput(self.ugridF)
            self.outlineMapperF = vtk.vtkPolyDataMapper()
            self.outlineMapperF.SetInput(self.outlineF.GetOutput())
            self.outlineActorF = vtk.vtkActor()
            self.outlineActorF.SetMapper(self.outlineMapperF)
        if self.boolShowOutlineF.get():
            self.renderer.AddActor(self.outlineActorF)
        else:
            self.renderer.RemoveActor(self.outlineActorF)
        self.renderWindow.Render()
    
    # show outline of solid domain
    def outlineOnOffS(self):
        if self.outlineS == []:
            self.outlineS = vtk.vtkOutlineFilter()
            if self.ugridS == []:
                self.outlineS.SetInput(self.sgridS)
            else:
                self.outlineS.SetInput(self.ugridS)
            self.outlineMapperS = vtk.vtkPolyDataMapper()
            self.outlineMapperS.SetInput(self.outlineS.GetOutput())
            self.outlineActorS = vtk.vtkActor()
            self.outlineActorS.SetMapper(self.outlineMapperS)
        if self.boolShowOutlineS.get():
            self.renderer.AddActor(self.outlineActorS)
        else:
            self.renderer.RemoveActor(self.outlineActorS)
        self.renderWindow.Render()
    
    # show outline of interface domain
    def outlineOnOffI(self):
        if self.outlineI == []:
            self.outlineI = vtk.vtkOutlineFilter()
            self.outlineI.SetInput(self.ugridI)
            self.outlineMapperI = vtk.vtkPolyDataMapper()
            self.outlineMapperI.SetInput(self.outlineI.GetOutput())
            self.outlineActorI = vtk.vtkActor()
            self.outlineActorI.SetMapper(self.outlineMapperI)
        if self.boolShowOutlineI.get():
            self.renderer.AddActor(self.outlineActorI)
        else:
            self.renderer.RemoveActor(self.outlineActorI)
        self.renderWindow.Render()
    
    # show/hide scalar bar for fluid data set
    def scalarBarOnOffF(self):
        if self.boolShowScalarBarF == []:
            self.boolShowScalarBarF = Tkinter.BooleanVar()
            self.boolShowScalarBarF.set(False)
        if self.scalarBarF == []:
            self.scalarBarF = vtk.vtkScalarBarActor()
            self.scalarBarF.SetOrientationToHorizontal()
            self.scalarBarF.GetLabelTextProperty().SetColor(0, 0, 0)
            self.scalarBarF.GetTitleTextProperty().SetColor(0, 0, 0)
            self.scalarBarF.GetLabelTextProperty().BoldOff()
            self.scalarBarF.GetTitleTextProperty().BoldOff()
            self.scalarBarF.GetLabelTextProperty().ItalicOff()
            self.scalarBarF.GetTitleTextProperty().ItalicOff()
            self.coordScalarBarF = self.scalarBarF.GetPositionCoordinate()
            self.coordScalarBarF.SetCoordinateSystemToNormalizedViewport()
            self.coordScalarBarF.SetValue(0.1, 0.025)
            self.scalarBarF.SetWidth(0.8)
            self.scalarBarF.SetHeight(0.1)
        self.nextCTF("fluid")
        if self.boolShowScalarBarF.get():
            if self.boolShowVel:
                self.scalarBarF.SetTitle("Fluid velocity")
            elif self.boolShowWel:
                self.scalarBarF.SetTitle("Fluid domain velocity")
            elif self.boolShowPresF:
                self.scalarBarF.SetTitle("Fluid pressure")
            elif self.boolShowVort:
                self.scalarBarF.SetTitle("Fluid vorticity")
            elif self.boolShowQualityF:
                self.scalarBarF.SetTitle("Fluid mesh quality")
            elif self.boolShowPhiF:
                self.scalarBarF.SetTitle("Fluid directional scalar")
            self.renderer.AddActor(self.scalarBarF)
        else:
            self.renderer.RemoveActor(self.scalarBarF)
        self.renderWindow.Render()
    
    # show/hide scalar bar for solid data set
    def scalarBarOnOffS(self):
        if self.boolShowScalarBarS == []:
            self.boolShowScalarBarS = Tkinter.BooleanVar()
            self.boolShowScalarBarS.set(False)
        if self.scalarBarS == []:
            self.scalarBarS = vtk.vtkScalarBarActor()
            self.scalarBarS.SetOrientationToHorizontal()
            self.scalarBarS.GetLabelTextProperty().SetColor(0, 0, 0)
            self.scalarBarS.GetTitleTextProperty().SetColor(0, 0, 0)
            self.scalarBarS.GetLabelTextProperty().BoldOff()
            self.scalarBarS.GetTitleTextProperty().BoldOff()
            self.scalarBarS.GetLabelTextProperty().ItalicOff()
            self.scalarBarS.GetTitleTextProperty().ItalicOff()
            self.coordScalarBarS = self.scalarBarS.GetPositionCoordinate()
            self.coordScalarBarS.SetCoordinateSystemToNormalizedViewport()
            self.coordScalarBarS.SetValue(0.1, 0.025)
            self.scalarBarS.SetWidth(0.8)
            self.scalarBarS.SetHeight(0.1)
        self.nextCTF("solid")
        if self.boolShowScalarBarS.get():
            if self.boolShowDisp:
                self.scalarBarS.SetTitle("Solid displacement")
            elif self.boolShowSolVel:
                self.scalarBarS.SetTitle("Solid velocity")
            elif self.boolShowPresS:
                self.scalarBarS.SetTitle("Solid pressure")
            elif self.boolShowQualityS:
                self.scalarBarS.SetTitle("Solid mesh quality")
            self.renderer.AddActor(self.scalarBarS)
        else:
            self.renderer.RemoveActor(self.scalarBarS)
        self.renderWindow.Render()
    
    # show/hide scalar bar for solid data set
    def scalarBarOnOffI(self):
        if self.boolShowScalarBarI == []:
            self.boolShowScalarBarI = Tkinter.BooleanVar()
            self.boolShowScalarBarI.set(False)
        if self.scalarBarI == []:
            self.scalarBarI = vtk.vtkScalarBarActor()
            self.scalarBarI.SetOrientationToHorizontal()
            self.scalarBarI.GetLabelTextProperty().SetColor(0, 0, 0)
            self.scalarBarI.GetTitleTextProperty().SetColor(0, 0, 0)
            self.scalarBarI.GetLabelTextProperty().BoldOff()
            self.scalarBarI.GetTitleTextProperty().BoldOff()
            self.scalarBarI.GetLabelTextProperty().ItalicOff()
            self.scalarBarI.GetTitleTextProperty().ItalicOff()
            self.coordScalarBarI = self.scalarBarI.GetPositionCoordinate()
            self.coordScalarBarI.SetCoordinateSystemToNormalizedViewport()
            self.coordScalarBarI.SetValue(0.1, 0.025)
            self.scalarBarI.SetWidth(0.8)
            self.scalarBarI.SetHeight(0.1)
        self.nextCTF("interface")
        if self.boolShowScalarBarI.get():
            if self.boolShowLMult:
                self.scalarBarI.SetTitle("Lagrange multiplier")
            self.renderer.AddActor(self.scalarBarI)
        else:
            self.renderer.RemoveActor(self.scalarBarI)
        self.renderWindow.Render()
    
    # update color transfer function
    def nextCTF(self, fluidORsolid):
        # define scalarbars
        def rainbowCTF(minValue, maxValue, component, fluidORsolid):
            # rainbow color map
            rainbow = vtk.vtkColorTransferFunction()
            rainbow.AddRGBPoint(minValue, 0.0, 0.0, 1.0)
            rainbow.AddRGBPoint(minValue+0.25*(maxValue-minValue), 0.0, 1.0, 1.0)
            rainbow.AddRGBPoint(minValue+0.50*(maxValue-minValue), 0.0, 1.0, 0.0)
            rainbow.AddRGBPoint(minValue+0.75*(maxValue-minValue), 1.0, 1.0, 0.0)
            rainbow.AddRGBPoint(maxValue, 1.0, 0.0, 0.0)
            if (fluidORsolid == "fluid" and self.boolShowPresF == False) \
                or (fluidORsolid == "solid" and self.boolShowPresS == False) \
                or (fluidORsolid == "interface"):
                if component == -1:
                    rainbow.SetVectorModeToMagnitude()
                    rainbow.SetVectorComponent(-1)
                else:
                    rainbow.SetVectorModeToComponent()
                    rainbow.SetVectorComponent(component)
            return rainbow

        def blueRedCTF(minValue, maxValue, component, fluidORsolid):
            # blue-red color map
            blueRed = vtk.vtkColorTransferFunction()
            blueRed.AddRGBPoint(minValue, 0.0, 0.0, 1.0)
            blueRed.AddRGBPoint(maxValue, 1.0, 0.0, 0.0)
            if (fluidORsolid == "fluid" and self.boolShowPresF == False) \
                or (fluidORsolid == "solid" and self.boolShowPresS == False) \
                or (fluidORsolid == "interface"):
                if component == -1:
                    blueRed.SetVectorModeToMagnitude()
                    blueRed.SetVectorComponent(-1)
                else:
                    blueRed.SetVectorModeToComponent()
                    blueRed.SetVectorComponent(component)
            return blueRed
        
        # http://www.sandia.gov/~kmorel/documents/ColorMaps/
        # Moreland2009.pdf
        def blueWhiteRedCTF(minValue, maxValue, component, fluidORsolid):
            # blue-red color map
            blueWhiteRed = vtk.vtkColorTransferFunction()
            blueWhiteRed.AddRGBPoint(minValue, 0.230, 0.299, 0.754)
            blueWhiteRed.AddRGBPoint(0.5*(minValue+maxValue), 0.865, 0.865, 0.865)
            blueWhiteRed.AddRGBPoint(maxValue, 0.706, 0.016, 0.150)
            blueWhiteRed.SetColorSpaceToDiverging()
            if (fluidORsolid == "fluid" and self.boolShowPresF == False) \
                or (fluidORsolid == "solid" and self.boolShowPresS == False) \
                or (fluidORsolid == "interface"):
                if component == -1:
                    blueWhiteRed.SetVectorModeToMagnitude()
                    blueWhiteRed.SetVectorComponent(-1)
                else:
                    blueWhiteRed.SetVectorModeToComponent()
                    blueWhiteRed.SetVectorComponent(component)
            return blueWhiteRed

        def blackWhiteCTF(minValue, maxValue, component, fluidORsolid):
            # black-white color map
            blackWhite = vtk.vtkColorTransferFunction()
            blackWhite.AddRGBPoint(minValue, 0.0, 0.0, 0.0)
            blackWhite.AddRGBPoint(maxValue, 1.0, 1.0, 1.0)
            if (fluidORsolid == "fluid" and self.boolShowPresF == False) \
                or (fluidORsolid == "solid" and self.boolShowPresS == False) \
                or (fluidORsolid == "interface"):
                if component == -1:
                    blackWhite.SetVectorModeToMagnitude()
                    blackWhite.SetVectorComponent(-1)
                else:
                    blackWhite.SetVectorModeToComponent()
                    blackWhite.SetVectorComponent(component)
            return blackWhite
        
        # get number of selected CTF
        self.ctfNumberF = self.scalarBarCacheF.get()
        self.ctfNumberS = self.scalarBarCacheS.get()
        self.ctfNumberI = self.scalarBarCacheI.get()
        # if current CTF number is non-existent, default to first CTF
        if self.ctfNumberF >= self.numberOfCTFs:
            self.ctfNumberF = 0
        if self.ctfNumberS >= self.numberOfCTFs:
            self.ctfNumberS = 0
        if self.ctfNumberI >= self.numberOfCTFs:
            self.ctfNumberI = 0
        if fluidORsolid == "fluid" and self.visualizeFluid.get():
            # decide which component we use the scalar bar for
            self.colorCompF = int(self.colorCompFstr.get())
            # auto-range values
            if self.boolAutoRangeF.get():
                if self.boolShowPresF:
                    self.colorCompF = -1
                    self.colorCompFstr.set(str(self.colorCompF))
                    self.userMinScalarBarF = self.minPressureF
                    self.userMaxScalarBarF = self.maxPressureF
                elif self.boolShowVel:
                    if self.colorCompF == -1:
                        self.userMinScalarBarF = self.minMagVel
                        self.userMaxScalarBarF = self.maxMagVel
                    elif self.colorCompF == 0:
                        self.userMinScalarBarF = self.minVel0
                        self.userMaxScalarBarF = self.maxVel0
                    elif self.colorCompF == 1:
                        self.userMinScalarBarF = self.minVel1
                        self.userMaxScalarBarF = self.maxVel1
                    elif self.colorCompF == 2:
                        self.userMinScalarBarF = self.minVel2
                        self.userMaxScalarBarF = self.maxVel2
                elif self.boolShowWel:
                    if self.colorCompF == -1:
                        self.userMinScalarBarF = self.minMagWel
                        self.userMaxScalarBarF = self.maxMagWel
                    elif self.colorCompF == 0:
                        self.userMinScalarBarF = self.minWel0
                        self.userMaxScalarBarF = self.maxWel0
                    elif self.colorCompF == 1:
                        self.userMinScalarBarF = self.minWel1
                        self.userMaxScalarBarF = self.maxWel1
                    elif self.colorCompF == 2:
                        self.userMinScalarBarF = self.minWel2
                        self.userMaxScalarBarF = self.maxWel2
                elif self.boolShowVort:
                    if self.colorCompF == -1:
                        self.userMinScalarBarF = self.minMagVort
                        self.userMaxScalarBarF = self.maxMagVort
                    elif self.colorCompF == 0:
                        self.userMinScalarBarF = self.minVort0
                        self.userMaxScalarBarF = self.maxVort0
                    elif self.colorCompF == 1:
                        self.userMinScalarBarF = self.minVort1
                        self.userMaxScalarBarF = self.maxVort1
                    elif self.colorCompF == 2:
                        self.userMinScalarBarF = self.minVort2
                        self.userMaxScalarBarF = self.maxVort2
                elif self.boolShowQualityF:
                    self.colorCompF = -1
                    self.colorCompFstr.set(str(self.colorCompF))
                    self.userMinScalarBarF = self.minQualityF
                    self.userMaxScalarBarF = self.maxQualityF
                elif self.boolShowPhiF:
                    self.colorCompF = -1
                    self.colorCompFstr.set(str(self.colorCompF))
                    self.userMinScalarBarF = self.minPhiF
                    self.userMaxScalarBarF = self.maxPhiF
                self.userMinF.set(str(self.userMinScalarBarF))
                self.userMaxF.set(str(self.userMaxScalarBarF))
            # use user defined range
            else:
                self.userMinScalarBarF = float(self.userMinF.get())
                self.userMaxScalarBarF = float(self.userMaxF.get())
            # select scalarbar and set ranges & vector component
            if self.ctfNumberF == 0:
                self.currentCTFF = rainbowCTF( \
                    self.userMinScalarBarF, self.userMaxScalarBarF, \
                    self.colorCompF, fluidORsolid)
            elif self.ctfNumberF == 1:
                self.currentCTFF = blueRedCTF( \
                    self.userMinScalarBarF, self.userMaxScalarBarF, \
                    self.colorCompF, fluidORsolid)
            elif self.ctfNumberF == 2:
                self.currentCTFF = blueWhiteRedCTF( \
                    self.userMinScalarBarF, self.userMaxScalarBarF, \
                    self.colorCompF, fluidORsolid)
            elif self.ctfNumberF == 3:
                self.currentCTFF = blackWhiteCTF( \
                    self.userMinScalarBarF, self.userMaxScalarBarF, \
                    self.colorCompF, fluidORsolid)
            # connect to data set mapper
            self.selectColorArrayF()
            self.scalarBarF.SetLookupTable(self.currentCTFF)
        elif fluidORsolid == "solid" and self.visualizeSolid.get():
            # decide which component we use the scalar bar for
            self.colorCompS = int(self.colorCompSstr.get())
            # auto-range values
            if self.boolAutoRangeS.get():
                if self.boolShowPresS:
                    self.colorCompS = -1
                    self.colorCompSstr.set(str(self.colorCompS))
                    self.userMinScalarBarS = self.minPressureS
                    self.userMaxScalarBarS = self.maxPressureS
                elif self.boolShowDisp:
                    if self.colorCompS == -1:
                        self.userMinScalarBarS = self.minMagDisp
                        self.userMaxScalarBarS = self.maxMagDisp
                    elif self.colorCompS == 0:
                        self.userMinScalarBarS = self.minDisp0
                        self.userMaxScalarBarS = self.maxDisp0
                    elif self.colorCompS == 1:
                        self.userMinScalarBarS = self.minDisp1
                        self.userMaxScalarBarS = self.maxDisp1
                    elif self.colorCompS == 2:
                        self.userMinScalarBarS = self.minDisp2
                        self.userMaxScalarBarS = self.maxDisp2
                elif self.boolShowSolVel:
                    if self.colorCompS == -1:
                        self.userMinScalarBarS = self.minMagSolVel
                        self.userMaxScalarBarS = self.maxMagSolVel
                    elif self.colorCompS == 0:
                        self.userMinScalarBarS = self.minSolVel0
                        self.userMaxScalarBarS = self.maxSolVel0
                    elif self.colorCompS == 1:
                        self.userMinScalarBarS = self.minSolVel1
                        self.userMaxScalarBarS = self.maxSolVel1
                    elif self.colorCompS == 2:
                        self.userMinScalarBarS = self.minSolVel2
                        self.userMaxScalarBarS = self.maxSolVel2
                elif self.boolShowQualityS:
                    self.colorCompS = -1
                    self.colorCompSstr.set(str(self.colorCompS))
                    self.userMinScalarBarS = self.minQualityS
                    self.userMaxScalarBarS = self.maxQualityS
                self.userMinS.set(str(self.userMinScalarBarS))
                self.userMaxS.set(str(self.userMaxScalarBarS))
            # use user defined range
            else:
                self.userMinScalarBarS = float(self.userMinS.get())
                self.userMaxScalarBarS = float(self.userMaxS.get())
            # select scalarbar and set ranges & vector component
            if self.ctfNumberS == 0:
                self.currentCTFS = rainbowCTF( \
                    self.userMinScalarBarS, self.userMaxScalarBarS, \
                    self.colorCompS, fluidORsolid)
            elif self.ctfNumberS == 1:
                self.currentCTFS = blueRedCTF( \
                    self.userMinScalarBarS, self.userMaxScalarBarS, \
                    self.colorCompS, fluidORsolid)
            elif self.ctfNumberS == 2:
                self.currentCTFS = blueWhiteRedCTF( \
                    self.userMinScalarBarS, self.userMaxScalarBarS, \
                    self.colorCompS, fluidORsolid)
            elif self.ctfNumberS == 3:
                self.currentCTFS = blackWhiteCTF( \
                    self.userMinScalarBarS, self.userMaxScalarBarS, \
                    self.colorCompS, fluidORsolid)
            # connect to data set mapper
            self.selectColorArrayS()
            self.scalarBarS.SetLookupTable(self.currentCTFS)
        elif fluidORsolid == "interface" and self.visualizeInterface.get():
            # decide which component we use the scalar bar for
            self.colorCompI = int(self.colorCompIstr.get())
            # auto-range values
            if self.boolAutoRangeI.get():
                if self.boolShowLMult:
                    if self.colorCompI == -1:
                        self.userMinScalarBarI = self.minMagLMult
                        self.userMaxScalarBarI = self.maxMagLMult
                    elif self.colorCompI == 0:
                        self.userMinScalarBarI = self.minLMult0
                        self.userMaxScalarBarI = self.maxLMult0
                    elif self.colorCompI == 1:
                        self.userMinScalarBarI = self.minLMult1
                        self.userMaxScalarBarI = self.maxLMult1
                    elif self.colorCompI == 2:
                        self.userMinScalarBarI = self.minLMult2
                        self.userMaxScalarBarI = self.maxLMult2
                self.userMinI.set(str(self.userMinScalarBarI))
                self.userMaxI.set(str(self.userMaxScalarBarI))
            # use user defined range
            else:
                self.userMinScalarBarI = float(self.userMinI.get())
                self.userMaxScalarBarI = float(self.userMaxI.get())
            # select scalarbar and set ranges & vector component
            if self.ctfNumberI == 0:
                self.currentCTFI = rainbowCTF( \
                    self.userMinScalarBarI, self.userMaxScalarBarI, \
                    self.colorCompI, fluidORsolid)
            elif self.ctfNumberI == 1:
                self.currentCTFI = blueRedCTF( \
                    self.userMinScalarBarI, self.userMaxScalarBarI, \
                    self.colorCompI, fluidORsolid)
            elif self.ctfNumberI == 2:
                self.currentCTFI = blueWhiteRedCTF( \
                    self.userMinScalarBarI, self.userMaxScalarBarI, \
                    self.colorCompI, fluidORsolid)
            elif self.ctfNumberI == 3:
                self.currentCTFI = blackWhiteCTF( \
                    self.userMinScalarBarI, self.userMaxScalarBarI, \
                    self.colorCompI, fluidORsolid)
            # connect to data set mapper
            self.selectColorArrayI()
            self.scalarBarI.SetLookupTable(self.currentCTFI)
        # update scene
        self.renderWindow.Render()
    
    # read configuration file to set user default values
    def readConfiguration(self, filename):
        with open (filename, "r") as myfile:
            config = myfile.read().splitlines()
        # use user configuration
        self.installDirectory   = config[0]
        self.baseDirectory      = config[1]
        self.dataFolder         = config[2]
        self.meshFolder         = config[3]
        self.filenameSpaceF     = config[4]
        self.filenameVel        = config[5]
        self.filenamePresF      = config[6]
        self.filenameVort       = config[7]
        self.boolEffectiveG     = Tkinter.BooleanVar()
        self.boolEffectiveG.set(config[8] == 'True')
        self.filenameSpaceS     = config[9]
        self.filenameDisp       = config[10]
        self.filenamePresS      = config[11]
        self.boolVarDispSpace   = Tkinter.BooleanVar()
        self.boolVarDispSpace.set(config[12] == 'True')
        self.filenameTopoLinF   = config[13] + "_lin_FE.T"
        self.filenameTopoQuadF  = config[13] + "_quad_FE.T"
        self.filenameTopoLinS   = config[14] + "_lin_FE.T"
        self.filenameTopoQuadS  = config[14] + "_quad_FE.T"
        self.DEBUG              = (config[15] == 'True')
        self.densityF           = float(config[16])
        self.gravity_x          = float(config[17])
        self.gravity_y          = float(config[18])
        self.gravity_z          = float(config[19])
        self.visualizeFluid     = Tkinter.BooleanVar()
        self.visualizeSolid     = Tkinter.BooleanVar()
        self.visualizeInterface = Tkinter.BooleanVar()
        self.visualizeFluid.set(config[20])
        self.visualizeSolid.set(config[21])
        self.visualizeInterface.set(config[22])
        self.PO                 = float(config[23])
        self.filenameWel        = config[24]
        self.filenamePhiF       = config[25]
        self.filenameSpaceI     = config[26]
        self.filenameLMult      = config[27]
        self.filenameSolVel     = config[28]
        # other hard-coded defaults
        self.boolAutoRangeF     = Tkinter.BooleanVar()
        self.boolAutoRangeF.set(True)
        self.boolAutoRangeS     = Tkinter.BooleanVar()
        self.boolAutoRangeS.set(True)
        self.boolAutoRangeI     = Tkinter.BooleanVar()
        self.boolAutoRangeI.set(True)
        self.userMinF = Tkinter.StringVar()
        self.userMinF.set(0.0)
        self.userMaxF = Tkinter.StringVar()
        self.userMaxF.set(1.0)
        self.userMinS = Tkinter.StringVar()
        self.userMinS.set(0.0)
        self.userMaxS = Tkinter.StringVar()
        self.userMaxS.set(1.0)
        self.userMinI = Tkinter.StringVar()
        self.userMinI.set(0.0)
        self.userMaxI = Tkinter.StringVar()
        self.userMaxI.set(1.0)
    
    # auto-range colormap or use user-defined range
    def enableUserRangeF(self, win):
        if self.boolAutoRangeF.get():
            win.entryMinF.state(["disabled"])
            win.entryMaxF.state(["disabled"])
            self.scalarBarOnOffF()
        else:
            win.entryMinF.state(["!disabled"])
            win.entryMaxF.state(["!disabled"])
    
    # auto-range colormap or use user-defined range
    def enableUserRangeS(self, win):
        if self.boolAutoRangeS.get():
            win.entryMinS.state(["disabled"])
            win.entryMaxS.state(["disabled"])
            self.scalarBarOnOffS()
        else:
            win.entryMinS.state(["!disabled"])
            win.entryMaxS.state(["!disabled"])
    
    # auto-range colormap or use user-defined range
    def enableUserRangeI(self, win):
        if self.boolAutoRangeI.get():
            win.entryMinI.state(["disabled"])
            win.entryMaxI.state(["disabled"])
            self.scalarBarOnOffI()
        else:
            win.entryMinI.state(["!disabled"])
            win.entryMaxI.state(["!disabled"])
    
    # update interface node coordinates
    def updateSpaceI(self):
        logging.debug("update interface space")
        if self.ugridI == []:
            self.ugridI      = vtk.vtkUnstructuredGrid()
            if self.numberOfDimensions == 3:
                if self.meshTypeI == 22:
                    # quadratic triangle mesh
                    self.cellTypesI = vtk.vtkQuadraticTriangle().GetCellType()
                    divby = 7
                    # read triangles
                    self.tempElemI = readCheartData.readInterfaceElementsQuad( \
                        self.baseDirectory \
                        +self.meshFolder \
                        +self.filenameTopoQuadI, \
                        self.numberOfDimensions)
                    # create cells for unstructured grid
                    tempElemLinI, cellstypesI, cellslocationsI = \
                        readCheartData.createTopologyInterface3Dquad(self.tempElemI, \
                        self.cellTypesI)
                    cellsI = vtk.vtkCellArray()
                    cellsI.SetCells(int(tempElemLinI.shape[0]/divby), \
                        numpy_to_vtk(tempElemLinI, deep=1, \
                        array_type=vtk.vtkIdTypeArray().GetDataType()))
                    # assign cells
                    self.ugridI.SetCells(numpy_to_vtk(cellstypesI, deep=1, \
                        array_type=vtk.vtkUnsignedCharArray().GetDataType()),
                                   numpy_to_vtk(cellslocationsI, deep = 1, \
                                   array_type=vtk.vtkIdTypeArray().GetDataType()),
                                   cellsI)
                elif self.meshTypeI == 5:
                    # linear triangle mesh
                    self.cellTypesI = vtk.vtkTriangle().GetCellType()
                    divby = 4
                    # read triangles
                    self.tempElemI = readCheartData.readInterfaceElementsLin( \
                        self.baseDirectory \
                        +self.meshFolder \
                        +self.filenameTopoQuadI, \
                        self.numberOfDimensions)
                    # create cells for unstructured grid
                    tempElemLinI, cellstypesI, cellslocationsI = \
                        readCheartData.createTopologyInterface3Dlin(self.tempElemI, \
                        self.cellTypesI)
                    cellsI = vtk.vtkCellArray()
                    cellsI.SetCells(int(tempElemLinI.shape[0]/divby), \
                        numpy_to_vtk(tempElemLinI, deep=1, \
                        array_type=vtk.vtkIdTypeArray().GetDataType()))
                    # assign cells
                    self.ugridI.SetCells(numpy_to_vtk(cellstypesI, deep=1, \
                        array_type=vtk.vtkUnsignedCharArray().GetDataType()),
                                   numpy_to_vtk(cellslocationsI, deep = 1, \
                                   array_type=vtk.vtkIdTypeArray().GetDataType()),
                                   cellsI)
            else:
                print "interface mesh for 2D case not implemented."
        if self.boolUpdateSpaceI:
            # read points
            pointsI = vtk.vtkPoints()
            tempCoord, self.numberOfDimensions = \
                readCheartData.readVectors(self.baseDirectory \
                                           +self.dataFolder \
                                           +self.filenameSpaceI \
                                           +str(self.currentT) \
                                           +self.filenameSuffix)
            pointsI.SetData(numpy_to_vtk(tempCoord, \
                deep=1, array_type=vtk.VTK_DOUBLE))
            # assign points
            self.ugridI.SetPoints(pointsI)
            self.minXI, self.maxXI, self.minYI, self.maxYI, self.minZI, self.maxZI = \
                self.ugridI.GetPoints().GetBounds()
            self.boolUpdateSpaceI = False
        logging.debug("update interface space completed")
    
    # update solid displacement
    def updateLMult(self):
        logging.debug("update Lagrange multiplier")
        if ((self.ugridS == []) or self.boolUpdateSpaceS):
            logging.debug("unstructured grid for interface will be updated first")
            self.updateSpaceI()
        if self.boolUpdateLMult:
            tempLMult, numberOfDimensions = \
                readCheartData.readVectors(self.baseDirectory \
                                           +self.dataFolder \
                                           +self.filenameLMult \
                                           +str(self.currentT) \
                                           +self.filenameSuffix)
            self.ugridI.GetPointData().SetVectors( \
                organiseData.numpy2vtkDataArray(tempLMult, "LM"))
            if self.numberOfDimensions != numberOfDimensions:
                logging.debug("ERROR: number of dimensions of interface space is " \
                              % self.numberOfDimensions)
                logging.debug("ERROR: number of Lagrange multiplier components is " \
                              % numberOfDimensions)
            self.minMagLMult, self.maxMagLMult = \
                self.ugridI.GetPointData().GetVectors().GetRange(-1)
            self.minLMult0, self.maxLMult0 = \
                self.ugridI.GetPointData().GetVectors().GetRange(0)
            self.minLMult1, self.maxLMult1 = \
                self.ugridI.GetPointData().GetVectors().GetRange(1)
            self.minLMult2, self.maxLMult2 = \
                self.ugridI.GetPointData().GetVectors().GetRange(2)
            logging.debug("Lagrange multiplier magnitude range: [%.2f, %.2f]" \
                          % (self.minMagLMult, self.maxMagLMult))
            logging.debug("Lagrange multiplier x-range: [%.2f, %.2f]" \
                          % (self.minLMult0, self.maxLMult0))
            logging.debug("Lagrange multiplier y-range: [%.2f, %.2f]" \
                          % (self.minLMult1, self.maxLMult1))
            logging.debug("Lagrange multiplier z-range: [%.2f, %.2f]" \
                          % (self.minLMult2, self.maxLMult2))
            self.boolUpdateLMult = False
        logging.debug("update Lagrange multiplier completed")
    
    # update fluid node coordinates
    def updateSpaceF(self):
        logging.debug("update fluid space")
        if self.boolUpdateSpaceF:
            # read points
            tempCoord, self.numberOfDimensions = \
                readCheartData.readVectors(self.baseDirectory \
                                           +self.dataFolder \
                                           +self.filenameSpaceF \
                                           +str(self.currentT) \
                                           +self.filenameSuffix)
        if self.ugridF == []:
            self.ugridF      = vtk.vtkUnstructuredGrid()
            self.ugridCellsF = vtk.vtkUnstructuredGrid()
            if self.numberOfDimensions == 3:
                if self.meshTypeF == 24:
                    # quadratic tetrahedral mesh
                    self.cellTypesF = vtk.vtkQuadraticTetra().GetCellType()
                    divby = 11
                    # read tetrahedrons
                    self.tempElemF = readCheartData.readTriQuadAsLin( \
                        self.baseDirectory \
                        +self.meshFolder \
                        +self.filenameTopoQuadF, \
                        self.numberOfDimensions)
                    # create cells for unstructured grid
                    tempElemLinF, cellstypesF, cellslocationsF = \
                        readCheartData.createTopology3Dquad(self.tempElemF, \
                        self.cellTypesF)
                elif self.meshTypeF == 10:
                    # linear tetrahedral mesh
                    self.cellTypesF = vtk.vtkTetra().GetCellType()
                    divby = 5
                    # read tetrahedrons
                    self.tempElemF = readCheartData.readTriTetLin( \
                        self.baseDirectory \
                        +self.meshFolder \
                        +self.filenameTopoQuadF, \
                        self.numberOfDimensions)
                    self.tempElemF = readCheartData.flipTets(self.tempElemF, \
                        tempCoord)
                    # create cells for unstructured grid
                    tempElemLinF, cellstypesF, cellslocationsF = \
                        readCheartData.createTopology3Dcells(self.tempElemF, \
                        self.cellTypesF)
                cellsF = vtk.vtkCellArray()
                cellsF.SetCells(int(tempElemLinF.shape[0]/divby), \
                    numpy_to_vtk(tempElemLinF, deep=1, \
                    array_type=vtk.vtkIdTypeArray().GetDataType()))
                # assign cells
                self.ugridF.SetCells(numpy_to_vtk(cellstypesF, deep=1, \
                    array_type=vtk.vtkUnsignedCharArray().GetDataType()),
                               numpy_to_vtk(cellslocationsF, deep = 1, \
                               array_type=vtk.vtkIdTypeArray().GetDataType()),
                               cellsF)
                
                ## create a linear tetra mesh too for cell quality
                ct = vtk.vtkTetra().GetCellType()
                divby = 5
                # create cells for unstructured grid
                tempElemLinF, cellstypesF, cellslocationsF = \
                    readCheartData.createTopology3Dcells(self.tempElemF, \
                    ct)
                cellsF = vtk.vtkCellArray()
                cellsF.SetCells(int(tempElemLinF.shape[0]/divby), \
                    numpy_to_vtk(tempElemLinF, deep=1, \
                    array_type=vtk.vtkIdTypeArray().GetDataType()))
                # assign cells
                self.ugridCellsF.SetCells(numpy_to_vtk(cellstypesF, deep=1, \
                    array_type=vtk.vtkUnsignedCharArray().GetDataType()),
                               numpy_to_vtk(cellslocationsF, deep = 1, \
                               array_type=vtk.vtkIdTypeArray().GetDataType()),
                               cellsF)
            else:
                # quadratic triangle mesh
                self.cellTypesF = vtk.vtkQuadraticTriangle().GetCellType()
                divby = 7
                # read triangles
                self.tempElemF = readCheartData.readTriQuadAsLin( \
                    self.baseDirectory \
                    +self.meshFolder \
                    +self.filenameTopoQuadF, \
                    self.numberOfDimensions)
                # create cells for unstructured grid
                tempElemLinF, cellstypesF, cellslocationsF = \
                    readCheartData.createTopology2Dquad(self.tempElemF, \
                    self.cellTypesF)
                cellsF = vtk.vtkCellArray()
                cellsF.SetCells(int(tempElemLinF.shape[0]/divby), \
                    numpy_to_vtk(tempElemLinF, deep=1, \
                    array_type=vtk.vtkIdTypeArray().GetDataType()))
                # assign cells
                self.ugridF.SetCells(numpy_to_vtk(cellstypesF, deep=1, \
                    array_type=vtk.vtkUnsignedCharArray().GetDataType()),
                               numpy_to_vtk(cellslocationsF, deep = 1, \
                               array_type=vtk.vtkIdTypeArray().GetDataType()),
                               cellsF)
                
                ## create a linear triangle mesh too for cell quality
                ct = vtk.vtkTriangle().GetCellType()
                divby = 4
                # create cells for unstructured grid
                tempElemLinF, cellstypesF, cellslocationsF = \
                    readCheartData.createTopology2D(self.tempElemF, \
                    ct)
                cellsF = vtk.vtkCellArray()
                cellsF.SetCells(int(tempElemLinF.shape[0]/divby), \
                    numpy_to_vtk(tempElemLinF, deep=1, \
                    array_type=vtk.vtkIdTypeArray().GetDataType()))
                # assign cells
                self.ugridCellsF.SetCells(numpy_to_vtk(cellstypesF, deep=1, \
                    array_type=vtk.vtkUnsignedCharArray().GetDataType()),
                               numpy_to_vtk(cellslocationsF, deep = 1, \
                               array_type=vtk.vtkIdTypeArray().GetDataType()),
                               cellsF)
        if self.boolUpdateSpaceF:
            # read points
            pointsF = vtk.vtkPoints()
            pointsF.SetData(numpy_to_vtk(tempCoord, \
                deep=1, array_type=vtk.VTK_DOUBLE))
            # assign points
            self.ugridF.SetPoints(pointsF)
            self.ugridCellsF.SetPoints(pointsF)
            self.minXF, self.maxXF, self.minYF, self.maxYF, self.minZF, self.maxZF = \
                self.ugridF.GetPoints().GetBounds()
            # now set increments for moving plane and sampling resolution
            self.movePlaneByX = (self.maxXF - self.minXF) * 0.01
            self.movePlaneByY = (self.maxYF - self.minYF) * 0.01
            self.movePlaneByZ = (self.maxZF - self.minZF) * 0.01
            self.sampleFdx    = (self.maxXF - self.minXF) \
                / (self.numSampleFX - 1) - 2.0 * self.sampleTol
            self.sampleFdy    = (self.maxYF - self.minYF) \
                / (self.numSampleFY - 1) - 2.0 * self.sampleTol
            self.sampleFdz    = (self.maxZF - self.minZF) \
                / (self.numSampleFZ - 1) - 2.0 * self.sampleTol
            self.boolUpdateSpaceF = False
        logging.debug("update fluid space completed")
    
    # update fluid velocity
    def updateVel(self):
        logging.debug("update fluid velocity")
        if self.ugridF == [] or self.boolUpdateSpaceF:
            logging.debug("unstructured grid for fluid will be updated first")
            self.updateSpaceF()
        if self.boolUpdateVel \
            and (os.path.exists(self.baseDirectory \
                 +self.dataFolder \
                 +self.filenameVel \
                 +str(self.currentT) \
                 +self.filenameSuffix)):
            tempVel, numberOfDimensions = \
                readCheartData.readVectors(self.baseDirectory \
                                           +self.dataFolder \
                                           +self.filenameVel \
                                           +str(self.currentT) \
                                           +self.filenameSuffix)
            self.ugridF.GetPointData().SetVectors( \
                organiseData.numpy2vtkDataArray(tempVel, "velocity"))
            if self.numberOfDimensions != numberOfDimensions:
                logging.debug("ERROR: number of dimensions of fluid space is " \
                              % self.numberOfDimensions)
                logging.debug("ERROR: number of fluid velocity components is " \
                              % numberOfDimensions)
            self.minMagVel, self.maxMagVel = \
                self.ugridF.GetPointData().GetVectors("velocity").GetRange(-1)
            self.minVel0, self.maxVel0 = \
                self.ugridF.GetPointData().GetVectors("velocity").GetRange(0)
            self.minVel1, self.maxVel1 = \
                self.ugridF.GetPointData().GetVectors("velocity").GetRange(1)
            self.minVel2, self.maxVel2 = \
                self.ugridF.GetPointData().GetVectors("velocity").GetRange(2)
            logging.debug("fluid velocity magnitude range: [%.2f, %.2f]" \
                          % (self.minMagVel, self.maxMagVel))
            logging.debug("fluid velocity x-range: [%.2f, %.2f]" \
                          % (self.minVel0, self.maxVel0))
            logging.debug("fluid velocity y-range: [%.2f, %.2f]" \
                          % (self.minVel1, self.maxVel1))
            logging.debug("fluid velocity z-range: [%.2f, %.2f]" \
                          % (self.minVel2, self.maxVel2))
            self.boolUpdateVel = False
        logging.debug("update fluid velocity completed")
    
    # update fluid domain velocity
    def updateWel(self):
        logging.debug("update fluid domain velocity")
        if self.ugridF == [] or self.boolUpdateSpaceF:
            logging.debug("unstructured grid for fluid will be updated first")
            self.updateSpaceF()
        if self.boolUpdateWel \
            and (os.path.exists(self.baseDirectory \
                 +self.dataFolder \
                 +self.filenameWel \
                 +str(self.currentT) \
                 +self.filenameSuffix)):
            tempWel, numberOfDimensions = \
                readCheartData.readVectors(self.baseDirectory \
                                           +self.dataFolder \
                                           +self.filenameWel \
                                           +str(self.currentT) \
                                           +self.filenameSuffix)
            self.ugridF.GetPointData().AddArray( \
                organiseData.numpy2vtkDataArray(tempWel, "welocity"))
            if self.numberOfDimensions != numberOfDimensions:
                logging.debug("ERROR: number of dimensions of fluid space is " \
                              % self.numberOfDimensions)
                logging.debug("ERROR: number of fluid domain velocity components is " \
                              % numberOfDimensions)
            self.minMagWel, self.maxMagWel = \
                self.ugridF.GetPointData().GetVectors("welocity").GetRange(-1)
            self.minWel0, self.maxWel0 = \
                self.ugridF.GetPointData().GetVectors("welocity").GetRange(0)
            self.minWel1, self.maxWel1 = \
                self.ugridF.GetPointData().GetVectors("welocity").GetRange(1)
            self.minWel2, self.maxWel2 = \
                self.ugridF.GetPointData().GetVectors("welocity").GetRange(2)
            logging.debug("fluid domain velocity magnitude range: [%.2f, %.2f]" \
                          % (self.minMagWel, self.maxMagWel))
            logging.debug("fluid domain velocity x-range: [%.2f, %.2f]" \
                          % (self.minWel0, self.maxWel0))
            logging.debug("fluid domain velocity y-range: [%.2f, %.2f]" \
                          % (self.minWel1, self.maxWel1))
            logging.debug("fluid domain velocity z-range: [%.2f, %.2f]" \
                          % (self.minWel2, self.maxWel2))
            self.boolUpdateWel = False
        logging.debug("update fluid domain velocity completed")
    
    # update fluid vorticity
    def updateVort(self):
        logging.debug("update fluid vorticity")
        if self.boolUpdateVort \
            and (os.path.exists(self.baseDirectory \
                 +self.dataFolder \
                 +self.filenameVel \
                 +str(self.currentT) \
                 +self.filenameSuffix)):
            if self.boolUpdateVel:
                self.updateVel()
            filename = self.baseDirectory \
                +self.dataFolder \
                +self.filenameVort \
                +str(self.currentT) \
                +self.filenameSuffix
            if not(os.path.exists(filename)):
                if self.gradientFilterF == []:
                    self.gradientFilterF = vtk.vtkGradientFilter()
                    self.gradientFilterF.SetInput(self.ugridF)
                    self.gradientFilterF.SetInputArrayToProcess(0, 0, 0, 0, "velocity")
                    self.gradientFilterF.SetResultArrayName("vorticity")
                    self.gradientFilterF.ComputeVorticityOn()
                self.gradientFilterF.Update()
                readCheartData.writeVectors( \
                    vtk_to_numpy( \
                    self.gradientFilterF.GetOutput().GetPointData().GetVectors("vorticity")), \
                    filename)
            #tempVort =  readCheartData.calculateVorticity3D(vtk_to_numpy(self.ugridF.GetPoints().GetData()), self.tempElemF, vtk_to_numpy(self.ugridF.GetPointData().GetVectors("velocity")))
            #for i in range(100):
            #    print tempVort[i, 0], tempVort[i, 1], tempVort[i, 2]
            tempVort, numberOfDimensionsVort = \
                readCheartData.readVectors(filename)
            self.ugridF.GetPointData().AddArray( \
                organiseData.numpy2vtkDataArray(tempVort, "vorticity"))
            self.minMagVort, self.maxMagVort = \
                self.ugridF.GetPointData().GetVectors("vorticity").GetRange(-1)
            self.minVort0, self.maxVort0 = \
                self.ugridF.GetPointData().GetVectors("vorticity").GetRange(0)
            self.minVort1, self.maxVort1 = \
                self.ugridF.GetPointData().GetVectors("vorticity").GetRange(1)
            self.minVort2, self.maxVort2 = \
                self.ugridF.GetPointData().GetVectors("vorticity").GetRange(2)
            logging.debug("fluid vorticity magnitude range: [%.2f, %.2f]" \
                          % (self.minMagVort, self.maxMagVort))
            logging.debug("fluid vorticity x-range: [%.2f, %.2f]" \
                          % (self.minVort0, self.maxVort0))
            logging.debug("fluid vorticity y-range: [%.2f, %.2f]" \
                          % (self.minVort1, self.maxVort1))
            logging.debug("fluid vorticity z-range: [%.2f, %.2f]" \
                          % (self.minVort2, self.maxVort2))
            self.boolUpdateVort = False
        logging.debug("update fluid vorticity complete")
    
    # update fluid pressure
    def updatePresF(self):
        logging.debug("update fluid pressure")
        if self.tempMappingF == [] and not(self.meshTypeF == 10):
            self.tempMappingF = readCheartData.findMappingLinQuad( \
                self.baseDirectory \
                +self.meshFolder \
                +self.filenameTopoLinF, \
                self.baseDirectory \
                +self.meshFolder \
                +self.filenameTopoQuadF, \
                self.numberOfDimensions)
        if self.boolUpdateSpaceF:
            logging.debug("unstructured grid for fluid will be updated first")
            self.updateSpaceF()
        if self.boolUpdatePresF \
            and (os.path.exists(self.baseDirectory \
                 +self.dataFolder \
                 +self.filenamePresF \
                 +str(self.currentT) \
                 +self.filenameSuffix)):
            tempPresLinF = readCheartData.readScalars( \
                self.baseDirectory \
                +self.dataFolder \
                +self.filenamePresF \
                +str(self.currentT) \
                +self.filenameSuffix)
            if not(self.meshTypeF == 10):
                tempPresQuadF = readCheartData.interpolateLinToQuad( \
                    self.tempElemF, \
                    vtk_to_numpy(self.ugridF.GetPoints().GetData()), \
                    tempPresLinF, \
                    self.tempMappingF, \
                    self.numberOfDimensions)
                if self.boolEffectiveG.get():
                    tempPresQuadF = readCheartData.changeOfVariables( \
                        vtk_to_numpy(self.ugridF.GetPoints().GetData()), \
                        tempPresQuadF, self.densityF, \
                        self.gravity_x, self.gravity_y, self.gravity_z, self.PO)
            else:
                if self.boolEffectiveG.get():
                    tempPresQuadF = readCheartData.changeOfVariables( \
                        vtk_to_numpy(self.ugridF.GetPoints().GetData()), \
                        tempPresLinF, self.densityF, \
                        self.gravity_x, self.gravity_y, self.gravity_z, self.PO)
            self.ugridF.GetPointData().SetScalars( \
                numpy_to_vtk(tempPresQuadF, deep=1, array_type=vtk.VTK_DOUBLE))
            self.ugridF.GetPointData().GetScalars().SetName("pressure")
            self.minPressureF, self.maxPressureF = \
                self.ugridF.GetPointData().GetScalars().GetRange()
            logging.debug("fluid pressure range: [%.2f, %.2f]" \
                          % (self.minPressureF, self.maxPressureF))
            self.boolUpdatePresF = False
        logging.debug("update fluid pressure completed")
    
    # update fluid pressure
    def updatePhiF(self):
        logging.debug("update directional scalars (fluid)")
        if self.boolUpdateSpaceF:
            logging.debug("unstructured grid for fluid will be updated first")
            self.updateSpaceF()
        if self.boolUpdatePhiF \
            and (os.path.exists(self.baseDirectory \
                 +self.dataFolder \
                 +self.filenamePhiF \
                 +str(self.currentT) \
                 +self.filenameSuffix)):
            tempPhiF = readCheartData.readScalars( \
                self.baseDirectory \
                +self.dataFolder \
                +self.filenamePhiF \
                +str(self.currentT) \
                +self.filenameSuffix)
            self.ugridF.GetPointData().AddArray( \
                organiseData.numpy2vtkDataArray1(tempPhiF, "phi"))
            self.minPhiF, self.maxPhiF = \
                self.ugridF.GetPointData().GetVectors("phi").GetRange()
            logging.debug("directional scalars (fluid) range: [%.2f, %.2f]" \
                          % (self.minPhiF, self.maxPhiF))
            self.boolUpdatePhiF = False
        logging.debug("update directional scalars (fluid) completed")
    
    # update solid node coordinates
    def updateSpaceS(self):
        logging.debug("update solid space")
        if (self.meshTypeS == 22) or (self.meshTypeS == 24):
            if self.ugridS == []:
                self.ugridS      = vtk.vtkUnstructuredGrid()
                self.ugridCellsS = vtk.vtkUnstructuredGrid()
                if self.numberOfDimensions == 3:
                    self.cellTypesS = vtk.vtkQuadraticTetra().GetCellType()
                    divby = 11
                    # read tetrahedrons
                    self.tempElemS = readCheartData.readTriQuadAsLin( \
                        self.baseDirectory \
                        +self.meshFolder \
                        +self.filenameTopoQuadS, \
                        self.numberOfDimensions)
                    # create cells for unstructured grid
                    tempElemLinS, cellstypesS, cellslocationsS = \
                        readCheartData.createTopology3Dquad(self.tempElemS, \
                        self.cellTypesS)
                    cellsS = vtk.vtkCellArray()
                    cellsS.SetCells(int(tempElemLinS.shape[0]/divby), \
                        numpy_to_vtk(tempElemLinS, deep=1, \
                        array_type=vtk.vtkIdTypeArray().GetDataType()))
                    # assign cells
                    self.ugridS.SetCells( \
                        numpy_to_vtk(cellstypesS, deep=1, \
                        array_type=vtk.vtkUnsignedCharArray().GetDataType()), \
                        numpy_to_vtk(cellslocationsS, deep = 1, \
                                   array_type=vtk.vtkIdTypeArray().GetDataType()),
                                   cellsS)
                    # linears (see fluid)
                    ct = vtk.vtkTetra().GetCellType()
                    divby = 5
                    # create cells for unstructured grid
                    tempElemLinS, cellstypesS, cellslocationsS = \
                        readCheartData.createTopology3Dcells(self.tempElemS, \
                        ct)
                    cellsS = vtk.vtkCellArray()
                    cellsS.SetCells(int(tempElemLinS.shape[0]/divby), \
                        numpy_to_vtk(tempElemLinS, deep=1, \
                        array_type=vtk.vtkIdTypeArray().GetDataType()))
                    # assign cells
                    self.ugridCellsS.SetCells( \
                        numpy_to_vtk(cellstypesS, deep=1, \
                        array_type=vtk.vtkUnsignedCharArray().GetDataType()), \
                        numpy_to_vtk(cellslocationsS, deep = 1, \
                                   array_type=vtk.vtkIdTypeArray().GetDataType()),
                                   cellsS)
                else:
                    # quadratic triangle mesh
                    self.cellTypesS = vtk.vtkQuadraticTriangle().GetCellType()
                    divby = 7
                    # read triangles
                    self.tempElemS = readCheartData.readTriQuadAsLin( \
                        self.baseDirectory \
                        +self.meshFolder \
                        +self.filenameTopoQuadS, \
                        self.numberOfDimensions)
                    # create cells for unstructured grid
                    tempElemLinS, cellstypesS, cellslocationsS = \
                        readCheartData.createTopology2Dquad(self.tempElemS, \
                        self.cellTypesS)
                    cellsS = vtk.vtkCellArray()
                    cellsS.SetCells(int(tempElemLinS.shape[0]/divby), \
                        numpy_to_vtk(tempElemLinS, deep=1, \
                        array_type=vtk.vtkIdTypeArray().GetDataType()))
                    # assign cells
                    self.ugridS.SetCells(numpy_to_vtk(cellstypesS, deep=1, \
                        array_type=vtk.vtkUnsignedCharArray().GetDataType()),
                                   numpy_to_vtk(cellslocationsS, deep = 1, \
                                   array_type=vtk.vtkIdTypeArray().GetDataType()),
                                   cellsS)
                    
                    ## create a linear triangle mesh too for cell quality
                    ct = vtk.vtkTriangle().GetCellType()
                    divby = 4
                    # create cells for unstructured grid
                    tempElemLinS, cellstypesS, cellslocationsS = \
                        readCheartData.createTopology2D(self.tempElemS, \
                        ct)
                    cellsS = vtk.vtkCellArray()
                    cellsS.SetCells(int(tempElemLinS.shape[0]/divby), \
                        numpy_to_vtk(tempElemLinS, deep=1, \
                        array_type=vtk.vtkIdTypeArray().GetDataType()))
                    # assign cells
                    self.ugridCellsS.SetCells(numpy_to_vtk(cellstypesS, deep=1, \
                        array_type=vtk.vtkUnsignedCharArray().GetDataType()),
                                   numpy_to_vtk(cellslocationsS, deep = 1, \
                                   array_type=vtk.vtkIdTypeArray().GetDataType()),
                                   cellsS)
        elif (self.meshTypeS == 23) or (self.meshTypeS == 25) or (self.meshTypeS == 29):
            if self.sgridS == []:
                # use unstructured grid here as well (for now)
                self.sgridS      = vtk.vtkUnstructuredGrid()
                self.sgridCellsS = vtk.vtkUnstructuredGrid()
                if self.numberOfDimensions == 3:
                    print "structured grid - 3D"
                    self.cellTypesS = vtk.vtkTriQuadraticHexahedron().GetCellType()
                    divby = 28
                    # read hexahedrons
                    self.tempElemS = readCheartData.readQuadHex( \
                        self.baseDirectory \
                        +self.meshFolder \
                        +self.filenameTopoQuadS, \
                        self.numberOfDimensions)
                    # create cells for unstructured grid
                    tempElemLinS, cellstypesS, cellslocationsS = \
                        readCheartData.createTopology3Dquad(self.tempElemS, \
                        self.cellTypesS)
                    cellsS = vtk.vtkCellArray()
                    cellsS.SetCells(int(tempElemLinS.shape[0]/divby), \
                        numpy_to_vtk(tempElemLinS, deep=1, \
                        array_type=vtk.vtkIdTypeArray().GetDataType()))
                    # assign cells
                    self.sgridS.SetCells( \
                        numpy_to_vtk(cellstypesS, deep=1, \
                        array_type=vtk.vtkUnsignedCharArray().GetDataType()), \
                        numpy_to_vtk(cellslocationsS, deep = 1, \
                                   array_type=vtk.vtkIdTypeArray().GetDataType()),
                                   cellsS)
                elif self.numberOfDimensions == 2:
                    print "structured grid - 2D ::: not implemented"
        else:
            print "unsupported mesh type (solid): ", self.meshTypeS
        if self.boolUpdateSpaceS:
            # read points
            pointsS = vtk.vtkPoints()
            if self.boolVarDispSpace.get():
                filename1 = self.baseDirectory \
                    +self.dataFolder \
                    +self.filenameSpaceS \
                    +"1" \
                    +self.filenameSuffix
                if not(os.path.exists(filename1)):
                    filename1 = self.baseDirectory \
                        +self.dataFolder \
                        +self.filenameSpaceS \
                        +str(self.currentT) \
                        +self.filenameSuffix
                    if not(os.path.exists(filename1)):
                        print "The following file does not exist:\n" \
                            +filename1
                        return -1
                filename2 = self.baseDirectory \
                    +self.dataFolder \
                    +self.filenameDisp \
                    +str(self.currentT) \
                    +self.filenameSuffix
                tempCoordS, tempDisp, self.numberOfDimensions = \
                    readCheartData.readCoordDisp(filename1, filename2)
                if not(self.ugridS == []):
                    self.ugridS.GetPointData().SetVectors( \
                        organiseData.numpy2vtkDataArray(tempDisp, "displacement"))
                    self.minMagDisp, self.maxMagDisp = \
                        self.ugridS.GetPointData().GetVectors().GetRange(-1)
                    self.minDisp0, self.maxDisp0 = \
                        self.ugridS.GetPointData().GetVectors().GetRange(0)
                    self.minDisp1, self.maxDisp1 = \
                        self.ugridS.GetPointData().GetVectors().GetRange(1)
                    self.minDisp2, self.maxDisp2 = \
                        self.ugridS.GetPointData().GetVectors().GetRange(2)
                else:
                    self.sgridS.GetPointData().SetVectors( \
                        organiseData.numpy2vtkDataArray(tempDisp, "displacement"))
                    self.minMagDisp, self.maxMagDisp = \
                        self.sgridS.GetPointData().GetVectors().GetRange(-1)
                    self.minDisp0, self.maxDisp0 = \
                        self.sgridS.GetPointData().GetVectors().GetRange(0)
                    self.minDisp1, self.maxDisp1 = \
                        self.sgridS.GetPointData().GetVectors().GetRange(1)
                    self.minDisp2, self.maxDisp2 = \
                        self.sgridS.GetPointData().GetVectors().GetRange(2)
                    self.boolUpdateDisp = False
            else:
                tempCoordS, self.numberOfDimensions = \
                    readCheartData.readVectors(self.baseDirectory \
                                               +self.dataFolder \
                                               +self.filenameSpaceS \
                                               +str(self.currentT) \
                                               +self.filenameSuffix)
            pointsS.SetData(numpy_to_vtk(tempCoordS, \
                deep=1, array_type=vtk.VTK_DOUBLE))
            # assign points
            if not(self.ugridS == []):
                self.ugridS.SetPoints(pointsS)
                self.ugridCellsS.SetPoints(pointsS)
                self.minXS, self.maxXS, self.minYS, self.maxYS, self.minZS, self.maxZS = \
                    self.ugridS.GetPoints().GetBounds()
            else:
                self.sgridS.SetPoints(pointsS)
                self.sgridCellsS.SetPoints(pointsS)
                self.minXS, self.maxXS, self.minYS, self.maxYS, self.minZS, self.maxZS = \
                    self.sgridS.GetPoints().GetBounds()
            self.boolUpdateSpaceS = False
        logging.debug("update solid space completed")
    
    # update solid displacement
    def updateDisp(self):
        logging.debug("update solid displacement")
        if ((self.ugridS == []) or (self.sgridS == [])) or self.boolUpdateSpaceS:
            logging.debug("unstructured grid for solid will be updated first")
            self.updateSpaceS()
        if self.boolUpdateDisp:
            tempDisp, numberOfDimensions = \
                readCheartData.readVectors(self.baseDirectory \
                                           +self.dataFolder \
                                           +self.filenameDisp \
                                           +str(self.currentT) \
                                           +self.filenameSuffix)
            if not(self.ugridS == []):
                self.ugridS.GetPointData().SetVectors( \
                    organiseData.numpy2vtkDataArray(tempDisp, "displacement"))
                if self.numberOfDimensions != numberOfDimensions:
                    logging.debug("ERROR: number of dimensions of solid space is " \
                                  % self.numberOfDimensions)
                    logging.debug("ERROR: number of solid displacement components is " \
                                  % numberOfDimensions)
                self.minMagDisp, self.maxMagDisp = \
                    self.ugridS.GetPointData().GetVectors("displacement").GetRange(-1)
                self.minDisp0, self.maxDisp0 = \
                    self.ugridS.GetPointData().GetVectors("displacement").GetRange(0)
                self.minDisp1, self.maxDisp1 = \
                    self.ugridS.GetPointData().GetVectors("displacement").GetRange(1)
                self.minDisp2, self.maxDisp2 = \
                    self.ugridS.GetPointData().GetVectors("displacement").GetRange(2)
            else:
                self.sgridS.GetPointData().SetVectors( \
                    organiseData.numpy2vtkDataArray(tempDisp, "displacement"))
                if self.numberOfDimensions != numberOfDimensions:
                    logging.debug("ERROR: number of dimensions of solid space is " \
                                  % self.numberOfDimensions)
                    logging.debug("ERROR: number of solid displacement components is " \
                                  % numberOfDimensions)
                self.minMagDisp, self.maxMagDisp = \
                    self.sgridS.GetPointData().GetVectors("displacement").GetRange(-1)
                self.minDisp0, self.maxDisp0 = \
                    self.sgridS.GetPointData().GetVectors("displacement").GetRange(0)
                self.minDisp1, self.maxDisp1 = \
                    self.sgridS.GetPointData().GetVectors("displacement").GetRange(1)
                self.minDisp2, self.maxDisp2 = \
                    self.sgridS.GetPointData().GetVectors("displacement").GetRange(2)
            logging.debug("solid displacement magnitude range: [%.2f, %.2f]" \
                          % (self.minMagDisp, self.maxMagDisp))
            logging.debug("solid displacement x-range: [%.2f, %.2f]" \
                          % (self.minDisp0, self.maxDisp0))
            logging.debug("solid displacement y-range: [%.2f, %.2f]" \
                          % (self.minDisp1, self.maxDisp1))
            logging.debug("solid displacement z-range: [%.2f, %.2f]" \
                          % (self.minDisp2, self.maxDisp2))
            self.boolUpdateDisp = False
        logging.debug("update solid displacement completed")
    
    # update solid displacement
    def updateSolVel(self):
        logging.debug("update solid velocity")
        if ((self.ugridS == []) or (self.sgridS == [])) or self.boolUpdateSpaceS:
            logging.debug("unstructured grid for solid will be updated first")
            self.updateSpaceS()
        if self.boolUpdateSolVel \
            and (os.path.exists(self.baseDirectory \
                 +self.dataFolder \
                 +self.filenameSolVel \
                 +str(self.currentT) \
                 +self.filenameSuffix)):
            tempSolVel, numberOfDimensions = \
                readCheartData.readVectors(self.baseDirectory \
                                           +self.dataFolder \
                                           +self.filenameSolVel \
                                           +str(self.currentT) \
                                           +self.filenameSuffix)
            if not(self.ugridS == []):
                self.ugridS.GetPointData().AddArray( \
                    organiseData.numpy2vtkDataArray(tempSolVel, "velocity"))
                if self.numberOfDimensions != numberOfDimensions:
                    logging.debug("ERROR: number of dimensions of solid space is " \
                                  % self.numberOfDimensions)
                    logging.debug("ERROR: number of solid velocity components is " \
                                  % numberOfDimensions)
                self.minMagSolVel, self.maxMagSolVel = \
                    self.ugridS.GetPointData().GetVectors("velocity").GetRange(-1)
                self.minSolVel0, self.maxSolVel0 = \
                    self.ugridS.GetPointData().GetVectors("velocity").GetRange(0)
                self.minSolVel1, self.maxSolVel1 = \
                    self.ugridS.GetPointData().GetVectors("velocity").GetRange(1)
                self.minSolVel2, self.maxSolVel2 = \
                    self.ugridS.GetPointData().GetVectors("velocity").GetRange(2)
            else:
                self.sgridS.GetPointData().AddArray( \
                    organiseData.numpy2vtkDataArray(tempSolVel, "velocity"))
                if self.numberOfDimensions != numberOfDimensions:
                    logging.debug("ERROR: number of dimensions of solid space is " \
                                  % self.numberOfDimensions)
                    logging.debug("ERROR: number of solid velocity components is " \
                                  % numberOfDimensions)
                self.minMagSolVel, self.maxMagSolVel = \
                    self.sgridS.GetPointData().GetVectors("velocity").GetRange(-1)
                self.minSolVel0, self.maxSolVel0 = \
                    self.sgridS.GetPointData().GetVectors("velocity").GetRange(0)
                self.minSolVel1, self.maxSolVel1 = \
                    self.sgridS.GetPointData().GetVectors("velocity").GetRange(1)
                self.minSolVel2, self.maxSolVel2 = \
                    self.sgridS.GetPointData().GetVectors("velocity").GetRange(2)
            logging.debug("solid velocity magnitude range: [%.2f, %.2f]" \
                          % (self.minMagSolVel, self.maxMagSolVel))
            logging.debug("solid velocity x-range: [%.2f, %.2f]" \
                          % (self.minSolVel0, self.maxSolVel0))
            logging.debug("solid velocity y-range: [%.2f, %.2f]" \
                          % (self.minSolVel1, self.maxSolVel1))
            logging.debug("solid velocity z-range: [%.2f, %.2f]" \
                          % (self.minSolVel2, self.maxSolVel2))
            self.boolUpdateSolVel = False
        logging.debug("update solid velocity completed")
    
    # update solid pressure
    def updatePresS(self):
        logging.debug("update solid pressure")
        if not(self.ugridS == []):
            if self.tempMappingS == []:
                self.tempMappingS = readCheartData.findMappingLinQuad( \
                    self.baseDirectory \
                    +self.meshFolder \
                    +self.filenameTopoLinS, \
                    self.baseDirectory \
                    +self.meshFolder \
                    +self.filenameTopoQuadS, \
                    self.numberOfDimensions)
            if self.boolUpdateSpaceS:
                logging.debug("unstructured grid for solid will be updated first")
                self.updateSpaceS()
            if self.boolUpdatePresS:
                tempPresLinS = readCheartData.readScalars( \
                    self.baseDirectory \
                    +self.dataFolder \
                    +self.filenamePresS \
                    +str(self.currentT) \
                    +self.filenameSuffix)
                tempPresQuadS = readCheartData.interpolateLinToQuad( \
                    self.tempElemS, \
                    vtk_to_numpy(self.ugridS.GetPoints().GetData()), \
                    tempPresLinS, \
                    self.tempMappingS, \
                    self.numberOfDimensions)
                if self.boolEffectiveG.get():
                    tempPresQuadS = readCheartData.changeOfVariables( \
                        vtk_to_numpy(self.ugridS.GetPoints().GetData()), \
                        tempPresQuadS, self.densityF, \
                        self.gravity_x, self.gravity_y, self.gravity_z, self.PO)
                self.ugridS.GetPointData().SetScalars( \
                    numpy_to_vtk(tempPresQuadS, deep=1, array_type=vtk.VTK_DOUBLE))
                self.ugridS.GetPointData().GetScalars().SetName("pressure")
                self.minPressureS, self.maxPressureS = \
                    self.ugridS.GetPointData().GetScalars().GetRange()
                logging.debug("solid pressure range: [%.2f, %.2f]" \
                              % (self.minPressureS, self.maxPressureS))
                self.boolUpdatePresS = False
        else:
            if self.tempMappingS == []:
                self.tempMappingS = readCheartData.findMappingLinQuad_Hex( \
                    self.baseDirectory \
                    +self.meshFolder \
                    +self.filenameTopoLinS, \
                    self.baseDirectory \
                    +self.meshFolder \
                    +self.filenameTopoQuadS)
            if self.boolUpdateSpaceS:
                logging.debug("structured grid for solid will be updated first")
                self.updateSpaceS()
            if self.boolUpdatePresS:
                tempPresLinS = readCheartData.readScalars( \
                    self.baseDirectory \
                    +self.dataFolder \
                    +self.filenamePresS \
                    +str(self.currentT) \
                    +self.filenameSuffix)
                tempPresQuadS = readCheartData.interpolateLinToQuad_Hex( \
                    self.tempElemS, \
                    vtk_to_numpy(self.sgridS.GetPoints().GetData()), \
                    tempPresLinS, \
                    self.tempMappingS, \
                    self.numberOfDimensions)
                if self.boolEffectiveG.get():
                    tempPresQuadS = readCheartData.changeOfVariables( \
                        vtk_to_numpy(self.sgridS.GetPoints().GetData()), \
                        tempPresQuadS, self.densityF, \
                        self.gravity_x, self.gravity_y, self.gravity_z, self.PO)
                self.sgridS.GetPointData().SetScalars( \
                    numpy_to_vtk(tempPresQuadS, deep=1, array_type=vtk.VTK_DOUBLE))
                self.sgridS.GetPointData().GetScalars().SetName("pressure")
                self.minPressureS, self.maxPressureS = \
                    self.sgridS.GetPointData().GetScalars().GetRange()
                logging.debug("solid pressure range: [%.2f, %.2f]" \
                              % (self.minPressureS, self.maxPressureS))
                self.boolUpdatePresS = False
        logging.debug("update solid pressure completed")
    
    # define time sequence
    def defineSequence(self, win):
        self.installDirectoryStr = Tkinter.StringVar()
        self.baseDirectoryStr    = Tkinter.StringVar()
        self.dataFolderStr       = Tkinter.StringVar()
        self.meshFolderStr       = Tkinter.StringVar()
        self.installDirectoryStr.set(self.installDirectory)
        self.baseDirectoryStr.set(self.baseDirectory)
        self.dataFolderStr.set(self.dataFolder)
        self.meshFolderStr.set(self.meshFolder)
        self.fromTStr         = Tkinter.StringVar()
        self.toTStr           = Tkinter.StringVar()
        self.incrementStr     = Tkinter.StringVar()
        self.fromTStr.set(str(self.fromT))
        self.toTStr.set(str(self.toT))
        self.incrementStr.set(str(self.increment))
        
        self.popup = Tkinter.Toplevel(win.root)
        
        self.popup.configure(bg=win.linuxMintHEX)
        for i in range(6):
            self.popup.rowconfigure(i, weight=0)
        self.popup.columnconfigure(0, weight=0)
        self.popup.columnconfigure(1, weight=1)
        self.popup.columnconfigure(2, weight=0)
        self.popup.title("Import")
        ttk.Label(self.popup, text="Choose path:", style='My.TLabel') \
            .grid(    column=0, row=0, padx=3, sticky=Tkinter.W)
        ttk.Label(self.popup, text="Meshes folder:", style='My.TLabel') \
            .grid(  column=0, row=1, padx=3, sticky=Tkinter.W)
        ttk.Label(self.popup, text="Data folder:", style='My.TLabel') \
            .grid(    column=0, row=2, padx=3, sticky=Tkinter.W)
        ttk.Label(self.popup, text="First time step:", style='My.TLabel') \
            .grid(column=0, row=3, padx=3, sticky=Tkinter.W)
        ttk.Label(self.popup, text="Last time step:", style='My.TLabel') \
            .grid( column=0, row=4, padx=3, sticky=Tkinter.W)
        ttk.Label(self.popup, text="Increment:", style='My.TLabel') \
            .grid(      column=0, row=5, padx=3, sticky=Tkinter.W)
        WIDTH = 80
        
        
        pathEntry = ttk.Entry(self.popup, width=WIDTH, \
            textvariable=self.baseDirectoryStr, justify=Tkinter.LEFT)
        meshesFolderEntry = ttk.Entry(self.popup, width=WIDTH, \
            textvariable=self.meshFolderStr, justify=Tkinter.LEFT)
        dataFolderEntry = ttk.Entry(self.popup, width=WIDTH, \
            textvariable=self.dataFolderStr, justify=Tkinter.LEFT)
        beginningEntry = ttk.Entry(self.popup, width=WIDTH, \
            textvariable=self.fromTStr, justify=Tkinter.LEFT)
        endEntry = ttk.Entry(self.popup, width=WIDTH, \
            textvariable=self.toTStr, justify=Tkinter.LEFT)
        incrementEntry = ttk.Entry(self.popup, width=WIDTH, \
            textvariable=self.incrementStr, justify=Tkinter.LEFT)
        pathEntry.grid(        column=1, row=0, sticky=(Tkinter.W, Tkinter.E))
        meshesFolderEntry.grid(column=1, row=1, sticky=(Tkinter.W, Tkinter.E))
        dataFolderEntry.grid(  column=1, row=2, sticky=(Tkinter.W, Tkinter.E))
        beginningEntry.grid(   column=1, row=3, sticky=(Tkinter.W, Tkinter.E))
        endEntry.grid(         column=1, row=4, sticky=(Tkinter.W, Tkinter.E))
        incrementEntry.grid(   column=1, row=5, sticky=(Tkinter.W, Tkinter.E))
        
        def setBaseDirectory():
            self.baseDirectory = tkFileDialog.askdirectory(parent=self.popup, \
                initialdir=self.baseDirectory, mustexist=1) + "/"
            self.baseDirectoryStr.set(str(self.baseDirectory))
        
        ttk.Button(self.popup, image=win.useFolderIcon, \
            command=setBaseDirectory, style='My.TButton').grid( \
            column = 2, row = 0, padx=3)
        
        toolbarChangeOfVariablesOKbutton = ttk.Checkbutton(self.popup, \
            variable=self.boolEffectiveG, \
            text='change-of-variables', style='My.TCheckbutton')
        toolbarChangeOfVariablesOKbutton.grid(column=1, row=6, \
            sticky=(Tkinter.W, Tkinter.E))
        if self.boolEffectiveG.get():
            toolbarChangeOfVariablesOKbutton.state(["selected"])
        toolbarDispOKbutton = ttk.Checkbutton(self.popup, \
            variable=self.boolVarDispSpace, \
            text='Space = SpaceO + Disp', style='My.TCheckbutton')
        if self.boolVarDispSpace.get():
            toolbarDispOKbutton.state(["selected"])
        toolbarDispOKbutton.grid(column=1, row=7, sticky=(Tkinter.W, Tkinter.E))
        
        toolbarFluid = ttk.Checkbutton(self.popup, \
            variable=self.visualizeFluid, \
            text='Visualize fluid', style='My.TCheckbutton')
        if self.visualizeFluid.get():
            toolbarFluid.state(["selected"])
        toolbarFluid.grid(column=1, row=8, \
            sticky=(Tkinter.W, Tkinter.E))
        toolbarSolid = ttk.Checkbutton(self.popup, \
            variable=self.visualizeSolid, \
            text='Visualize solid', style='My.TCheckbutton')
        if self.visualizeSolid.get():
            toolbarSolid.state(["selected"])
        toolbarSolid.grid(column=1, row=9, \
            sticky=(Tkinter.W, Tkinter.E))
        toolbarInterface = ttk.Checkbutton(self.popup, \
            variable=self.visualizeInterface, \
            text='Visualize interface', style='My.TCheckbutton')
        if self.visualizeInterface.get():
            toolbarInterface.state(["selected"])
        toolbarInterface.grid(column=1, row=10, \
            sticky=(Tkinter.W, Tkinter.E))
        
        toolbarDispOK = ttk.Frame(self.popup, borderwidth=5, style='My.TFrame')
        toolbarDispOK.grid(row=11, column=1, columnspan=2, \
            sticky=(Tkinter.W, Tkinter.E))
        
        def importOK():
            self.baseDirectory = self.baseDirectoryStr.get()
            self.dataFolder    = self.dataFolderStr.get()
            self.meshFolder    = self.meshFolderStr.get()
            self.fromT = int(self.fromTStr.get())
            self.toT   = int(self.toTStr.get())
            self.increment = int(self.incrementStr.get())
            self.currentT = self.fromT
            self.importData(win)
            self.createDataSetMappers()
            self.popup.destroy()
        
        importOKButton = ttk.Button(toolbarDispOK, text = "Update & exit", \
            command=importOK, style='My.TButton')
        importOKButton.pack(side=Tkinter.RIGHT, fill=Tkinter.X, padx=1)
    
    # configure vtk renderer
    def configureRenderer(self):
        self.renderer.SetBackground(1.0, 1.0, 1.0)
        self.renderer.SetBackground2(0.0, 0.0, 0.0)
        self.renderer.GradientBackgroundOn()
        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()
    
    # add sphere to default scene
    def addSphere(self):
        self.sphereSource = vtk.vtkSphereSource()
        self.sphereSource.SetCenter(0, 0, 0)
        self.sphereSource.SetRadius(0.5)
        self.sphereMapper = vtk.vtkPolyDataMapper()
        self.sphereMapper.SetInput(self.sphereSource.GetOutput())
        self.sphereActor = vtk.vtkActor()
        self.sphereActor.SetMapper(self.sphereMapper)
        self.renderer.AddActor(self.sphereActor)
    
    # configure camera
    def configureCamera(self):
        self.cameraUp0Str = Tkinter.StringVar()
        self.cameraUp1Str = Tkinter.StringVar()
        self.cameraUp2Str = Tkinter.StringVar()
        self.cameraUp0Str.set(str(self.cameraUp0))
        self.cameraUp1Str.set(str(self.cameraUp1))
        self.cameraUp2Str.set(str(self.cameraUp2))
        self.cameraPos0Str = Tkinter.StringVar()
        self.cameraPos1Str = Tkinter.StringVar()
        self.cameraPos2Str = Tkinter.StringVar()
        self.cameraPos0Str.set(str(self.cameraPos0))
        self.cameraPos1Str.set(str(self.cameraPos1))
        self.cameraPos2Str.set(str(self.cameraPos2))
        self.camera = vtk.vtkCamera()
        self.parallelProjection = Tkinter.BooleanVar()
        self.parallelProjection.set(False)
        self.camera.SetParallelProjection(self.parallelProjection.get())
        self.camera.SetViewUp( \
            self.cameraUp0, self.cameraUp1, self.cameraUp2)
        self.camera.SetPosition( \
            self.cameraPos0, self.cameraPos1, self.cameraPos2)
    
    # modify camera position and view-up
    def modifyCamera(self, win):
        def cameraUpdate():
            self.cameraUp0 = float(self.cameraUp0Str.get())
            self.cameraUp1 = float(self.cameraUp1Str.get())
            self.cameraUp2 = float(self.cameraUp2Str.get())
            self.cameraPos0 = float(self.cameraPos0Str.get())
            self.cameraPos1 = float(self.cameraPos1Str.get())
            self.cameraPos2 = float(self.cameraPos2Str.get())
            self.camera.SetViewUp( \
                self.cameraUp0, self.cameraUp1, self.cameraUp2)
            self.camera.SetPosition( \
                self.cameraPos0, self.cameraPos1, self.cameraPos2)
            self.camera.SetParallelProjection(self.parallelProjection.get())
            self.renderer.SetActiveCamera(self.camera)
            self.renderer.ResetCamera()
            self.renderWindow.Render()
        def cameraExit():
            self.cameraWindow.destroy()
        self.cameraWindow = Tkinter.Toplevel(win.root)
        localFrame   = ttk.Frame(self.cameraWindow, style='My.TFrame')
        localFrame.pack(fill=Tkinter.BOTH, expand=True)
        self.cameraWindow.title("Camera")
        ttk.Label(localFrame, text="View up:", \
            style='My.TLabel').grid(column = 0, row = 0)
        cameraUp1Entry = ttk.Entry(localFrame, width=5, \
            textvariable=self.cameraUp0Str, justify=Tkinter.RIGHT)
        cameraUp2Entry = ttk.Entry(localFrame, width=5, \
            textvariable=self.cameraUp1Str, justify=Tkinter.RIGHT)
        cameraUp3Entry = ttk.Entry(localFrame, width=5, \
            textvariable=self.cameraUp2Str, justify=Tkinter.RIGHT)
        cameraUp1Entry.grid(column=1, row=0)
        cameraUp2Entry.grid(column=2, row=0)
        cameraUp3Entry.grid(column=3, row=0)
        ttk.Label(localFrame, text="Camera position:", \
            style='My.TLabel').grid(column=0, row=1)
        cameraPos1Entry = ttk.Entry(localFrame, width=5, \
            textvariable=self.cameraPos0Str, justify=Tkinter.RIGHT)
        cameraPos2Entry = ttk.Entry(localFrame, width=5, \
            textvariable=self.cameraPos1Str, justify=Tkinter.RIGHT)
        cameraPos3Entry = ttk.Entry(localFrame, width=5, \
            textvariable=self.cameraPos2Str, justify=Tkinter.RIGHT)
        cameraPos1Entry.grid(column=1, row=1)
        cameraPos2Entry.grid(column=2, row=1)
        cameraPos3Entry.grid(column=3, row=1)
        parallelProjectionOnOff = ttk.Checkbutton(localFrame, \
            variable=self.parallelProjection, \
            text='Parallel projection', style='My.TCheckbutton')
        parallelProjectionOnOff.grid(column = 1, row = 3)
        if self.parallelProjection.get():
            parallelProjectionOnOff.state(["selected"])
        ttk.Button(localFrame, text = "Update", command=cameraUpdate, \
            style='My.TButton').grid(column = 2, row = 3)
        ttk.Button(localFrame, text = "Exit", command=cameraExit, \
            style='My.TButton').grid(column = 3, row = 3)
    
    # save screenshot
    def screenshot(self):
        self.renderWindow.Render()
        if self.window2imageFilter == []:
            self.window2imageFilter = vtk.vtkWindowToImageFilter()
            self.window2imageFilter.SetInput(self.renderWindow)
        if self.pngWriter == []:
            self.pngWriter = vtk.vtkPNGWriter()
        if self.boolMagnification == False:
            screenshotFilename = self.baseDirectory + self.screenshotFolderStr.get() \
                + ("timestep_%05d.png" % (self.currentT))
            self.pngWriter.SetInput(self.window2imageFilter.GetOutput())
        else:
            # TODO always resizes to initial window size..
            screenshotFilename = self.baseDirectory + self.screenshotFolderStr.get() \
                + ("large_timestep_%05d.png" % (self.currentT))
            #self.renderLarge.SetInput(self.renderer)
        self.window2imageFilter.Modified()
        self.pngWriter.SetFileName(screenshotFilename)
        self.pngWriter.Write()
        print("Saved %s" % (screenshotFilename))
        self.screenshotCounter += 1
    
    # modify view port background colors
    def modifyBackground(self, arg2):
        if self.backgroundDropDown.current() == 0:
            self.renderer.SetBackground(0.0, 0.0, 0.0)
            self.renderer.SetBackground2(0.0, 0.0, 0.0)
            if not(self.scalarBarF == []):
                self.scalarBarF.GetLabelTextProperty().SetColor(1, 1, 1)
                self.scalarBarF.GetTitleTextProperty().SetColor(1, 1, 1)
            if not(self.scalarBarS == []):
                self.scalarBarS.GetLabelTextProperty().SetColor(1, 1, 1)
                self.scalarBarS.GetTitleTextProperty().SetColor(1, 1, 1)
            if not(self.scalarBarI == []):
                self.scalarBarI.GetLabelTextProperty().SetColor(1, 1, 1)
                self.scalarBarI.GetTitleTextProperty().SetColor(1, 1, 1)
        elif self.backgroundDropDown.current() == 1:
            self.renderer.SetBackground(1.0, 1.0, 1.0)
            self.renderer.SetBackground2(0.0, 0.0, 0.0)
            if not(self.scalarBarF == []):
                self.scalarBarF.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarF.GetTitleTextProperty().SetColor(0, 0, 0)
            if not(self.scalarBarS == []):
                self.scalarBarS.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarS.GetTitleTextProperty().SetColor(0, 0, 0)
            if not(self.scalarBarI == []):
                self.scalarBarI.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarI.GetTitleTextProperty().SetColor(0, 0, 0)
        elif self.backgroundDropDown.current() == 2:
            self.renderer.SetBackground(1.0, 1.0, 1.0)
            self.renderer.SetBackground2(1.0, 1.0, 1.0)
            if not(self.scalarBarF == []):
                self.scalarBarF.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarF.GetTitleTextProperty().SetColor(0, 0, 0)
            if not(self.scalarBarS == []):
                self.scalarBarS.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarS.GetTitleTextProperty().SetColor(0, 0, 0)
            if not(self.scalarBarI == []):
                self.scalarBarI.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarI.GetTitleTextProperty().SetColor(0, 0, 0)
        elif self.backgroundDropDown.current() == 3:
            self.renderer.SetBackground(0.0, 0.0, 0.0)
            self.renderer.SetBackground2(1.0, 1.0, 1.0)
            if not(self.scalarBarF == []):
                self.scalarBarF.GetLabelTextProperty().SetColor(1, 1, 1)
                self.scalarBarF.GetTitleTextProperty().SetColor(1, 1, 1)
            if not(self.scalarBarS == []):
                self.scalarBarS.GetLabelTextProperty().SetColor(1, 1, 1)
                self.scalarBarS.GetTitleTextProperty().SetColor(1, 1, 1)
            if not(self.scalarBarI == []):
                self.scalarBarI.GetLabelTextProperty().SetColor(1, 1, 1)
                self.scalarBarI.GetTitleTextProperty().SetColor(1, 1, 1)
        elif self.backgroundDropDown.current() == 4:
            self.rgb, self.hexx = \
                tkColorChooser.askcolor(initialcolor=self.hexx)
            self.customBG0 = self.rgb[0] / 255.0
            self.customBG1 = self.rgb[1] / 255.0
            self.customBG2 = self.rgb[2] / 255.0
            self.renderer.SetBackground( \
                self.customBG0, self.customBG1, self.customBG2)
            self.renderer.SetBackground2( \
                self.customBG0, self.customBG1, self.customBG2)
            if not(self.scalarBarF == []):
                self.scalarBarF.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarF.GetTitleTextProperty().SetColor(0, 0, 0)
            if not(self.scalarBarS == []):
                self.scalarBarS.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarS.GetTitleTextProperty().SetColor(0, 0, 0)
            if not(self.scalarBarI == []):
                self.scalarBarI.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarI.GetTitleTextProperty().SetColor(0, 0, 0)
        elif self.backgroundDropDown.current() == 5:
            self.rgb, self.hexx = \
                tkColorChooser.askcolor(initialcolor=self.hexx)
            self.customBG0 = self.rgb[0] / 255.0
            self.customBG1 = self.rgb[1] / 255.0
            self.customBG2 = self.rgb[2] / 255.0
            self.renderer.SetBackground(1.0, 1.0, 1.0)
            self.renderer.SetBackground2( \
                self.customBG0, self.customBG1, self.customBG2)
            if not(self.scalarBarF == []):
                self.scalarBarF.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarF.GetTitleTextProperty().SetColor(0, 0, 0)
            if not(self.scalarBarS == []):
                self.scalarBarS.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarS.GetTitleTextProperty().SetColor(0, 0, 0)
            if not(self.scalarBarI == []):
                self.scalarBarI.GetLabelTextProperty().SetColor(0, 0, 0)
                self.scalarBarI.GetTitleTextProperty().SetColor(0, 0, 0)
        self.renderWindow.Render()
    
    # import first time step
    def importData(self, win):
        t0 = time.time()
        self.renderer.RemoveActor(self.sphereActor)
        
        print " data:   ", self.baseDirectory+self.dataFolder, \
              "\n meshes: ", self.baseDirectory+self.meshFolder, \
              "\n\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" \
              ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
        
        win.root.title("FSIViewer: "+self.baseDirectory+self.dataFolder)
        
        # firstly, get number of dimensions of mesh
        if os.path.exists(str(self.baseDirectory \
                + self.dataFolder \
                + self.filenameSpaceF \
                + str(self.currentT) \
                + self.filenameSuffix)):
            getNumberOfDimensions = open(str(self.baseDirectory \
                + self.dataFolder \
                + self.filenameSpaceF \
                + str(self.currentT) \
                + self.filenameSuffix), 'r')
        elif os.path.exists(str(self.baseDirectory \
                + self.dataFolder \
                + self.filenameSpaceS \
                + str(self.currentT) \
                + self.filenameSuffix)):
            getNumberOfDimensions = open(str(self.baseDirectory \
                + self.dataFolder \
                + self.filenameSpaceS \
                + str(self.currentT) \
                + self.filenameSuffix), 'r')
        elif os.path.exists(str(self.baseDirectory \
                + self.dataFolder \
                + self.filenameSpaceI \
                + str(self.currentT) \
                + self.filenameSuffix)):
            getNumberOfDimensions = open(str(self.baseDirectory \
                + self.dataFolder \
                + self.filenameSpaceI \
                + str(self.currentT) \
                + self.filenameSuffix), 'r')
        firstLine = getNumberOfDimensions.readline()
        getNumberOfDimensions.close()
        temp = firstLine.split()
        self.numberOfDimensions = int(temp[1])
        # secondly, get mesh type (tri/tet or quad/hex)
        # -- obtained from linear topology
        print " mesh types:"
        if self.visualizeFluid.get():
            getMeshType = open(str(self.baseDirectory \
                + self.meshFolder \
                + self.filenameTopoLinF), 'r')
            firstLine = getMeshType.readline()
            firstLine = getMeshType.readline()
            getMeshType.close()
            temp = firstLine.split()
            if len(temp) == 2:
                self.meshTypeF = 21
                print "  F: "+str(self.meshTypeF)+" (line)"
            elif len(temp) == 3:
                self.meshTypeF = 22
                print "  F: "+str(self.meshTypeF)+" (tri)"
            elif len(temp) == 4 and self.numberOfDimensions == 2:
                self.meshTypeF = 23
                print "  F: "+str(self.meshTypeF)+" (quad)"
            elif len(temp) == 4 and self.numberOfDimensions == 3:
                getMeshType = open(str(self.baseDirectory \
                    + self.meshFolder \
                    + self.filenameTopoQuadF), 'r')
                firstLine = getMeshType.readline()
                firstLine = getMeshType.readline()
                getMeshType.close()
                temp = firstLine.split()
                if len(temp) == 4:
                    self.meshTypeF = 10
                else:
                    self.meshTypeF = 24
                print "  F: "+str(self.meshTypeF)+" (tet)"
            elif len(temp) == 8 and self.numberOfDimensions == 3:
                self.meshTypeF = 25
                print "  F: "+str(self.meshTypeF)+" (hex)"
        if self.visualizeSolid.get():
            getMeshType = open(str(self.baseDirectory \
                + self.meshFolder \
                + self.filenameTopoLinS), 'r')
            firstLine = getMeshType.readline()
            firstLine = getMeshType.readline()
            getMeshType.close()
            temp = firstLine.split()
            # lines
            if len(temp) == 2:
                self.meshTypeS = 21
                print "  S: "+str(self.meshTypeS)+" (line)"
            # tris
            elif len(temp) == 3:
                self.meshTypeS = 22
                print "  S: "+str(self.meshTypeS)+" (tri)"
            # quads
            elif len(temp) == 4 and self.numberOfDimensions == 2:
                self.meshTypeS = 23
                print "  S: "+str(self.meshTypeS)+" (quad)"
            # tets
            elif len(temp) == 4 and self.numberOfDimensions == 3:
                self.meshTypeS = 24
                print "  S: "+str(self.meshTypeS)+" (tet)"
            elif len(temp) == 8 and self.numberOfDimensions == 3:
                self.meshTypeS = 29
                print "  S: "+str(self.meshTypeS)+" (hex)"
        if self.visualizeInterface.get():
            getMeshType = open(str(self.baseDirectory \
                + self.meshFolder \
                + self.filenameTopoQuadI), 'r')
            firstLine = getMeshType.readline()
            firstLine = getMeshType.readline()
            getMeshType.close()
            temp = firstLine.split()
            # quad lines
            if len(temp) == 3 and self.numberOfDimensions == 2:
                self.meshTypeI = 21
                print "  I: "+str(self.meshTypeI)+" (line)"
            elif len(temp) == 3 and self.numberOfDimensions == 3:
                self.meshTypeI = 5
                print "  I: "+str(self.meshTypeI)+" (tri)"
            # quad tris
            elif len(temp) == 6:
                self.meshTypeI = 22
                print "  I: "+str(self.meshTypeI)+" (tri)"
            elif len(temp) == 8:
                self.meshTypeI = 23
                print "  I: "+str(self.meshTypeI)+" (hex)"
            # else
            else:
                self.meshTypeI = 14000
                print "  I: -1 (unknown)"
        
        self.progress.grid()
        self.progress["value"] = 2
        self.progress.update()
        # now, import data
        if not(self.visualizeFluid.get()):
            self.showF = "none"
        else:
            self.updateSpaceF()
            self.progress["value"] = 10
            self.progress.update()
            self.updateVel()
            self.progress["value"] = 30
            self.progress.update()
            self.updateWel()
            self.progress["value"] = 40
            self.progress.update()
            self.updatePresF()
            self.progress["value"] = 50
            self.progress.update()
            self.updateVort()
            self.progress["value"] = 60
            self.progress.update()
            self.updatePhiF()
            self.progress["value"] = 70
            self.progress.update()
            self.updateQualityF()
        #self.readFluidPoints(self.baseDirectory \
        #    + self.submitFolder \
        #    + "FluidPoints-Phase-I.txt")
        #self.exportFluidPoints()
        if not(self.visualizeSolid.get()):
            self.showS = "none"
        else:
            self.updateSpaceS()
            self.updateDisp()
            self.updateSolVel()
            self.updatePresS()
            self.progress["value"] = 80
            self.progress.update()
            self.updateQualityS()
            self.progress["value"] = 90
            self.progress.update()
        if not(self.visualizeInterface.get()):
            self.showI = "none"
        else:
            self.updateSpaceI()
            self.updateLMult()
        self.progress["value"] = 100
        self.progress.update()
        self.progress.grid_remove()
        # enable tabs to interactively visualize fluid and solid fields
        if self.visualizeFluid.get(): win.notebook.tab(0, state="normal")
        if self.visualizeSolid.get(): win.notebook.tab(1, state="normal")
        if self.visualizeInterface.get(): win.notebook.tab(2, state="normal")
        win.notebook.enable_traversal()
        t1 = time.time()
        logging.debug("data import completed in %.2f seconds" % (t1-t0))
        self.timeSlider = Tkinter.Scale(win.mainframe, \
            from_=self.fromT, to=self.toT, \
            resolution=self.increment, \
            orient=Tkinter.HORIZONTAL, \
            command=self.updateScaleValue, \
            showvalue=0, \
            background=win.linuxMintHEX, foreground='black', \
            relief='flat', borderwidth=0)
        self.timeSlider.set(self.currentT)
        self.timeSlider.grid(padx=0, pady=5, column=2, row=win.gridy-1, \
            columnspan=win.gridx-3, sticky = (Tkinter.W, Tkinter.E))
        self.renderWindow.Render()
    
    def readFluidPoints(self, filename):
        self.fluidPoints = numpy.loadtxt(filename)
        a = self.fluidPoints.shape[0]
        b = self.fluidPoints.shape[1]
        print a, b
        for i in range(a):
            print self.fluidPoints[i][:]
    
    def exportFluidPoints(self):
        
        numpy.savetxt(self.baseDirectory \
            + self.submitFolder \
            + "FluidPoints-Phase-I-out.txt", self.fluidPoints)
    
