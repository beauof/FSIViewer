import vtk
import numpy
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy
import sys
sys.dont_write_bytecode = True

def assignElements2Dlin(mesh, elements):
    
    numRows, numCols = elements.shape
    
    # TODO can we do this faster?
    for i in range(numRows):
        v0, v1, v2, v3, v4, v5 = elements[i, :]
        tri1 = vtk.vtkTriangle()
        tri1.GetPointIds().SetId(0, v0)
        tri1.GetPointIds().SetId(1, v3)
        tri1.GetPointIds().SetId(2, v4)
        tri2 = vtk.vtkTriangle()
        tri2.GetPointIds().SetId(0, v3)
        tri2.GetPointIds().SetId(1, v1)
        tri2.GetPointIds().SetId(2, v5)
        tri3 = vtk.vtkTriangle()
        tri3.GetPointIds().SetId(0, v3)
        tri3.GetPointIds().SetId(1, v5)
        tri3.GetPointIds().SetId(2, v4)
        tri4 = vtk.vtkTriangle()
        tri4.GetPointIds().SetId(0, v4)
        tri4.GetPointIds().SetId(1, v5)
        tri4.GetPointIds().SetId(2, v2)
        mesh.InsertNextCell(tri1.GetCellType(), tri1.GetPointIds())
        mesh.InsertNextCell(tri1.GetCellType(), tri2.GetPointIds())
        mesh.InsertNextCell(tri1.GetCellType(), tri3.GetPointIds())
        mesh.InsertNextCell(tri1.GetCellType(), tri4.GetPointIds())
    return mesh

def assignElements3Dlin(mesh, elements):
    
    numRows, numCols = elements.shape
    tet = vtk.vtkTetra()
    # TODO can we do this faster?
    for i in range(numRows):
        v0, v1, v2, v3, v4, v5, v6, v7, v8, v9 = elements[i, :]
        '''
        tet.GetPointIds().SetId(0, v0)
        tet.GetPointIds().SetId(1, v4)
        tet.GetPointIds().SetId(2, v6)
        tet.GetPointIds().SetId(3, v7)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v6)
        tet.GetPointIds().SetId(1, v4)
        tet.GetPointIds().SetId(2, v5)
        tet.GetPointIds().SetId(3, v7)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v4)
        tet.GetPointIds().SetId(1, v1)
        tet.GetPointIds().SetId(2, v5)
        tet.GetPointIds().SetId(3, v8)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v6)
        tet.GetPointIds().SetId(1, v5)
        tet.GetPointIds().SetId(2, v2)
        tet.GetPointIds().SetId(3, v7)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v4)
        tet.GetPointIds().SetId(1, v8)
        tet.GetPointIds().SetId(2, v5)
        tet.GetPointIds().SetId(3, v7)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v2)
        tet.GetPointIds().SetId(1, v7)
        tet.GetPointIds().SetId(2, v5)
        tet.GetPointIds().SetId(3, v9)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v7)
        tet.GetPointIds().SetId(1, v5)
        tet.GetPointIds().SetId(2, v9)
        tet.GetPointIds().SetId(3, v8)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v7)
        tet.GetPointIds().SetId(1, v8)
        tet.GetPointIds().SetId(2, v9)
        tet.GetPointIds().SetId(3, v3)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        '''
        
        
        
        
        tet.GetPointIds().SetId(0, v0)
        tet.GetPointIds().SetId(1, v4)
        tet.GetPointIds().SetId(2, v6)
        tet.GetPointIds().SetId(3, v7)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v4)
        tet.GetPointIds().SetId(1, v1)
        tet.GetPointIds().SetId(2, v5)
        tet.GetPointIds().SetId(3, v8)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v6)
        tet.GetPointIds().SetId(1, v5)
        tet.GetPointIds().SetId(2, v2)
        tet.GetPointIds().SetId(3, v9)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v7)
        tet.GetPointIds().SetId(1, v8)
        tet.GetPointIds().SetId(2, v9)
        tet.GetPointIds().SetId(3, v3)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v6)
        tet.GetPointIds().SetId(1, v9)
        tet.GetPointIds().SetId(2, v7)
        tet.GetPointIds().SetId(3, v5)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v7)
        tet.GetPointIds().SetId(1, v5)
        tet.GetPointIds().SetId(2, v9)
        tet.GetPointIds().SetId(3, v8)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v6)
        tet.GetPointIds().SetId(1, v4)
        tet.GetPointIds().SetId(2, v5)
        tet.GetPointIds().SetId(3, v7)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
        
        tet.GetPointIds().SetId(0, v4)
        tet.GetPointIds().SetId(1, v5)
        tet.GetPointIds().SetId(2, v7)
        tet.GetPointIds().SetId(3, v8)
        mesh.InsertNextCell(tet.GetCellType(), tet.GetPointIds())
    return mesh


def numpy2vtkDataArray(npa, mystr):
#    print npa[1][0]
    size0, size1 = npa.shape
    data = vtk.vtkDoubleArray()
    data.SetNumberOfComponents(3)
    data.SetName(mystr)
    for i in range(size0):
        x = npa[i, 0]
        y = npa[i, 1]
        z = npa[i, 2]
        data.InsertNextTuple3(x, y, z)
    
    return data

def numpy2vtkDataArray1(npa, mystr):
#    print npa[1][0]
    size0 = npa.shape[0]
    data = vtk.vtkDoubleArray()
    data.SetNumberOfComponents(1)
    data.SetName(mystr)
    for i in range(size0):
        data.InsertNextValue(npa[i])
    
    return data

def numpy2vtkDataArray9(npa, mystr):
#    print npa[1][0]
    size0, size1 = npa.shape
    data = vtk.vtkDoubleArray()
    data.SetNumberOfComponents(9)
    data.SetName(mystr)
    for i in range(size0):
        data.InsertNextTuple9(npa[i, 0], npa[i, 1], npa[i, 2], npa[i, 3], npa[i, 4], npa[i, 5], npa[i, 6], npa[i, 7], npa[i, 8])
    
    return data


def numpy2vtkDataArrayInt(npa):
#    print npa[1][0]
    size0, size1 = npa.shape
    data = vtk.vtkIdTypeArray()
    data.SetNumberOfComponents(4)
#    data.SetName("CELLS")
    for i in range(size0):
        n0 = int(npa[i, 0])
        n1 = int(npa[i, 1])
        n2 = int(npa[i, 2])
        n3 = int(npa[i, 3])
        data.InsertNextTuple4(n0, n1, n2, n3)
    
    return data
