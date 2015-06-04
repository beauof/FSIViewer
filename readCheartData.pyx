# cython: profile=False
import numpy
import string
import sys
cimport numpy
cimport cython
from numpy cimport ndarray
from libc.stdio cimport *
from libc.math cimport sqrt
from libc.math cimport abs
from libc.math cimport pow

sys.dont_write_bytecode = True

INTTYPE = numpy.int
DOUBLETYPE = numpy.double
ctypedef numpy.int_t INTTYPE_t
ctypedef numpy.double_t DOUBLETYPE_t

# c functions we wanna use
cdef extern from "stdio.h":
    FILE *fopen(const char *, const char *)
    int fclose(FILE *)
    ssize_t getline(char **, size_t *, FILE *)
    double strtod(char*, char**)

# c reimplementation of python split() command
def splitLine(char* l):
    cdef char** j
    j = &l
    return strtod(l,j)
# returns zero if no value is given
def splitLine2(char* l):
    cdef char** j
    j = &l
    return strtod(l,j), strtod(j[0]+1,j)

def splitLine3(char* l):
    cdef char** j
    j = &l
    return strtod(l,j), strtod(j[0]+1,j), strtod(j[0]+1,j)

def splitLine4(char* l):
    cdef char** j
    j = &l
    return strtod(l,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j)

def splitLine6(char* l):
    cdef char** j
    j = &l
    return strtod(l,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j)

def splitLine10(char* l):
    cdef char** j
    j = &l
    return strtod(l,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j)

def splitLine8(char* l):
    cdef char** j
    j = &l
    return strtod(l,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j)

def splitLine27(char* l):
    cdef char** j
    j = &l
    return strtod(l,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j), strtod(j[0]+1,j)



# write numpy arrays to file (convenience method for vorticity)
def writeVectors(ndarray[numpy.double_t, ndim=2] towrite, str filename):
    # see:
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html#numpy.loadtxt
    cdef unsigned int numberOfNodes, numberOfComponents
    cdef str myheader
    
    numberOfNodes      = towrite.shape[0]
    numberOfComponents = towrite.shape[1]
    myheader = str(numberOfNodes) + ' ' + str(numberOfComponents)
    numpy.savetxt(filename, towrite, fmt='%.18e', delimiter=' ', newline='\n', header=myheader, footer='', comments='')
    
    return 1

# write numpy arrays to file (convenience method for mesh quality measure)
def writeScalars(ndarray[numpy.double_t, ndim=1] towrite, str filename):
    # see:
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html#numpy.loadtxt
    cdef unsigned int numberOfNodes, numberOfComponents
    cdef str myheader
    
    numberOfNodes      = towrite.shape[0]
    numberOfComponents = 1
    myheader = str(numberOfNodes) + ' ' + str(numberOfComponents)
    numpy.savetxt(filename, towrite, fmt='%.18e', delimiter=' ', newline='\n', header=myheader, footer='', comments='')
    
    return 1

# write numpy arrays to file (convenience method for mesh quality measure)
def writeScalarInts(ndarray[numpy.int_t, ndim=1] towrite, str filename):
    # see:
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.savetxt.html
    # http://docs.scipy.org/doc/numpy/reference/generated/numpy.loadtxt.html#numpy.loadtxt
    cdef unsigned int numberOfNodes, numberOfComponents
    cdef str myheader
    
    numberOfNodes      = towrite.shape[0]
    numberOfComponents = 1
    myheader = str(numberOfNodes) + ' ' + str(numberOfComponents)
    numpy.savetxt(filename, towrite, fmt='%i', delimiter=' ', newline='\n', header=myheader, footer='', comments='')
    
    return 1



def readFileList(str filename):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.int_t, ndim=1] listNumber
    cdef unsigned int numberOfTimeSteps
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef double s0
    
    # for linux/windows portability use: cfile = fopen(fname, "r")
    # otherwise, the following reads binary as well (needs modifications though):
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    # first line
    read = getline(&line, &l, cfile)
    s0 = splitLine(line)
    numberOfTimeSteps = int(s0)
    listNumber = numpy.empty(numberOfTimeSteps).astype(int)
    # read all subsequent lines
    for i in range(numberOfTimeSteps):
        read = getline(&line, &l, cfile)
        if read == -1: break
        s0 = splitLine(line)
        listNumber[i] = int(s0)
    fclose(cfile)
    
    return listNumber

def createFileList(unsigned int minn, unsigned int maxx, unsigned int increment):
    cdef ndarray[numpy.int_t, ndim=1] listNumber
    cdef unsigned int currentIndex, current
    
    if increment == 0: increment = 1
    current = minn
    currentIndex = 0
    listNumber = numpy.empty(numpy.floor(1+(maxx-minn) / increment)).astype(int)
    while (current <= maxx):
        listNumber[currentIndex] = current
        current = current + increment
        currentIndex = currentIndex + 1
    
    return listNumber

# reads coordinates
def readVectors(str filename):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.double_t, ndim=2] coordinates
    cdef unsigned int numberOfComponents, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef double s0, s1, s2
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1, s2 = splitLine3(line)
    numberOfNodes = int(s0)
    numberOfComponents = int(s1)
    # defaults to three dimensional coordinate data (vtk depends on 3D)
    coordinates = numpy.empty((numberOfNodes, 3))
    # read all subsequent lines
    for i in range(numberOfNodes):
        read = getline(&line, &l, cfile)
        if read == -1: break
        s0, s1, s2 = splitLine3(line)
#        data = string.split(line) # is slower but safer..
        coordinates[i, 0] = float(s0) #float(data[0])
        coordinates[i, 1] = float(s1) #float(data[1])
        coordinates[i, 2] = float(s2)
    fclose(cfile)
    
    return coordinates, numberOfComponents

# reads coordinates
def readCoordDisp(str filename, str filename2):
    filename_byte_string = filename.encode("UTF-8")
    filename_byte_string2 = filename2.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef char* fname2 = filename_byte_string2
    cdef FILE* cfile
    cdef FILE* cfile2
    cdef ndarray[numpy.double_t, ndim=2] coordinates
    cdef ndarray[numpy.double_t, ndim=2] displacement
    cdef unsigned int numberOfComponents, numberOfNodes, i
    cdef char * line = NULL
    cdef char * line2 = NULL
    cdef size_t l = 0
    cdef size_t l2 = 0
    cdef ssize_t read
    cdef ssize_t read2
    cdef double s0, s1, s2, d0, d1, d2
    
    cfile = fopen(fname, "rb")
    cfile2 = fopen(fname2, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    if cfile2 == NULL:
        print "No such file or directory: '%s'" % filename2
    
    # first line
    read = getline(&line, &l, cfile)
    read2 = getline(&line2, &l2, cfile2)
    s0, s1, s2 = splitLine3(line)
    d0, d1, d2 = splitLine3(line2)
    numberOfNodes = int(s0)
    numberOfComponents = int(s1)
    # defaults to three dimensional coordinate data (vtk depends on 3D)
    coordinates = numpy.empty((numberOfNodes, 3))
    displacement = numpy.empty((numberOfNodes, 3))
    # read all subsequent lines
    for i in range(numberOfNodes):
        read = getline(&line, &l, cfile)
        read2 = getline(&line2, &l2, cfile2)
        if read == -1: break
        s0, s1, s2 = splitLine3(line)
        d0, d1, d2 = splitLine3(line2)
#        data = string.split(line) # is slower but safer..
        coordinates[i, 0] = float(s0+d0) #float(data[0])
        coordinates[i, 1] = float(s1+d1) #float(data[1])
        coordinates[i, 2] = float(s2+d2)
        displacement[i, 0] = float(d0) #float(data[0])
        displacement[i, 1] = float(d1) #float(data[1])
        displacement[i, 2] = float(d2)
    fclose(cfile)
    fclose(cfile2)
    
    return coordinates, displacement, numberOfComponents

# reads scalars
def readScalars(str filename):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.double_t, ndim=1] scalars
    cdef unsigned int numberOfComponents, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef double s0, s1, s2
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1, s2 = splitLine3(line)
    numberOfNodes = int(s0)
    numberOfComponents = int(s1)
    scalars = numpy.empty(numberOfNodes)
    # read all subsequent lines
    for i in range(numberOfNodes):
        read = getline(&line, &l, cfile)
        if read == -1: break
        scalars[i] = float(splitLine(line)) #float(data[0])
    fclose(cfile)
    
    return scalars

# reads scalars
def readScalarInts(str filename):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.int_t, ndim=1] scalars
    cdef unsigned int numberOfComponents, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef double s0, s1, s2
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1, s2 = splitLine3(line)
    numberOfNodes = int(s0)
    numberOfComponents = int(s1)
    scalars = numpy.empty(numberOfNodes, dtype=int)
    # read all subsequent lines
    for i in range(numberOfNodes):
        read = getline(&line, &l, cfile)
        if read == -1: break
        scalars[i] = int(splitLine(line)) #float(data[0])
    fclose(cfile)
    
    return scalars

# reads scalars
def readScalarInts27(str filename):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.int_t, ndim=2] scalars
    cdef unsigned int numberOfComponents, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef double s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1, s2 = splitLine3(line)
    numberOfNodes = int(s0)
    numberOfComponents = 27
    scalars = numpy.empty((numberOfNodes, numberOfComponents), dtype=int)
    # read all subsequent lines
    for i in range(numberOfNodes):
        read = getline(&line, &l, cfile)
        if read == -1: break
        s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26 = splitLine27(line)
        scalars[i, 0] = int(s0)
        scalars[i, 1] = int(s1)
        scalars[i, 2] = int(s2)
        scalars[i, 3] = int(s3)
        scalars[i, 4] = int(s4)
        scalars[i, 5] = int(s5)
        scalars[i, 6] = int(s6)
        scalars[i, 7] = int(s7)
        scalars[i, 8] = int(s8)
        scalars[i, 9] = int(s9)
        scalars[i, 10] = int(s10)
        scalars[i, 11] = int(s11)
        scalars[i, 12] = int(s12)
        scalars[i, 13] = int(s13)
        scalars[i, 14] = int(s14)
        scalars[i, 15] = int(s15)
        scalars[i, 16] = int(s16)
        scalars[i, 17] = int(s17)
        scalars[i, 18] = int(s18)
        scalars[i, 19] = int(s19)
        scalars[i, 20] = int(s20)
        scalars[i, 21] = int(s21)
        scalars[i, 22] = int(s22)
        scalars[i, 23] = int(s23)
        scalars[i, 24] = int(s24)
        scalars[i, 25] = int(s25)
        scalars[i, 26] = int(s26)
    fclose(cfile)
    
    return scalars

# reads scalars
def readScalarInts10(str filename):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.int_t, ndim=2] scalars
    cdef unsigned int numberOfComponents, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef double s0, s1, s2, s3, s4, s5, s6, s7, s8, s9
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1, s2 = splitLine3(line)
    numberOfNodes = int(s0)
    numberOfComponents = 10
    scalars = numpy.empty((numberOfNodes, numberOfComponents), dtype=int)
    # read all subsequent lines
    for i in range(numberOfNodes):
        read = getline(&line, &l, cfile)
        if read == -1: break
        s0, s1, s2, s3, s4, s5, s6, s7, s8, s9 = splitLine10(line)
        scalars[i, 0] = int(s0)
        scalars[i, 1] = int(s1)
        scalars[i, 2] = int(s2)
        scalars[i, 3] = int(s3)
        scalars[i, 4] = int(s4)
        scalars[i, 5] = int(s5)
        scalars[i, 6] = int(s6)
        scalars[i, 7] = int(s7)
        scalars[i, 8] = int(s8)
        scalars[i, 9] = int(s9)
    fclose(cfile)
    
    return scalars

# reads scalars
def readScalarInts8(str filename):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.int_t, ndim=2] scalars
    cdef unsigned int numberOfComponents, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef double s0, s1, s2, s3, s4, s5, s6, s7
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1, s2 = splitLine3(line)
    numberOfNodes = int(s0)
    numberOfComponents = 8
    scalars = numpy.empty((numberOfNodes, numberOfComponents), dtype=int)
    # read all subsequent lines
    for i in range(numberOfNodes):
        read = getline(&line, &l, cfile)
        if read == -1: break
        s0, s1, s2, s3, s4, s5, s6, s7 = splitLine8(line)
        scalars[i, 0] = int(s0)
        scalars[i, 1] = int(s1)
        scalars[i, 2] = int(s2)
        scalars[i, 3] = int(s3)
        scalars[i, 4] = int(s4)
        scalars[i, 5] = int(s5)
        scalars[i, 6] = int(s6)
        scalars[i, 7] = int(s7)
    fclose(cfile)
    
    return scalars

# reads scalars
def readScalarInts4(str filename):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.int_t, ndim=2] scalars
    cdef unsigned int numberOfComponents, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef double s0, s1, s2, s3
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1, s2 = splitLine3(line)
    numberOfNodes = int(s0)
    numberOfComponents = 4
    scalars = numpy.empty((numberOfNodes, numberOfComponents), dtype=int)
    # read all subsequent lines
    for i in range(numberOfNodes):
        read = getline(&line, &l, cfile)
        if read == -1: break
        s0, s1, s2, s3 = splitLine4(line)
        scalars[i, 0] = int(s0)
        scalars[i, 1] = int(s1)
        scalars[i, 2] = int(s2)
        scalars[i, 3] = int(s3)
    fclose(cfile)
    
    return scalars

# if the FSI method includes a change-of-variables (tranforming pressure variables such that fluid is free of gravitational effects)
# then we have to use a reverse transformation to recover the correct pressures including hydrostatic pressure contributions
def changeOfVariables(ndarray[numpy.double_t, ndim=2] coord, ndarray[numpy.double_t, ndim=1] pres, numpy.double_t density, numpy.double_t gx, numpy.double_t gy, numpy.double_t gz, numpy.double_t PO):
    cdef unsigned int i, numberOfNodes
    
    numberOfNodes = coord.shape[0]
    for i in range(numberOfNodes):
        pres[i] = pres[i] + density * (gx * coord[i, 0] + gy * coord[i, 1] + gz * coord[i, 2]) + PO
    
    return pres

def readTriQuadAsLin(str filename, int numDim=2):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.int_t, ndim=2] elements
    cdef unsigned int numberOfElements, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef int s0, s1, s2, s3, s4, s5, s6, s7, s8, s9
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1, s2, s3, s4, s5, s6, s7, s8, s9 = splitLine10(line)
    numberOfElements = int(s0)
    numberOfNodes = int(s1)
    # duplicate code here rather than if/else inside for loop (TODO: more clever way?)
    if numDim == 2:
        elements = numpy.empty((numberOfElements, 6)).astype(int)
        # read all subsequent lines
        for i in range(numberOfElements):
            read = getline(&line, &l, cfile)
            if read == -1: break
            s0, s1, s2, s3, s4, s5 = splitLine6(line)
            elements[i, 0] = int(s0-1)
            elements[i, 1] = int(s1-1)
            elements[i, 2] = int(s2-1)
            elements[i, 3] = int(s3-1)
            elements[i, 4] = int(s4-1)
            elements[i, 5] = int(s5-1)
    else:
        elements = numpy.empty((numberOfElements, 10)).astype(int)
        # read all subsequent lines
        for i in range(numberOfElements):
            read = getline(&line, &l, cfile)
            if read == -1: break
            s0, s1, s2, s3, s4, s5, s6, s7, s8, s9 = splitLine10(line)
            # vtk and cheart node numbers: one has to swap vtk nodes 5 and 6
            elements[i, 0] = int(s0-1)
            elements[i, 1] = int(s1-1)
            elements[i, 2] = int(s2-1)
            elements[i, 3] = int(s3-1)
            elements[i, 4] = int(s4-1)
            elements[i, 5] = int(s6-1)
            elements[i, 6] = int(s5-1)
            elements[i, 7] = int(s7-1)
            elements[i, 8] = int(s8-1)
            elements[i, 9] = int(s9-1)
    fclose(cfile)
    
    return elements

def readTriTetLin(str filename, int numDim=2):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.int_t, ndim=2] elements
    cdef unsigned int numberOfElements, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef int s0, s1, s2, s3
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1, s2, s3 = splitLine4(line)
    numberOfElements = int(s0)
    numberOfNodes = int(s1)
    # duplicate code here rather than if/else inside for loop (TODO: more clever way?)
    if numDim == 2:
        print "Linear tris not implemented!"
    else:
        elements = numpy.empty((numberOfElements, 4)).astype(int)
        # read all subsequent lines
        for i in range(numberOfElements):
            read = getline(&line, &l, cfile)
            if read == -1: break
            s0, s1, s2, s3 = splitLine4(line)
            elements[i, 0] = int(s0-1)
            elements[i, 1] = int(s2-1)
            elements[i, 2] = int(s1-1)
            elements[i, 3] = int(s3-1)
    fclose(cfile)
    
    return elements

def readInterfaceElementsQuad(str filename, int numDim=2):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.int_t, ndim=2] elements
    cdef unsigned int numberOfElements, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef int s0, s1, s2, s3, s4, s5
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1, s2, s3, s4, s5 = splitLine6(line)
    numberOfElements = int(s0)
    numberOfNodes = int(s1)
    # duplicate code here rather than if/else inside for loop (TODO: more clever way?)
    if numDim == 2:
        print "not implemented"
    else:
        elements = numpy.empty((numberOfElements, 6)).astype(int)
        # read all subsequent lines
        for i in range(numberOfElements):
            read = getline(&line, &l, cfile)
            if read == -1: break
            s0, s1, s2, s3, s4, s5 = splitLine6(line)
            # vtk and cheart node numbers: one has to swap vtk nodes ? and ?
            elements[i, 0] = int(s0-1)
            elements[i, 1] = int(s1-1)
            elements[i, 2] = int(s2-1)
            elements[i, 3] = int(s3-1)
            elements[i, 4] = int(s5-1)
            elements[i, 5] = int(s4-1)
    fclose(cfile)
    
    return elements

def readInterfaceElementsLin(str filename, int numDim=2):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.int_t, ndim=2] elements
    cdef unsigned int numberOfElements, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef int s0, s1, s2
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1, s2 = splitLine3(line)
    numberOfElements = int(s0)
    numberOfNodes = int(s1)
    # duplicate code here rather than if/else inside for loop (TODO: more clever way?)
    if numDim == 2:
        print "not implemented"
    else:
        elements = numpy.empty((numberOfElements, 3)).astype(int)
        # read all subsequent lines
        for i in range(numberOfElements):
            read = getline(&line, &l, cfile)
            if read == -1: break
            s0, s1, s2 = splitLine3(line)
            # vtk and cheart node numbers: one has to swap vtk nodes ? and ?
            elements[i, 0] = int(s0-1)
            elements[i, 1] = int(s1-1)
            elements[i, 2] = int(s2-1)
    fclose(cfile)
    
    return elements

def readQuadHex(str filename, int numDim=2):
    filename_byte_string = filename.encode("UTF-8")
    cdef char* fname = filename_byte_string
    cdef FILE* cfile
    cdef ndarray[numpy.int_t, ndim=2] elements
    cdef unsigned int numberOfElements, numberOfNodes, i
    cdef char * line = NULL
    cdef size_t l = 0
    cdef ssize_t read
    cdef int s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26, s27
    
    cfile = fopen(fname, "rb")
    if cfile == NULL:
        print "No such file or directory: '%s'" % filename
    
    # first line
    read = getline(&line, &l, cfile)
    s0, s1 = splitLine2(line)
    numberOfElements = int(s0)
    numberOfNodes = int(s1)
    if numDim == 2:
        elements = numpy.empty((numberOfElements, 8)).astype(int)
        # read all subsequent lines
        for i in range(numberOfElements):
            read = getline(&line, &l, cfile)
            if read == -1: break
            s0, s1, s2, s3, s4, s5, s6, s7 = splitLine6(line)
            elements[i, 0] = int(s0-1)
            elements[i, 1] = int(s1-1)
            elements[i, 2] = int(s2-1)
            elements[i, 3] = int(s3-1)
            elements[i, 4] = int(s4-1)
            elements[i, 5] = int(s5-1)
            elements[i, 6] = int(s6-1)
            elements[i, 7] = int(s7-1)
            # TODO not checked TODO
    else:
        elements = numpy.empty((numberOfElements, 27)).astype(int)
        # read all subsequent lines
        for i in range(numberOfElements):
            read = getline(&line, &l, cfile)
            if read == -1: break
            s0, s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14, s15, s16, s17, s18, s19, s20, s21, s22, s23, s24, s25, s26 = splitLine27(line)
            # VTK node numbers          Cheart node numbers
            #top                        top
            # 7--14--6                   6--26--7
            # |      |                   |      |
            #15  25  13                 19--20--21
            # |      |                   |      |
            # 4--12--5                   2--12--3
            #
            # middle
            #19--23--18                 23--24--25
            # |      |                   |      |
            #20  26  21                 16  17  18
            # |      |                   |      |
            #16--22--17                  9--10--11
            #
            #bottom
            # 3--10--2                   4--22--5
            # |      |                   |      |
            #11  24  9                  13  14  15
            # |      |                   |      |
            # 0-- 8--1                   0-- 8--1
            elements[i,  0] =  int(s0-1)
            elements[i,  1] =  int(s1-1)
            elements[i,  2] =  int(s5-1)
            elements[i,  3] =  int(s4-1)
            elements[i,  4] =  int(s2-1)
            elements[i,  5] =  int(s3-1)
            elements[i,  6] =  int(s7-1)
            elements[i,  7] =  int(s6-1)
            elements[i,  8] =  int(s8-1)
            elements[i,  9] = int(s15-1)
            elements[i, 10] = int(s22-1)
            elements[i, 11] = int(s13-1)
            elements[i, 12] = int(s12-1)
            elements[i, 13] = int(s21-1)
            elements[i, 14] = int(s26-1)
            elements[i, 15] = int(s19-1)
            elements[i, 16] =  int(s9-1)
            elements[i, 17] = int(s11-1)
            elements[i, 18] = int(s25-1)
            elements[i, 19] = int(s23-1)
            elements[i, 20] = int(s16-1)
            elements[i, 21] = int(s18-1)
            elements[i, 22] = int(s10-1)
            elements[i, 23] = int(s24-1)
            elements[i, 24] = int(s14-1)
            elements[i, 25] = int(s20-1)
            elements[i, 26] = int(s17-1)
    fclose(cfile)
    
    return elements

    

def findMapping2D(str filename1, str filename2):
    """Find mapping from linear to quadratic mesh"""
    filename1_byte_string = filename1.encode("UTF-8")
    filename2_byte_string = filename2.encode("UTF-8")
    cdef char* fname1 = filename1_byte_string
    cdef char* fname2 = filename2_byte_string
    cdef FILE* cfile1
    cdef FILE* cfile2
    cdef ndarray[numpy.int_t, ndim=1] mapping
    cdef unsigned int numberOfElements, numberOfNodes, i
    cdef char * line1 = NULL
    cdef char * line2 = NULL
    cdef size_t ll1 = 0
    cdef size_t ll2 = 0
    cdef ssize_t read1
    cdef ssize_t read2
    cdef int l0, l1, l2, q0, q1, q2
    
    cfile1 = fopen(fname1, "rb")
    cfile2 = fopen(fname2, "rb")
    if cfile1 == NULL:
        print "No such file or directory: '%s'" % filename1
    if cfile2 == NULL:
        print "No such file or directory: '%s'" % filename2
    
    # first line
    read1 = getline(&line1, &ll1, cfile1)
    read2 = getline(&line2, &ll2, cfile2)
    l0, l1, l2 = splitLine3(line1)
    numberOfElements = int(l0)
    numberOfNodes = int(l1)
    mapping = numpy.empty(numberOfNodes).astype(int)
    # read all subsequent lines
    for i in range(numberOfElements):
        read1 = getline(&line1, &ll1, cfile1)
        read2 = getline(&line2, &ll2, cfile2)
        if read1 == -1: break
        if read2 == -1: break
        l0, l1, l2 = splitLine3(line1)
        q0, q1, q2 = splitLine3(line2)
        mapping[l0-1] = q0-1
        mapping[l1-1] = q1-1
        mapping[l2-1] = q2-1
    fclose(cfile1)
    fclose(cfile2)
    
    return mapping


def findMappingLinQuad(str filename1, str filename2, int numDim=2):
    """Find mapping from linear to quadratic mesh"""
    filename1_byte_string = filename1.encode("UTF-8")
    filename2_byte_string = filename2.encode("UTF-8")
    cdef char* fname1 = filename1_byte_string
    cdef char* fname2 = filename2_byte_string
    cdef FILE* cfile1
    cdef FILE* cfile2
    cdef ndarray[numpy.int_t, ndim=1] mapping
    cdef unsigned int numberOfElements, numberOfNodes, i
    cdef char * line1 = NULL
    cdef char * line2 = NULL
    cdef size_t ll1 = 0
    cdef size_t ll2 = 0
    cdef ssize_t read1
    cdef ssize_t read2
    cdef int l0, l1, l2, l3, q0, q1, q2, q3
    
    cfile1 = fopen(fname1, "rb")
    cfile2 = fopen(fname2, "rb")
    if cfile1 == NULL:
        print "No such file or directory: '%s'" % filename1
    if cfile2 == NULL:
        print "No such file or directory: '%s'" % filename2
    
    # first line
    read1 = getline(&line1, &ll1, cfile1)
    read2 = getline(&line2, &ll2, cfile2)
    l0, l1, l2 = splitLine3(line1)
    numberOfElements = int(l0)
    numberOfNodes = int(l1)
    mapping = numpy.empty(numberOfNodes).astype(int)
    # read all subsequent lines
    for i in range(numberOfElements):
        read1 = getline(&line1, &ll1, cfile1)
        read2 = getline(&line2, &ll2, cfile2)
        if read1 == -1: break
        if read2 == -1: break
        l0, l1, l2, l3 = splitLine4(line1)
        q0, q1, q2, q3 = splitLine4(line2)
        mapping[l0-1] = q0-1
        mapping[l1-1] = q1-1
        mapping[l2-1] = q2-1
        if numDim == 3: mapping[l3-1] = q3-1
    fclose(cfile1)
    fclose(cfile2)
    
    return mapping


def findMappingLinQuad_Hex(str filename1, str filename2):
    """Find mapping from linear to quadratic mesh"""
    filename1_byte_string = filename1.encode("UTF-8")
    filename2_byte_string = filename2.encode("UTF-8")
    cdef char* fname1 = filename1_byte_string
    cdef char* fname2 = filename2_byte_string
    cdef FILE* cfile1
    cdef FILE* cfile2
    cdef ndarray[numpy.int_t, ndim=1] mapping
    cdef unsigned int numberOfElements, numberOfNodes, i
    cdef char * line1 = NULL
    cdef char * line2 = NULL
    cdef size_t ll1 = 0
    cdef size_t ll2 = 0
    cdef ssize_t read1
    cdef ssize_t read2
    cdef int l0, l1, l2, l3, l4, l5, l6, l7, q0, q1, q2, q3, q4, q5, q6, q7
    
    cfile1 = fopen(fname1, "rb")
    cfile2 = fopen(fname2, "rb")
    if cfile1 == NULL:
        print "No such file or directory: '%s'" % filename1
    if cfile2 == NULL:
        print "No such file or directory: '%s'" % filename2
    
    # first line
    read1 = getline(&line1, &ll1, cfile1)
    read2 = getline(&line2, &ll2, cfile2)
    l0, l1, l2, l3, l4, l5, l6, l7 = splitLine8(line1)
    numberOfElements = int(l0)
    numberOfNodes = int(l1)
    mapping = numpy.empty(numberOfNodes).astype(int)
    # read all subsequent lines
    for i in range(numberOfElements):
        read1 = getline(&line1, &ll1, cfile1)
        read2 = getline(&line2, &ll2, cfile2)
        if read1 == -1: break
        if read2 == -1: break
        l0, l1, l2, l3, l4, l5, l6, l7 = splitLine8(line1)
        q0, q1, q2, q3, q4, q5, q6, q7 = splitLine8(line2)
        mapping[l0-1] = q0-1
        mapping[l1-1] = q1-1
        mapping[l2-1] = q2-1
        mapping[l3-1] = q3-1
        mapping[l4-1] = q4-1
        mapping[l5-1] = q5-1
        mapping[l6-1] = q6-1
        mapping[l7-1] = q7-1
    fclose(cfile1)
    fclose(cfile2)
    
    return mapping

def interpolateLinToQuad2D(ndarray[numpy.int_t, ndim=2] elem, ndarray[numpy.double_t, ndim=2] coord, ndarray[numpy.double_t, ndim=1] presLin, ndarray[numpy.int_t, ndim=1] mapping):
    
    cdef unsigned int numberOfQuadraticElements, numberOfNodesPerCell, numberOfNodes, numberOfComponents, numScalarsLin, i
    cdef ndarray[numpy.double_t, ndim=1] presQuad
    cdef double initVal, n0x, n1x, n2x, n0y, n1y, n2y, n0z, n1z, n2z, val0, val1, val2, area, r, s
    cdef ndarray[numpy.int_t, ndim=1] remapping
    
    b = elem.shape
    numberOfQuadraticElements = b[0]
    numberOfNodesPerCell = b[1]
    b = coord.shape
    numberOfNodes = b[0]
    numberOfComponents = b[1]
    numScalarsLin = presLin.shape[0]
    
    
    presQuad = numpy.empty(numberOfNodes)
    remapping = numpy.empty(numScalarsLin).astype(int)
    initVal = -1351353513.55
    
    for i in range(numberOfNodes):
        presQuad[i] = initVal;
    
    for i in range(numScalarsLin):
        presQuad[mapping[i]] = presLin[i]
    
    for i in range(numberOfQuadraticElements):
        n0x = coord[elem[i, 0], 0]
        n0y = coord[elem[i, 0], 1]
        n0z = coord[elem[i, 0], 2]
        n1x = coord[elem[i, 1], 0]
        n1y = coord[elem[i, 1], 1]
        n1z = coord[elem[i, 1], 2]
        n2x = coord[elem[i, 2], 0]
        n2y = coord[elem[i, 2], 1]
        n2z = coord[elem[i, 2], 2]
        val0 = presQuad[elem[i, 0]]
        val1 = presQuad[elem[i, 1]]
        val2 = presQuad[elem[i, 2]]
        for j in range(3, numberOfNodesPerCell):
            njx = coord[elem[i, j], 0]
            njy = coord[elem[i, j], 1]
            njz = coord[elem[i, j], 2]
            # solve for inside/outside triangle
            area = 0.5 * (-n1y*n2x + n0y*(-n1x + n2x) + n0x*(n1y - n2y) + n1x*n2y)
            s = 1.0 / (2.0 * area) * (n0y*n2x - n0x*n2y + (n2y - n0y)*njx + (n0x - n2x)*njy)
            r = 1.0 / (2.0 * area) * (n0x*n1y - n0y*n1x + (n0y - n1y)*njx + (n1x - n0x)*njy)
            # only if point is inside triangle: interpolate
            if s>=0.0 and r>=0.0 and 1.0-s-r>=0.0:
            #    print "POINT IS INSIDE TRIANGLE", currentCellPoints.GetId(j)
#                presQuad[elem[i, j]] = (1.0-r-s) * val0 + r * val1 + s * val2
                presQuad[elem[i, j]] = (1.0-r-s) * val0 + s * val1 + r * val2
            else:
                # if node on boundary has moved outside linear triangle: extrapolate
                if presQuad[elem[i, j]] == initVal:
                    presQuad[elem[i, j]] = (1.0-r-s) * val0 + s * val1 + r * val2
    
    return presQuad

def interpolateLinToQuad(ndarray[numpy.int_t, ndim=2] elem, ndarray[numpy.double_t, ndim=2] coord, ndarray[numpy.double_t, ndim=1] presLin, ndarray[numpy.int_t, ndim=1] mapping, int numDim=2):
    
    cdef unsigned int numberOfQuadraticElements, numberOfNodesPerCell, numberOfNodes, numberOfComponents, numScalarsLin, i
    cdef ndarray[numpy.double_t, ndim=1] presQuad
    cdef double initVal, n0x, n1x, n2x, n3x, n0y, n1y, n2y, n3y, n0z, n1z, n2z, n3z, val0, val1, val2, val3, area, r, s, t, V0, V1, V2, V3, V, N0, N1, N2, N3, njx, njy, njz
    
    numberOfQuadraticElements = elem.shape[0]
    numberOfNodesPerCell = elem.shape[1]
    numberOfNodes = coord.shape[0]
    numberOfComponents = coord.shape[1]
    numScalarsLin = presLin.shape[0]
    
    
    presQuad = numpy.empty(numberOfNodes)
    initVal = -1351353513.55
    
    for i in range(numberOfNodes):
        presQuad[i] = initVal;
    
    for i in range(numScalarsLin):
        presQuad[mapping[i]] = presLin[i]
    
    if numDim == 2:
        for i in range(numberOfQuadraticElements):
            n0x = coord[elem[i, 0], 0]
            n0y = coord[elem[i, 0], 1]
            n0z = coord[elem[i, 0], 2]
            n1x = coord[elem[i, 1], 0]
            n1y = coord[elem[i, 1], 1]
            n1z = coord[elem[i, 1], 2]
            n2x = coord[elem[i, 2], 0]
            n2y = coord[elem[i, 2], 1]
            n2z = coord[elem[i, 2], 2]
            val0 = presQuad[elem[i, 0]]
            val1 = presQuad[elem[i, 1]]
            val2 = presQuad[elem[i, 2]]
            for j in range(3, numberOfNodesPerCell):
                njx = coord[elem[i, j], 0]
                njy = coord[elem[i, j], 1]
                njz = coord[elem[i, j], 2]
                # solve for inside/outside triangle
                area = 0.5 * (-n1y*n2x + n0y*(-n1x + n2x) + n0x*(n1y - n2y) + n1x*n2y)
                s = 1.0 / (2.0 * area) * (n0y*n2x - n0x*n2y + (n2y - n0y)*njx + (n0x - n2x)*njy)
                r = 1.0 / (2.0 * area) * (n0x*n1y - n0y*n1x + (n0y - n1y)*njx + (n1x - n0x)*njy)
                # only if point is inside triangle: interpolate
                if s>=0.0 and r>=0.0 and 1.0-s-r>=0.0:
                #    print "POINT IS INSIDE TRIANGLE", currentCellPoints.GetId(j)
    #                presQuad[elem[i, j]] = (1.0-r-s) * val0 + r * val1 + s * val2
                    presQuad[elem[i, j]] = (1.0-r-s) * val0 + s * val1 + r * val2
                else:
                    # if node on boundary has moved outside linear triangle: extrapolate
                    if presQuad[elem[i, j]] == initVal:
                        presQuad[elem[i, j]] = (1.0-r-s) * val0 + s * val1 + r * val2
    else:
        for i in range(numberOfQuadraticElements):
            # get coordinates of master-tetrahedron
            n0x = coord[elem[i, 0], 0]
            n0y = coord[elem[i, 0], 1]
            n0z = coord[elem[i, 0], 2]
            n1x = coord[elem[i, 1], 0]
            n1y = coord[elem[i, 1], 1]
            n1z = coord[elem[i, 1], 2]
            n2x = coord[elem[i, 2], 0]
            n2y = coord[elem[i, 2], 1]
            n2z = coord[elem[i, 2], 2]
            n3x = coord[elem[i, 3], 0]
            n3y = coord[elem[i, 3], 1]
            n3z = coord[elem[i, 3], 2]
            val0 = presQuad[elem[i, 0]]
            val1 = presQuad[elem[i, 1]]
            val2 = presQuad[elem[i, 2]]
            val3 = presQuad[elem[i, 3]]
            for j in range(4, numberOfNodesPerCell):
                # current node coordinates
                njx = coord[elem[i, j], 0]
                njy = coord[elem[i, j], 1]
                njz = coord[elem[i, j], 2]
                # calculate volumes of sub-tetrahedrons
                V0 = abs((njx - n3x) * ((n1y - n3y) * (n2z - n3z) - (n1z - n3z) * (n2y - n3y))
                       + (njy - n3y) * ((n1z - n3z) * (n2x - n3x) - (n1x - n3x) * (n2z - n3z))
                       + (njz - n3z) * ((n1x - n3x) * (n2y - n3y) - (n1y - n3y) * (n2x - n3x)))
                V1 = abs((njx - n3x) * ((n0y - n3y) * (n2z - n3z) - (n0z - n3z) * (n2y - n3y))
                       + (njy - n3y) * ((n0z - n3z) * (n2x - n3x) - (n0x - n3x) * (n2z - n3z))
                       + (njz - n3z) * ((n0x - n3x) * (n2y - n3y) - (n0y - n3y) * (n2x - n3x)))
                V2 = abs((njx - n3x) * ((n0y - n3y) * (n1z - n3z) - (n0z - n3z) * (n1y - n3y))
                       + (njy - n3y) * ((n0z - n3z) * (n1x - n3x) - (n0x - n3x) * (n1z - n3z))
                       + (njz - n3z) * ((n0x - n3x) * (n1y - n3y) - (n0y - n3y) * (n1x - n3x)))
                V3 = abs((njx - n0x) * ((n2y - n0y) * (n1z - n0z) - (n2z - n0z) * (n1y - n0y))
                       + (njy - n0y) * ((n2z - n0z) * (n1x - n0x) - (n2x - n0x) * (n1z - n0z))
                       + (njz - n0z) * ((n2x - n0x) * (n1y - n0y) - (n2y - n0y) * (n1x - n0x)))
                # volume of master tetrahedron
                V = abs((n0x - n3x) * ((n1y - n3y) * (n2z - n3z) - (n1z - n3z) * (n2y - n3y))
                      + (n0y - n3y) * ((n1z - n3z) * (n2x - n3x) - (n1x - n3x) * (n2z - n3z))
                      + (n0z - n3z) * ((n1x - n3x) * (n2y - n3y) - (n1y - n3y) * (n2x - n3x)))
                # shape functions
                N0 = V0 / V
                N1 = V1 / V
                N2 = V2 / V
                N3 = V3 / V
                # only if point is inside tetrahedron or outside but on boundary: interpolate
                if (V0+V1+V2+V3<=V) or (presQuad[elem[i, j]] == initVal):
                    # interpolate
                    presQuad[elem[i, j]] = N0 * val0 + N1 * val1 + N2 * val2 + N3 * val3
    
    return presQuad

# interpolate scalar field onto quad-hexes
def interpolateLinToQuad_Hex(ndarray[numpy.int_t, ndim=2] elem, ndarray[numpy.double_t, ndim=2] coord, ndarray[numpy.double_t, ndim=1] presLin, ndarray[numpy.int_t, ndim=1] mapping, int numDim=2):
    
    cdef unsigned int numberOfQuadraticElements, numberOfNodesPerCell, numberOfNodes, numberOfComponents, numScalarsLin, i, j, k, l, m, inside, iterX, iterMax
    cdef ndarray[numpy.double_t, ndim=1] presQuad
    cdef ndarray[numpy.double_t, ndim=2] nm # master-hex nodes
    cdef ndarray[numpy.double_t, ndim=2] pyramid, Jkinv, Jk
    cdef ndarray[numpy.double_t, ndim=1] vals, ip, ipk, ip_m_ipk, N, xik
    cdef double initVal, l2norm
    cdef double pv1, pv2, pv3, pv4, pv5, pv6, hexv
    
    numberOfQuadraticElements = elem.shape[0]
    numberOfNodesPerCell = elem.shape[1]
    numberOfNodes = coord.shape[0]
    numberOfComponents = coord.shape[1]
    numScalarsLin = presLin.shape[0]
    
    
    presQuad = numpy.zeros(numberOfNodes).astype(float)
    nm       = numpy.zeros((27, numberOfComponents)).astype(float)
    pyramid  = numpy.zeros((5, numberOfComponents)).astype(float)
    Jk       = numpy.zeros((numberOfComponents, numberOfComponents)).astype(float)
    Jkinv    = numpy.zeros((numberOfComponents, numberOfComponents)).astype(float)
    N        = numpy.zeros((8)).astype(float)
    vals     = numpy.zeros((8)).astype(float)
    ip       = numpy.zeros(numberOfComponents).astype(float)
    ipk      = numpy.zeros(numberOfComponents).astype(float)
    xik      = numpy.zeros(numberOfComponents).astype(float)
    ip_m_ipk = numpy.zeros(numberOfComponents).astype(float)
    initVal  = -1351353513.55
    iterMax  = 200
    
    for i in range(numberOfNodes):
        presQuad[i] = initVal;
    
    for i in range(numScalarsLin):
        presQuad[mapping[i]] = presLin[i]
    
    if numDim == 2:
        return -1
        # TODO not implemented
    else:
        for i in range(numberOfQuadraticElements):
            # get coordinates of master-hexahedron
            # this is the vtkTriQuadraticHexahedron
            for k in range (27):
                for l in range(numberOfComponents):
                    nm[k, l] = coord[elem[i, k], l]
            # VTK node numbers          Cheart node numbers
            #top                        top
            # 7--14--6                   6--26--7
            # |      |                   |      |
            #15  25  13                 19--20--21
            # |      |                   |      |
            # 4--12--5                   2--12--3
            #
            # middle
            #19--23--18                 23--24--25
            # |      |                   |      |
            #20  26  21                 16  17  18
            # |      |                   |      |
            #16--22--17                  9--10--11
            #
            #bottom
            # 3--10--2                   4--22--5
            # |      |                   |      |
            #11  24  9                  13  14  15
            # |      |                   |      |
            # 0-- 8--1                   0-- 8--1
            
            # get values at corners of master-hexahedron
            for k in range(8):
                vals[k] = presQuad[elem[i, k]]
            
            # check if point is inside the hexahedron
            for k in range(8, 27):
                # point to interpolate
                for l in range(numberOfComponents):
                    ip[l] = nm[k, l]
                inside = 1
                # we split the hex into six pyramids and check if the volume is
                # positive, otherwise point is outside
                for m in range(numberOfComponents):
                    pyramid[0, m] = ip[m]
                    pyramid[1, m] = nm[0, m]
                    pyramid[2, m] = nm[1, m]
                    pyramid[3, m] = nm[5, m]
                    pyramid[4, m] = nm[4, m]
                pv1 = computePyramidVolume(pyramid)
                if pv1 >= 0.0:
                    for m in range(numberOfComponents):
                        pyramid[1, m] = nm[1, m]
                        pyramid[2, m] = nm[2, m]
                        pyramid[3, m] = nm[6, m]
                        pyramid[4, m] = nm[5, m]
                    pv2 = computePyramidVolume(pyramid)
                    if pv2 >= 0.0:
                        for m in range(numberOfComponents):
                            pyramid[1, m] = nm[4, m]
                            pyramid[2, m] = nm[5, m]
                            pyramid[3, m] = nm[6, m]
                            pyramid[4, m] = nm[7, m]
                        pv3 = computePyramidVolume(pyramid)
                        if pv3 >= 0.0:
                            for m in range(numberOfComponents):
                                pyramid[1, m] = nm[2, m]
                                pyramid[2, m] = nm[3, m]
                                pyramid[3, m] = nm[7, m]
                                pyramid[4, m] = nm[6, m]
                            pv4 = computePyramidVolume(pyramid)
                            if pv4 >= 0.0:
                                for m in range(numberOfComponents):
                                    pyramid[1, m] = nm[0, m]
                                    pyramid[2, m] = nm[3, m]
                                    pyramid[3, m] = nm[2, m]
                                    pyramid[4, m] = nm[1, m]
                                pv5 = computePyramidVolume(pyramid)
                                if pv5 >= 0.0:
                                    for m in range(numberOfComponents):
                                        pyramid[1, m] = nm[0, m]
                                        pyramid[2, m] = nm[4, m]
                                        pyramid[3, m] = nm[7, m]
                                        pyramid[4, m] = nm[3, m]
                                    pv6 = computePyramidVolume(pyramid)
                                    if pv6 >= 0.0:
                                        # compute total volume for sanity check
                                        hexv = pv1 + pv2 + pv3 + pv4 + pv5 + pv6
                                    else:
                                        inside = 0
#                                        print "outside pv6 = ", pv6
                                else:
                                    inside = 0
#                                    print "outside pv5 = ", pv5
                            else:
                                inside = 0
#                                print "outside pv4 = ", pv4
                        else:
                            inside = 0
#                            print "outside pv3 = ", pv3
                    else:
                        inside = 0
#                        print "outside pv2 = ", pv2
                else:
                    inside = 0
#                    print "outside pv1 = ", pv1
                
                # if node is inside hexahedron: interpolate
                # else: is interpolated in another hex
                if (inside == 1) or (presQuad[elem[i, k]] == initVal):
                    #print "elem ", i, ", node ", k, ", inside ", inside, ", presQuad ", presQuad[elem[i, k]]
                    # initial guess is node of linear subdivision of hex
                    # note: master hex has quadratic ansatz function, thus
                    #       the nodes do not coincide generally
                    if k == 8:
                        xik[0] = 0.0
                        xik[1] = -1.0
                        xik[2] = -1.0
                    elif k == 9:
                        xik[0] = 1.0
                        xik[1] = 0.0
                        xik[2] = -1.0
                    elif k == 10:
                        xik[0] = 0.0
                        xik[1] = 1.0
                        xik[2] = -1.0
                    elif k == 11:
                        xik[0] = -1.0
                        xik[1] = 0.0
                        xik[2] = -1.0
                    elif k == 12:
                        xik[0] = 0.0
                        xik[1] = -1.0
                        xik[2] = 1.0
                    elif k == 13:
                        xik[0] = 1.0
                        xik[1] = 0.0
                        xik[2] = 1.0
                    elif k == 14:
                        xik[0] = 0.0
                        xik[1] = 1.0
                        xik[2] = 1.0
                    elif k == 15:
                        xik[0] = -1.0
                        xik[1] = 0.0
                        xik[2] = 1.0
                    elif k == 16:
                        xik[0] = -1.0
                        xik[1] = -1.0
                        xik[2] = 0.0
                    elif k == 17:
                        xik[0] = 1.0
                        xik[1] = -1.0
                        xik[2] = 0.0
                    elif k == 18:
                        xik[0] = 1.0
                        xik[1] = 1.0
                        xik[2] = 0.0
                    elif k == 19:
                        xik[0] = -1.0
                        xik[1] = 1.0
                        xik[2] = 0.0
                    elif k == 20:
                        xik[0] = -1.0
                        xik[1] = 0.0
                        xik[2] = 0.0
                    elif k == 21:
                        xik[0] = 1.0
                        xik[1] = 0.0
                        xik[2] = 0.0
                    elif k == 22:
                        xik[0] = 0.0
                        xik[1] = -1.0
                        xik[2] = 0.0
                    elif k == 23:
                        xik[0] = 0.0
                        xik[1] = 1.0
                        xik[2] = 0.0
                    elif k == 24:
                        xik[0] = 0.0
                        xik[1] = 0.0
                        xik[2] = -1.0
                    elif k == 25:
                        xik[0] = 0.0
                        xik[1] = 0.0
                        xik[2] = 1.0
                    elif k == 26:
                        xik[0] = 0.0
                        xik[1] = 0.0
                        xik[2] = 0.0
                    # initial guess for global coordinate
                    ipk = getGlobalCoordinates(xik, nm)
                    iterX = 0
                    l2norm = l2diff(ip, ipk)
                    ############################################################
                    # this code crashes for very large deformations,
                    # but we keep it for a later switch between inaccurate
                    # and more accurate interpolation
                    # ###
                    # obtain local coordinates of point for interpolation of
                    # pressure variable (diff: use l2 norm instead of l1 norm)
                    # LiWittekMiller2014.pdf
                    #while (l2norm > 1.0e-6 and iterX < iterMax):
                    #    Jk = computeJacobianHex(xik, nm)
                    #    Jkinv = invert3x3(Jk)
                    #    for m in range(3):
                    #        ip_m_ipk[m] = ip[m] - ipk[m]
                    #    xik = xik + mult33x31(Jkinv, ip_m_ipk)
                    #    ipk = getGlobalCoordinates(xik, nm)
                    #    iterX = iterX + 1
                    #    l2norm = l2diff(ip, ipk)
                    #if iterX >= 100:
                    #    print inside, iterX, l2norm
                    #    print ip, xik, ipk
                    ############################################################
                    # now interpolate scalar value at point in local coordinate system
                    N = hexN(xik)
                    presQuad[elem[i, k]] = 0.0
                    for m in range(8):
                        presQuad[elem[i, k]] += vals[m] * N[m]
    
    return presQuad

def l1(ndarray[numpy.double_t, ndim=1] x, ndarray[numpy.double_t, ndim=1] xk):
    cdef double result
    cdef unsigned int i
    result = 0.0
    for i in range(3):
        result += abs(xk[i] - x[i])
    return result

def l2diff(ndarray[numpy.double_t, ndim=1] x, ndarray[numpy.double_t, ndim=1] xk):
    cdef double result
    cdef unsigned int i
    result = 0.0
    for i in range(3):
        result += pow(xk[i] - x[i], 2)
    return sqrt(result)

def frobenius(ndarray[numpy.double_t, ndim=2] x):
    cdef double result
    cdef unsigned int i, j
    result = 0.0
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            result += pow(x[i, j], 2)
    return sqrt(result)

# computes the l2 norm column-wise and linfty norm of result
def l2linfty(ndarray[numpy.double_t, ndim=2] x):
    cdef unsigned int i, j
    cdef double maxx, result
    maxx = 0.0
    for i in range(x.shape[0]):
        result = 0.0
        for j in range(x.shape[1]):
            result += pow(x[i, j], 2)
        if maxx < sqrt(result):
            maxx = sqrt(result)
    return maxx

# computes the l2 norm column-wise and mean of result
def l2mean(ndarray[numpy.double_t, ndim=2] x):
    cdef unsigned int i, j
    cdef double l2, result
    result = 0.0
    for i in range(x.shape[0]):
        l2 = 0.0
        for j in range(x.shape[1]):
            l2 += pow(x[i, j], 2)
        result += sqrt(l2)
    return result/x.shape[0]

def l2(ndarray[numpy.double_t, ndim=1] x):
    cdef double result
    cdef unsigned int i, j
    result = 0.0
    for i in range(x.shape[0]):
        result += pow(x[i], 2)
    return sqrt(result)

def linfty(ndarray[numpy.double_t, ndim=1] x):
    cdef double result
    cdef unsigned int i, j
    result = 0.0
    for i in range(x.shape[0]):
        if result < abs(x[i]):
            result = abs(x[i])
    return result

# computes l2 norm per node and returns nodal scalar field
def l2pointwise(ndarray[numpy.double_t, ndim=2] x):
    cdef ndarray[numpy.double_t, ndim=1] result
    
    result = numpy.zeros(x.shape[0]).astype(float)
    for i in range(x.shape[0]):
        result[i] = sqrt(x[i, 0] * x[i, 0] + x[i, 1] * x[i, 1] + x[i, 2] * x[i, 2])
    return result

def mult33x31(ndarray[numpy.double_t, ndim=2] A, ndarray[numpy.double_t, ndim=1] b):
    cdef ndarray[numpy.double_t, ndim=1] result
    cdef unsigned int i, j
    result = numpy.zeros(3).astype(float)
    for i in range(3):
        for j in range(3):
            result[i] += A[i, j] * b[j]
    return result

def det3x3(ndarray[numpy.double_t, ndim=2] J):
    cdef double result
    result =  J[0, 0] * J[1, 1] * J[2, 2] \
            + J[0, 1] * J[1, 2] * J[2, 0] \
            + J[0, 2] * J[1, 0] * J[2, 1] \
            - J[2, 0] * J[1, 1] * J[0, 2] \
            - J[2, 1] * J[1, 2] * J[0, 0] \
            - J[2, 2] * J[1, 0] * J[0, 1]
    return result

def invert3x3(ndarray[numpy.double_t, ndim=2] J):
    cdef ndarray[numpy.double_t, ndim=2] result
    cdef double det, one_over_det
    result = numpy.zeros((3, 3)).astype(float)
    det = det3x3(J)
    one_over_det = 1.0 / det
    # http://mo.mathematik.uni-stuttgart.de/inhalt/beispiel/beispiel1113/
    result[0, 0] = one_over_det * (J[1, 1] * J[2, 2] - J[2, 1] * J[1, 2])
    result[0, 1] = one_over_det * (J[0, 2] * J[2, 1] - J[2, 2] * J[0, 1])
    result[0, 2] = one_over_det * (J[0, 1] * J[1, 2] - J[1, 1] * J[0, 2])
    result[1, 0] = one_over_det * (J[1, 2] * J[2, 0] - J[2, 2] * J[1, 0])
    result[1, 1] = one_over_det * (J[0, 0] * J[2, 2] - J[2, 0] * J[0, 2])
    result[1, 2] = one_over_det * (J[0, 2] * J[1, 0] - J[1, 2] * J[0, 0])
    result[2, 0] = one_over_det * (J[1, 0] * J[2, 1] - J[2, 0] * J[1, 1])
    result[2, 1] = one_over_det * (J[0, 1] * J[2, 0] - J[2, 1] * J[0, 0])
    result[2, 2] = one_over_det * (J[0, 0] * J[1, 1] - J[1, 0] * J[0, 1])
    return result

def computeJacobianHex(ndarray[numpy.double_t, ndim=1] xik, ndarray[numpy.double_t, ndim=2] x):
    cdef ndarray[numpy.double_t, ndim=2] result, dNdxi
    cdef unsigned int i
    result = numpy.zeros((3, 3)).astype(float)
    dNdxi  = numpy.empty((3, 8)).astype(float)
    dNdxi[:, :] = hexdNdxi(xik)
    for i in range(8):
        result[0, 0] += x[i, 0] * dNdxi[0, i]
        result[1, 0] += x[i, 0] * dNdxi[1, i]
        result[2, 0] += x[i, 0] * dNdxi[2, i]
        result[0, 1] += x[i, 1] * dNdxi[0, i]
        result[1, 1] += x[i, 1] * dNdxi[1, i]
        result[2, 1] += x[i, 1] * dNdxi[2, i]
        result[0, 2] += x[i, 2] * dNdxi[0, i]
        result[1, 2] += x[i, 2] * dNdxi[1, i]
        result[2, 2] += x[i, 2] * dNdxi[2, i]
    return result

# Computational Methods in Solid Mechanics by A. Curnier, p. 338
def hexN(ndarray[numpy.double_t, ndim=1] xik):
    cdef ndarray[numpy.double_t, ndim=1] result
    result = numpy.empty(8)
    result[0] = 0.125 * (1.0 - xik[0]) * (1.0 - xik[1]) * (1.0 - xik[2])
    result[1] = 0.125 * (1.0 + xik[0]) * (1.0 - xik[1]) * (1.0 - xik[2])
    result[2] = 0.125 * (1.0 + xik[0]) * (1.0 + xik[1]) * (1.0 - xik[2])
    result[3] = 0.125 * (1.0 - xik[0]) * (1.0 + xik[1]) * (1.0 - xik[2])
    result[4] = 0.125 * (1.0 - xik[0]) * (1.0 - xik[1]) * (1.0 + xik[2])
    result[5] = 0.125 * (1.0 + xik[0]) * (1.0 - xik[1]) * (1.0 + xik[2])
    result[6] = 0.125 * (1.0 + xik[0]) * (1.0 + xik[1]) * (1.0 + xik[2])
    result[7] = 0.125 * (1.0 - xik[0]) * (1.0 + xik[1]) * (1.0 + xik[2])
    return result

def hexdNdxi(ndarray[numpy.double_t, ndim=1] xik):
    cdef ndarray[numpy.double_t, ndim=2] result
    result = numpy.empty((3, 8))
    result[0, 0] = -0.125 * (1.0 - xik[1]) * (1.0 - xik[2])
    result[0, 1] =  0.125 * (1.0 - xik[1]) * (1.0 - xik[2])
    result[0, 2] =  0.125 * (1.0 + xik[1]) * (1.0 - xik[2])
    result[0, 3] = -0.125 * (1.0 + xik[1]) * (1.0 - xik[2])
    result[0, 4] = -0.125 * (1.0 - xik[1]) * (1.0 + xik[2])
    result[0, 5] =  0.125 * (1.0 - xik[1]) * (1.0 + xik[2])
    result[0, 6] =  0.125 * (1.0 + xik[1]) * (1.0 + xik[2])
    result[0, 7] = -0.125 * (1.0 + xik[1]) * (1.0 + xik[2])
    result[1, 0] = -0.125 * (1.0 - xik[0]) * (1.0 - xik[2])
    result[1, 1] = -0.125 * (1.0 + xik[0]) * (1.0 - xik[2])
    result[1, 2] =  0.125 * (1.0 + xik[0]) * (1.0 - xik[2])
    result[1, 3] =  0.125 * (1.0 - xik[0]) * (1.0 - xik[2])
    result[1, 4] = -0.125 * (1.0 - xik[0]) * (1.0 + xik[2])
    result[1, 5] = -0.125 * (1.0 + xik[0]) * (1.0 + xik[2])
    result[1, 6] =  0.125 * (1.0 + xik[0]) * (1.0 + xik[2])
    result[1, 7] =  0.125 * (1.0 - xik[0]) * (1.0 + xik[2])
    result[2, 0] = -0.125 * (1.0 - xik[0]) * (1.0 - xik[1])
    result[2, 1] = -0.125 * (1.0 + xik[0]) * (1.0 - xik[1])
    result[2, 2] = -0.125 * (1.0 + xik[0]) * (1.0 + xik[1])
    result[2, 3] = -0.125 * (1.0 - xik[0]) * (1.0 + xik[1])
    result[2, 4] =  0.125 * (1.0 - xik[0]) * (1.0 - xik[1])
    result[2, 5] =  0.125 * (1.0 + xik[0]) * (1.0 - xik[1])
    result[2, 6] =  0.125 * (1.0 + xik[0]) * (1.0 + xik[1])
    result[2, 7] =  0.125 * (1.0 - xik[0]) * (1.0 + xik[1])
    return result

def getGlobalCoordinates(ndarray[numpy.double_t, ndim=1] xik, ndarray[numpy.double_t, ndim=2] x):
    cdef ndarray[numpy.double_t, ndim=1] result, N
    cdef unsigned int i
    result = numpy.zeros(3).astype(float)
    N      = numpy.empty(8)
    N = hexN(xik)
    for i in range(8):
        result[0] += x[i, 0] * N[i]
        result[1] += x[i, 1] * N[i]
        result[2] += x[i, 2] * N[i]
    return result

def computeHexVolumes(ndarray[numpy.double_t, ndim=2] h):
    cdef double v1, v2, v3, oneSixth
    oneSixth = 1.0 / 6.0
    v1 = oneSixth * (dotProduct(differenceVector(h[7, :], h[1, :]), crossProduct(differenceVector(h[5, :], h[1, :]), differenceVector(h[1, :], h[6, :]))) + 0.5 * dotProduct(differenceVector(h[1, :], h[6, :]), crossProduct(differenceVector(h[1, :], h[5, :]), differenceVector(h[1, :], h[6, :]))))
    v2 = oneSixth * (dotProduct(differenceVector(h[7, :], h[0, :]), crossProduct(differenceVector(h[4, :], h[1, :]), differenceVector(h[0, :], h[5, :]))) + 0.5 * dotProduct(differenceVector(h[0, :], h[5, :]), crossProduct(differenceVector(h[0, :], h[4, :]), differenceVector(h[0, :], h[1, :]))))
    v3 = oneSixth * (dotProduct(differenceVector(h[7, :], h[0, :]), crossProduct(differenceVector(h[4, :], h[1, :]), differenceVector(h[0, :], h[5, :]))) + 0.5 * dotProduct(differenceVector(h[0, :], h[2, :]), crossProduct(differenceVector(h[0, :], h[1, :]), differenceVector(h[0, :], h[3, :]))))
    return v1, v2, v3

def computeTetVolumes(ndarray[numpy.double_t, ndim=2] tet):
    cdef double result
    result = dotProduct(differenceVector(tet[:, 0], tet[:, 3]), \
        crossProduct(differenceVector(tet[:, 1], tet[:, 3]), \
        differenceVector(tet[:, 2], tet[:, 3]))) / 6.0
    return result

# tip - 0; from bottom counter-clockwise 1-2-3-4 for positive volume
# DaviesSalmond1984.pdf
# http://arc.aiaa.org/doi/pdf/10.2514/3.9013
def computePyramidVolume(ndarray[numpy.double_t, ndim=2] p):
    cdef double result
    result = 1.0 / 6.0 * (dotProduct(differenceVector(p[0, :], p[1, :]), crossProduct(differenceVector(p[4, :], p[2, :]), differenceVector(p[1, :], p[3, :]))) + 0.5 * dotProduct(differenceVector(p[1, :], p[3, :]), crossProduct(differenceVector(p[1, :], p[4, :]), differenceVector(p[1, :], p[2, :]))))
    return result

def differenceVector(ndarray[numpy.double_t, ndim=1] v1, ndarray[numpy.double_t, ndim=1] v2):
    cdef ndarray[numpy.double_t, ndim=1] result
    result = numpy.empty(3)
    result[0] = v1[0] - v2[0]
    result[1] = v1[1] - v2[1]
    result[2] = v1[2] - v2[2]
    return result

def edgeCenter(ndarray[numpy.double_t, ndim=1] n1, ndarray[numpy.double_t, ndim=1] n2):
    cdef ndarray[numpy.double_t, ndim=1] result
    result = numpy.empty(3)
    result[0] = n1[0] + 0.5 * (n2[0] - n1[0])
    result[1] = n1[1] + 0.5 * (n2[1] - n1[1])
    result[2] = n1[2] + 0.5 * (n2[2] - n1[2])
    return result

def dotProduct(ndarray[numpy.double_t, ndim=1] v1, ndarray[numpy.double_t, ndim=1] v2):
    cdef double result
    result = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
    return result

def crossProduct(ndarray[numpy.double_t, ndim=1] v1, ndarray[numpy.double_t, ndim=1] v2):
    cdef ndarray[numpy.double_t, ndim=1] result
    result = numpy.empty(3)
    result[0] = v1[1] * v2[2] - v1[2] * v2[1]
    result[1] = v1[2] * v2[0] - v1[0] * v2[2]
    result[2] = v1[0] * v2[1] - v1[1] * v2[0]
    return result

def createTopology3D(ndarray[numpy.int_t, ndim=2] elements, int ct):
    cdef unsigned int numRows, numCols, v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, i, k
    cdef ndarray[numpy.int_t, ndim=1] elementsLin
    cdef ndarray[numpy.int_t, ndim=1] cellslocations
    cdef ndarray[numpy.int_t, ndim=1] cellstypes
    
    numRows = elements.shape[0]
    numCols = elements.shape[1]
    elementsLin = numpy.empty(numRows*8*5).astype(int)
    cellslocations = numpy.empty(numRows*8).astype(int)
    cellstypes = numpy.empty(numRows*8).astype(int)
    
    for k in range(numRows):
        i = k * 8
        v0 = elements[k, 0]
        v1 = elements[k, 1]
        v2 = elements[k, 2]
        v3 = elements[k, 3]
        v4 = elements[k, 4]
        v5 = elements[k, 5]
        v6 = elements[k, 6]
        v7 = elements[k, 7]
        v8 = elements[k, 8]
        v9 = elements[k, 9]
        
        cellslocations[i]   = 5*i
        cellslocations[i+1] = 5*(1+i)
        cellslocations[i+2] = 5*(2+i)
        cellslocations[i+3] = 5*(3+i)
        cellslocations[i+4] = 5*(4+i)
        cellslocations[i+5] = 5*(5+i)
        cellslocations[i+6] = 5*(6+i)
        cellslocations[i+7] = 5*(7+i)
        
        cellstypes[i]   = ct
        cellstypes[i+1] = ct
        cellstypes[i+2] = ct
        cellstypes[i+3] = ct
        cellstypes[i+4] = ct
        cellstypes[i+5] = ct
        cellstypes[i+6] = ct
        cellstypes[i+7] = ct
        
        elementsLin[5*i]       = 4
        elementsLin[5*i+1] = v0
        elementsLin[5*i+2] = v4
        elementsLin[5*i+3] = v6
        elementsLin[5*i+4] = v7
        
        elementsLin[5*(1+i)]   = 4
        elementsLin[5*(1+i)+1] = v4
        elementsLin[5*(1+i)+2] = v1
        elementsLin[5*(1+i)+3] = v5
        elementsLin[5*(1+i)+4] = v8
        
        elementsLin[5*(2+i)]   = 4
        elementsLin[5*(2+i)+1] = v6
        elementsLin[5*(2+i)+2] = v5
        elementsLin[5*(2+i)+3] = v2
        elementsLin[5*(2+i)+4] = v9
        
        elementsLin[5*(3+i)]   = 4
        elementsLin[5*(3+i)+1] = v7
        elementsLin[5*(3+i)+2] = v8
        elementsLin[5*(3+i)+3] = v9
        elementsLin[5*(3+i)+4] = v3
        
        elementsLin[5*(4+i)]   = 4
        elementsLin[5*(4+i)+1] = v6
        elementsLin[5*(4+i)+2] = v9
        elementsLin[5*(4+i)+3] = v7
        elementsLin[5*(4+i)+4] = v5
        
        elementsLin[5*(5+i)]   = 4
        elementsLin[5*(5+i)+1] = v7
        elementsLin[5*(5+i)+2] = v5
        elementsLin[5*(5+i)+3] = v9
        elementsLin[5*(5+i)+4] = v8
        
        elementsLin[5*(6+i)]   = 4
        elementsLin[5*(6+i)+1] = v6
        elementsLin[5*(6+i)+2] = v4
        elementsLin[5*(6+i)+3] = v5
        elementsLin[5*(6+i)+4] = v7
        
        elementsLin[5*(7+i)]  = 4
        elementsLin[5*(7+i)+1] = v4
        elementsLin[5*(7+i)+2] = v5
        elementsLin[5*(7+i)+3] = v7
        elementsLin[5*(7+i)+4] = v8
    
    return elementsLin, cellstypes, cellslocations

def createTopology3Dcells(ndarray[numpy.int_t, ndim=2] elements, int ct):
    cdef unsigned int numRows, numCols, i
    cdef ndarray[numpy.int_t, ndim=1] elementsLin
    cdef ndarray[numpy.int_t, ndim=1] cellslocations
    cdef ndarray[numpy.int_t, ndim=1] cellstypes
    
    numRows = elements.shape[0]
    numCols = elements.shape[1]
    elementsLin = numpy.empty(numRows*5).astype(int)
    cellslocations = numpy.empty(numRows).astype(int)
    cellstypes = numpy.empty(numRows).astype(int)
    
    for i in range(numRows):
        cellslocations[i]   = 5*i
        
        cellstypes[i]   = ct
        
        elementsLin[5*i]   = 4
        elementsLin[5*i+1] = elements[i, 0]
        elementsLin[5*i+2] = elements[i, 1]
        elementsLin[5*i+3] = elements[i, 2]
        elementsLin[5*i+4] = elements[i, 3]
    
    return elementsLin, cellstypes, cellslocations

def createTopology2D(ndarray[numpy.int_t, ndim=2] elements, int ct):
    cdef unsigned int numRows, numCols, v0, v1, v2, v3, v4, v5, i, k
    cdef ndarray[numpy.int_t, ndim=1] elementsLin
    cdef ndarray[numpy.int_t, ndim=1] cellslocations
    cdef ndarray[numpy.int_t, ndim=1] cellstypes
    
    numRows = elements.shape[0]
    numCols = elements.shape[1]
    elementsLin = numpy.empty(numRows*4*4).astype(int)
    cellslocations = numpy.empty(numRows*4).astype(int)
    cellstypes = numpy.empty(numRows*4).astype(int)
    
    for k in range(numRows):
        i = k * 4
        v0 = elements[k, 0]
        v1 = elements[k, 1]
        v2 = elements[k, 2]
        v3 = elements[k, 3]
        v4 = elements[k, 4]
        v5 = elements[k, 5]
        
        cellslocations[i]   = 4*i
        cellslocations[i+1] = 4*(1+i)
        cellslocations[i+2] = 4*(2+i)
        cellslocations[i+3] = 4*(3+i)
        
        cellstypes[i]   = ct
        cellstypes[i+1] = ct
        cellstypes[i+2] = ct
        cellstypes[i+3] = ct
        
        elementsLin[4*i]   = 3
        elementsLin[4*i+1] = v0
        elementsLin[4*i+2] = v3
        elementsLin[4*i+3] = v4
        
        elementsLin[4*(1+i)]   = 3
        elementsLin[4*(1+i)+1] = v3
        elementsLin[4*(1+i)+2] = v1
        elementsLin[4*(1+i)+3] = v5
        
        elementsLin[4*(2+i)]   = 3
        elementsLin[4*(2+i)+1] = v3
        elementsLin[4*(2+i)+2] = v5
        elementsLin[4*(2+i)+3] = v4
        
        elementsLin[4*(3+i)]   = 3
        elementsLin[4*(3+i)+1] = v4
        elementsLin[4*(3+i)+2] = v5
        elementsLin[4*(3+i)+3] = v2
    
    return elementsLin, cellstypes, cellslocations

def createTopologyInterface3Dquad(ndarray[numpy.int_t, ndim=2] elements, int ct):
    cdef unsigned int numRows, numCols, i, k
    cdef ndarray[numpy.int_t, ndim=1] elementsLinearIndex
    cdef ndarray[numpy.int_t, ndim=1] cellslocations
    cdef ndarray[numpy.int_t, ndim=1] cellstypes
    
    # number of elements
    numRows = elements.shape[0]
    # number of nodes per element
    numCols = elements.shape[1]
    
    # quadratic triangles
    # allocate memory
    elementsLinearIndex = numpy.empty(numRows*7).astype(int)
    cellslocations = numpy.empty(numRows).astype(int)
    cellstypes = numpy.empty(numRows).astype(int)
    
    # for all elements
    for i in range(numRows):
        # set cell locations in linearly indexed array
        k = (numCols + 1) * i
        cellslocations[i]   = k
        # set cell type
        cellstypes[i]   = ct
        # set elements
        elementsLinearIndex[k]    = numCols
        elementsLinearIndex[k+1]  = elements[i, 0]
        elementsLinearIndex[k+2]  = elements[i, 1]
        elementsLinearIndex[k+3]  = elements[i, 2]
        elementsLinearIndex[k+4]  = elements[i, 3]
        elementsLinearIndex[k+5]  = elements[i, 4]
        elementsLinearIndex[k+6]  = elements[i, 5]
        
    return elementsLinearIndex, cellstypes, cellslocations

def createTopologyInterface3Dlin(ndarray[numpy.int_t, ndim=2] elements, int ct):
    cdef unsigned int numRows, numCols, i, k
    cdef ndarray[numpy.int_t, ndim=1] elementsLinearIndex
    cdef ndarray[numpy.int_t, ndim=1] cellslocations
    cdef ndarray[numpy.int_t, ndim=1] cellstypes
    
    # number of elements
    numRows = elements.shape[0]
    # number of nodes per element
    numCols = elements.shape[1]
    
    # quadratic triangles
    # allocate memory
    elementsLinearIndex = numpy.empty(numRows*4).astype(int)
    cellslocations = numpy.empty(numRows).astype(int)
    cellstypes = numpy.empty(numRows).astype(int)
    
    # for all elements
    for i in range(numRows):
        # set cell locations in linearly indexed array
        k = (numCols + 1) * i
        cellslocations[i]   = k
        # set cell type
        cellstypes[i]   = ct
        # set elements
        elementsLinearIndex[k]    = numCols
        elementsLinearIndex[k+1]  = elements[i, 0]
        elementsLinearIndex[k+2]  = elements[i, 1]
        elementsLinearIndex[k+3]  = elements[i, 2]
        
    return elementsLinearIndex, cellstypes, cellslocations

def createTopology3Dquad(ndarray[numpy.int_t, ndim=2] elements, int ct):
    cdef unsigned int numRows, numCols, i, k
    cdef ndarray[numpy.int_t, ndim=1] elementsLinearIndex
    cdef ndarray[numpy.int_t, ndim=1] cellslocations
    cdef ndarray[numpy.int_t, ndim=1] cellstypes
    
    # number of elements
    numRows = elements.shape[0]
    # number of nodes per element
    numCols = elements.shape[1]
    
    # quadratic tetrahedron
    if ct == 24:
        # allocate memory
        elementsLinearIndex = numpy.empty(numRows*11).astype(int)
        cellslocations = numpy.empty(numRows).astype(int)
        cellstypes = numpy.empty(numRows).astype(int)
        
        # for all elements
        for i in range(numRows):
            # set cell locations in linearly indexed array
            k = (numCols + 1) * i
            cellslocations[i]   = k
            # set cell type
            cellstypes[i]   = ct
            # set elements
            elementsLinearIndex[k]    = numCols
            elementsLinearIndex[k+1]  = elements[i, 0]
            elementsLinearIndex[k+2]  = elements[i, 1]
            elementsLinearIndex[k+3]  = elements[i, 2]
            elementsLinearIndex[k+4]  = elements[i, 3]
            elementsLinearIndex[k+5]  = elements[i, 4]
            elementsLinearIndex[k+6]  = elements[i, 5]
            elementsLinearIndex[k+7]  = elements[i, 6]
            elementsLinearIndex[k+8]  = elements[i, 7]
            elementsLinearIndex[k+9]  = elements[i, 8]
            elementsLinearIndex[k+10] = elements[i, 9]
    # tri-quadratic hexahedron
    elif ct == 29:
        # allocate memory
        elementsLinearIndex = numpy.empty(numRows*28).astype(int)
        cellslocations = numpy.empty(numRows).astype(int)
        cellstypes = numpy.empty(numRows).astype(int)
        
        # for all elements
        for i in range(numRows):
            # set cell locations in linearly indexed array
            k = (numCols + 1) * i
            cellslocations[i]   = k
            # set cell type
            cellstypes[i]   = ct
            # set elements
            elementsLinearIndex[k]    = numCols
            elementsLinearIndex[k+1]  = elements[i, 0]
            elementsLinearIndex[k+2]  = elements[i, 1]
            elementsLinearIndex[k+3]  = elements[i, 2]
            elementsLinearIndex[k+4]  = elements[i, 3]
            elementsLinearIndex[k+5]  = elements[i, 4]
            elementsLinearIndex[k+6]  = elements[i, 5]
            elementsLinearIndex[k+7]  = elements[i, 6]
            elementsLinearIndex[k+8]  = elements[i, 7]
            elementsLinearIndex[k+9]  = elements[i, 8]
            elementsLinearIndex[k+10] = elements[i, 9]
            elementsLinearIndex[k+11] = elements[i, 10]
            elementsLinearIndex[k+12] = elements[i, 11]
            elementsLinearIndex[k+13] = elements[i, 12]
            elementsLinearIndex[k+14] = elements[i, 13]
            elementsLinearIndex[k+15] = elements[i, 14]
            elementsLinearIndex[k+16] = elements[i, 15]
            elementsLinearIndex[k+17] = elements[i, 16]
            elementsLinearIndex[k+18] = elements[i, 17]
            elementsLinearIndex[k+19] = elements[i, 18]
            elementsLinearIndex[k+20] = elements[i, 19]
            elementsLinearIndex[k+21] = elements[i, 20]
            elementsLinearIndex[k+22] = elements[i, 21]
            elementsLinearIndex[k+23] = elements[i, 22]
            elementsLinearIndex[k+24] = elements[i, 23]
            elementsLinearIndex[k+25] = elements[i, 24]
            elementsLinearIndex[k+26] = elements[i, 25]
            elementsLinearIndex[k+27] = elements[i, 26]
        
    return elementsLinearIndex, cellstypes, cellslocations

def createTopology2Dquad(ndarray[numpy.int_t, ndim=2] elements, int ct):
    cdef unsigned int numRows, numCols, i, k
    cdef ndarray[numpy.int_t, ndim=1] elementsLinearIndex
    cdef ndarray[numpy.int_t, ndim=1] cellslocations
    cdef ndarray[numpy.int_t, ndim=1] cellstypes
    
    # number of elements
    numRows = elements.shape[0]
    # number of nodes per element
    numCols = elements.shape[1]
    
    # allocate memory
    elementsLinearIndex = numpy.empty(numRows*7).astype(int)
    cellslocations = numpy.empty(numRows).astype(int)
    cellstypes = numpy.empty(numRows).astype(int)
    
    # for all elements
    for i in range(numRows):
        # set cell locations in linearly indexed array
        k = (numCols + 1) * i
        cellslocations[i]   = k
        # set cell type
        cellstypes[i]   = ct
        # set elements
        elementsLinearIndex[k]    = numCols
        elementsLinearIndex[k+1]  = elements[i, 0]
        elementsLinearIndex[k+2]  = elements[i, 1]
        elementsLinearIndex[k+3]  = elements[i, 2]
        elementsLinearIndex[k+4]  = elements[i, 3]
        elementsLinearIndex[k+5]  = elements[i, 5]
        elementsLinearIndex[k+6]  = elements[i, 4]
    
    return elementsLinearIndex, cellstypes, cellslocations


def computeMagnitude(ndarray[numpy.double_t, ndim=2] field):
    cdef ndarray[numpy.double_t, ndim=1] magnitude
    cdef unsigned int numberOfNodes, numberOfComponents
    
    numberOfNodes      = field.shape[0]
    numberOfComponents = field.shape[1]
    magnitude          = numpy.zeros(numberOfNodes).astype(float)
    
    for i in range(numberOfNodes):
        print i
        magnitude[i] = sqrt(field[i, 0] * field[i, 0] + field[i, 1] * field[i, 1] + field[i, 2] * field[i, 2])
    
    return magnitude

# flip tets such that tet volume has consistent sign, which is equivalent to
# consistent node number order
def flipTets(ndarray[numpy.int_t, ndim=2] elem, ndarray[numpy.double_t, ndim=2] coord):
    cdef unsigned int numElems, numNodesPerElement, numNodes, numDim, i, temp
    cdef ndarray[numpy.double_t, ndim=2] tet
    numElems           = elem.shape[0]
    numNodesPerElement = elem.shape[1]
    numNodes           = coord.shape[0]
    numDim             = coord.shape[1]
    tet                = numpy.zeros((numDim, numNodesPerElement)).astype(float)
    
    for i in range(numElems):
        for j in range(numNodesPerElement):
            for k in range(numDim):
                tet[k, j] = coord[elem[i, j], k]
        if computeTetVolumes(tet) < 0:
            temp = elem[i, 1]
            elem[i, 1] = elem[i, 2]
            elem[i, 2] = temp
            #for j in range(numNodesPerElement):
            #    for k in range(numDim):
            #        tet[k, j] = coord[elem[i, j], k]
            #if computeTetVolumes(tet) < 0:
            #    print "flipTets: Didn't work."
    
    return elem

# http://people.sc.fsu.edu/~jburkardt/m_src/tet_mesh_quality/tet_mesh_quality.html
def computeTetQuality(ndarray[numpy.double_t, ndim=2] coord, ndarray[numpy.int_t, ndim=2] elem, int qualityMeasure=0):
    cdef Py_ssize_t i, j, k
    cdef unsigned int numElems, numNodesPerElement, numNodes, numDim
    cdef double circumradius, inradius, l123, l124, l134, l234, divby, gamma, vol
    cdef ndarray[numpy.double_t, ndim=2] tet, a, b
    cdef ndarray[numpy.double_t, ndim=1] v21, v31, v41, v32, v42, n123, n124, n134, n234, pc, quality
    
    numElems           = elem.shape[0]
    numNodesPerElement = elem.shape[1]
    numNodes           = coord.shape[0]
    numDim             = coord.shape[1]
    tet                = numpy.zeros((numDim, numNodesPerElement)).astype(float)
    a                  = numpy.zeros((numDim, numNodesPerElement)).astype(float)
    b                  = numpy.zeros((numNodesPerElement, numNodesPerElement)).astype(float)
    v21                = numpy.zeros(numDim).astype(float)
    v31                = numpy.zeros(numDim).astype(float)
    v41                = numpy.zeros(numDim).astype(float)
    v32                = numpy.zeros(numDim).astype(float)
    v42                = numpy.zeros(numDim).astype(float)
    n123               = numpy.zeros(numDim).astype(float)
    n124               = numpy.zeros(numDim).astype(float)
    n134               = numpy.zeros(numDim).astype(float)
    n234               = numpy.zeros(numDim).astype(float)
    pc                 = numpy.zeros(numDim).astype(float)
    quality            = numpy.zeros(numElems).astype(float)
    
    if qualityMeasure == 0:
        for i in range(numElems):
            for j in range(numNodesPerElement):
                for k in range(numDim):
                    tet[k, j] = coord[elem[i, j], k]
            
            ## TET VOLUME ######################################################
            #if numNodesPerElement == 4:
            #    vol = dotProduct(differenceVector(tet[:, 0], tet[:, 3]), \
            #        crossProduct(differenceVector(tet[:, 1], tet[:, 3]), \
            #        differenceVector(tet[:, 2], tet[:, 3]))) / 6.0
            #    print "elem "+str(i)+": V = "+str(vol)
            
            ## CIRCUMSPHERE ####################################################
            
            # set up linear system
            for j in range(numDim):
                for k in range(numDim):
                    a[k, j] = tet[j, k+1] - tet[j, 0]
                    a[k, j] = tet[j, k+1] - tet[j, 0]
                    a[k, j] = tet[j, k+1] - tet[j, 0]
             
            for j in range(numDim):
                a[j, 3] = a[j, 0] * a[j, 0] + a[j, 1] * a[j, 1] + a[j, 2] * a[j, 2]
            
            # solve linear system and return circumradius
            circumradius = solve(3, 1, a)
            
            ## INSPHERE ########################################################
            for j in range(numDim):
                v21[j] = tet[j, 1] - tet[j, 0]
                v31[j] = tet[j, 2] - tet[j, 0]
                v41[j] = tet[j, 3] - tet[j, 0]
                v32[j] = tet[j, 2] - tet[j, 1]
                v42[j] = tet[j, 3] - tet[j, 1]
            
            n123[0] = v21[1] * v31[2] - v21[2] * v31[1]
            n123[1] = v21[2] * v31[0] - v21[0] * v31[2]
            n123[2] = v21[0] * v31[1] - v21[1] * v31[0]
            
            n124[0] = v41[1] * v21[2] - v41[2] * v21[1]
            n124[1] = v41[2] * v21[0] - v41[0] * v21[2]
            n124[2] = v41[0] * v21[1] - v41[1] * v21[0]
            
            n134[0] = v31[1] * v41[2] - v31[2] * v41[1]
            n134[1] = v31[2] * v41[0] - v31[0] * v41[2]
            n134[2] = v31[0] * v41[1] - v31[1] * v41[0]
            
            n234[0] = v42[1] * v32[2] - v42[2] * v32[1]
            n234[1] = v42[2] * v32[0] - v42[0] * v32[2]
            n234[2] = v42[0] * v32[1] - v42[1] * v32[0]
            
            l123 = 0.0
            l124 = 0.0
            l134 = 0.0
            l234 = 0.0
            
            for j in range(numDim):
                l123 = l123 + n123[j] * n123[j]
                l124 = l124 + n124[j] * n124[j]
                l134 = l134 + n134[j] * n134[j]
                l234 = l234 + n234[j] * n234[j]
            
            l123 = sqrt(l123)
            l124 = sqrt(l124)
            l134 = sqrt(l134)
            l234 = sqrt(l234)
            
            divby = 1.0 / (l234 + l134 + l124 + l123)
            
            for j in range(numDim):
                pc[j] = (l234 * tet[j, 0] + l134 * tet[j, 1] + l124 * tet[j, 2] + l123 * tet[j, 3]) * divby
            
            for k in range(numDim+1):
                b[numDim, k] = 1.0
                for j in range(numDim):
                    b[j, k] = tet[j, k]
            
            inradius = abs(det4x4(b)) * divby
            
            ## QUALITY #########################################################
            quality[i] = 3.0 * inradius / circumradius;
    
    return quality

cdef inline double det4x4(ndarray[numpy.double_t, ndim=2] b):
    cdef double det
    det = b[0, 0] * (b[1, 1] * ( b[2, 2] * b[3, 3] - b[2, 3] * b[3, 2]) \
                    - b[1, 2] * ( b[2, 1] * b[3, 3] - b[2, 3] * b[3, 1]) \
                    + b[1, 3] * ( b[2, 1] * b[3, 2] - b[2, 2] * b[3, 1])) \
          - b[0, 1] * (b[1, 0] * ( b[2, 2] * b[3, 3] - b[2, 3] * b[3, 2]) \
                      - b[1, 2] * ( b[2, 0] * b[3, 3] - b[2, 3] * b[3, 0]) \
                      + b[1, 3] * ( b[2, 0] * b[3, 2] - b[2, 2] * b[3, 0])) \
          + b[0, 2] * (b[1, 0] * ( b[2, 1] * b[3, 3] - b[2, 3] * b[3, 1]) \
                      - b[1, 1] * ( b[2, 0] * b[3, 3] - b[2, 3] * b[3, 0]) \
                      + b[1, 3] * ( b[2, 0] * b[3, 1] - b[2, 1] * b[3, 0])) \
          - b[0, 3] * (b[1, 0] * ( b[2, 1] * b[3, 2] - b[2, 2] * b[3, 1] ) \
                      - b[1, 1] * ( b[2, 0] * b[3, 2] - b[2, 2] * b[3, 0] ) \
                      + b[1, 2] * ( b[2, 0] * b[3, 1] - b[2, 1] * b[3, 0] ) )
    return det

def solve(int numDim, int numRHS, ndarray[DOUBLETYPE_t, ndim=2] a):
    cdef Py_ssize_t i, j, k, ipivot
    cdef double apivot, factor
    cdef ndarray[DOUBLETYPE_t, ndim=1] temp = numpy.zeros([numDim+numRHS], dtype=DOUBLETYPE)
    
    for j in range(numDim):
        # Choose a pivot row IPIVOT.
        ipivot = j
        apivot = a[j, j]
        
        for i in range(j+1, numDim):
            if (abs(apivot) < abs(a[i, j])):
                apivot = a[i, j]
                ipivot = i
        
        if (apivot == 0.0):
            -1.0
        
        # interchange
        for i in range(numDim+numRHS):
            temp[i] = a[ipivot, i]
            a[ipivot, i] = a[j, i]
            a[j, i] = temp[i]
        
        # A(J,J) becomes 1
        a[j, j] = 1.0
        for i in range(numDim+numRHS):
            a[j, i] = a[j, i] / apivot
        
        # A(I,J) becomes 0
        for i in range(numDim):
            if (i != j):
                factor = a[i, j]
                a[i, j] = 0.0
                for k in range(j, numDim+numRHS):
                    a[i, k] = a[i, k] - factor * a[j, k]
    
    # Compute circumradius
    circumradius = 0.5 * sqrt(pow(a[0, numDim], 2) + pow(a[1, numDim], 2) + pow(a[2, numDim],2 ))
    
    return circumradius

# source: http://www.iue.tuwien.ac.at/phd/hollauer/node29.html equation (5.38)
# NOTE: not checked
def calculateVorticity3D(ndarray[numpy.double_t, ndim=2] tempCoord, ndarray[numpy.int_t, ndim=2] tempElemLinF, ndarray[numpy.double_t, ndim=2] tempVel):
    
    cdef unsigned int numberOfNodes, numberOfElements, numberOfComponents, i, node0, node1, node2, node3
    cdef double n0x, n1x, n2x, n3x, n0y, n1y, n2y, n3y, n0z, n1z, n2z, n3z, one_over_det_jacobian
    cdef ndarray[numpy.double_t, ndim=2] vort
    cdef ndarray[numpy.double_t, ndim=2] jacobian
    cdef ndarray[numpy.double_t, ndim=2] inverse_jacobian
    cdef ndarray[numpy.double_t, ndim=2] inverse_jacobian_t
    cdef ndarray[numpy.double_t, ndim=2] velocity_gradient
    
    numberOfNodes      = tempCoord.shape[0]
    numberOfComponents = tempCoord.shape[1]
    numberOfElements   = tempElemLinF.shape[0]
    
    vort               = numpy.zeros((numberOfNodes, numberOfComponents)).astype(float)
    jacobian           = numpy.empty((numberOfComponents, numberOfComponents)).astype(float)
    inverse_jacobian   = numpy.empty((numberOfComponents, numberOfComponents)).astype(float)
    inverse_jacobian_t = numpy.empty((numberOfComponents, numberOfComponents)).astype(float)
    velocity_gradient  = numpy.empty((numberOfComponents, numberOfComponents)).astype(float)
    
    for i in range(numberOfElements):
        node0 = tempElemLinF[i, 0]
        node1 = tempElemLinF[i, 1]
        node2 = tempElemLinF[i, 2]
        node3 = tempElemLinF[i, 3]
        if (abs(vort[node0, 0])+abs(vort[node0, 1])+abs(vort[node0, 2])>0.0): continue
        n0x = tempCoord[node0, 0]
        n1x = tempCoord[node1, 0]
        n2x = tempCoord[node2, 0]
        n3x = tempCoord[node3, 0]
        n0y = tempCoord[node0, 1]
        n1y = tempCoord[node1, 1]
        n2y = tempCoord[node2, 1]
        n3y = tempCoord[node3, 1]
        n0z = tempCoord[node0, 2]
        n1z = tempCoord[node1, 2]
        n2z = tempCoord[node2, 2]
        n3z = tempCoord[node3, 2]
        # jacobian
        jacobian[0, 0] = n1x - n0x
        jacobian[1, 0] = n2x - n0x
        jacobian[2, 0] = n3x - n0x
        jacobian[0, 1] = n1y - n0y
        jacobian[1, 1] = n2y - n0y
        jacobian[2, 1] = n3y - n0y
        jacobian[0, 2] = n1z - n0z
        jacobian[1, 2] = n2z - n0z
        jacobian[2, 2] = n3z - n0z
        # 1 / (determinant jacobian)
        one_over_det_jacobian = 1.0 / ( \
            jacobian[0, 0] * jacobian[1, 1] * jacobian[2, 2] \
            + jacobian[0, 1] * jacobian[1, 2] * jacobian[2, 0] \
            + jacobian[0, 2] * jacobian[1, 0] * jacobian[2, 1] \
            - jacobian[2, 0] * jacobian[1, 1] * jacobian[0, 2] \
            - jacobian[2, 1] * jacobian[1, 2] * jacobian[0, 0] \
            - jacobian[2, 2] * jacobian[1, 0] * jacobian[0, 1])
        # inverse jacobian
        inverse_jacobian[0, 0] = one_over_det_jacobian * (jacobian[1, 1]*jacobian[2, 2] - jacobian[2, 1]*jacobian[1, 2])
        inverse_jacobian[0, 1] = one_over_det_jacobian * (jacobian[0, 2]*jacobian[2, 1] - jacobian[2, 2]*jacobian[0, 1])
        inverse_jacobian[0, 2] = one_over_det_jacobian * (jacobian[0, 1]*jacobian[1, 2] - jacobian[1, 1]*jacobian[0, 2])
        inverse_jacobian[1, 0] = one_over_det_jacobian * (jacobian[1, 2]*jacobian[2, 0] - jacobian[2, 2]*jacobian[1, 0])
        inverse_jacobian[1, 1] = one_over_det_jacobian * (jacobian[0, 0]*jacobian[2, 2] - jacobian[2, 0]*jacobian[0, 2])
        inverse_jacobian[1, 2] = one_over_det_jacobian * (jacobian[0, 2]*jacobian[1, 0] - jacobian[1, 2]*jacobian[0, 0])
        inverse_jacobian[2, 0] = one_over_det_jacobian * (jacobian[1, 0]*jacobian[2, 1] - jacobian[2, 0]*jacobian[1, 1])
        inverse_jacobian[2, 1] = one_over_det_jacobian * (jacobian[0, 1]*jacobian[2, 0] - jacobian[2, 1]*jacobian[0, 0])
        inverse_jacobian[2, 2] = one_over_det_jacobian * (jacobian[0, 0]*jacobian[1, 1] - jacobian[1, 0]*jacobian[0, 1])
        # inverse jacobian transposed
        inverse_jacobian_t[0, 0] = inverse_jacobian[0, 0]
        inverse_jacobian_t[0, 1] = inverse_jacobian[1, 0]
        inverse_jacobian_t[0, 2] = inverse_jacobian[2, 0]
        inverse_jacobian_t[1, 0] = inverse_jacobian[0, 1]
        inverse_jacobian_t[1, 1] = inverse_jacobian[1, 1]
        inverse_jacobian_t[1, 2] = inverse_jacobian[2, 1]
        inverse_jacobian_t[2, 0] = inverse_jacobian[0, 2]
        inverse_jacobian_t[2, 1] = inverse_jacobian[1, 2]
        inverse_jacobian_t[2, 2] = inverse_jacobian[2, 2]
        # velocity gradient - node 0
        # vx,x vy,x vz,x
        # vx,y vy,y vz,y
        # vx,z vy,z vz,z
        velocity_gradient[0, 0] = \
            inverse_jacobian_t[0, 0] * (tempVel[node1, 0] - tempVel[node0, 0]) \
            + inverse_jacobian_t[0, 1] * (tempVel[node2, 0] - tempVel[node0, 0]) \
            + inverse_jacobian_t[0, 2] * (tempVel[node3, 0] - tempVel[node0, 0])
        velocity_gradient[0, 1] = \
            inverse_jacobian_t[1, 0] * (tempVel[node1, 1] - tempVel[node0, 1]) \
            + inverse_jacobian_t[1, 1] * (tempVel[node2, 1] - tempVel[node0, 1]) \
            + inverse_jacobian_t[1, 2] * (tempVel[node3, 1] - tempVel[node0, 1])
        velocity_gradient[0, 2] = \
            inverse_jacobian_t[2, 0] * (tempVel[node1, 2] - tempVel[node0, 2]) \
            + inverse_jacobian_t[2, 1] * (tempVel[node2, 2] - tempVel[node0, 2]) \
            + inverse_jacobian_t[2, 2] * (tempVel[node3, 2] - tempVel[node0, 2])
        velocity_gradient[1, 0] = \
            inverse_jacobian_t[0, 0] * (tempVel[node1, 0] - tempVel[node0, 0]) \
            + inverse_jacobian_t[0, 1] * (tempVel[node2, 0] - tempVel[node0, 0]) \
            + inverse_jacobian_t[0, 2] * (tempVel[node3, 0] - tempVel[node0, 0])
        velocity_gradient[1, 1] = \
            inverse_jacobian_t[1, 0] * (tempVel[node1, 1] - tempVel[node0, 1]) \
            + inverse_jacobian_t[1, 1] * (tempVel[node2, 1] - tempVel[node0, 1]) \
            + inverse_jacobian_t[1, 2] * (tempVel[node3, 1] - tempVel[node0, 1])
        velocity_gradient[1, 2] = \
            inverse_jacobian_t[2, 0] * (tempVel[node1, 2] - tempVel[node0, 2]) \
            + inverse_jacobian_t[2, 1] * (tempVel[node2, 2] - tempVel[node0, 2]) \
            + inverse_jacobian_t[2, 2] * (tempVel[node3, 2] - tempVel[node0, 2])
        velocity_gradient[2, 0] = \
            inverse_jacobian_t[0, 0] * (tempVel[node1, 0] - tempVel[node0, 0]) \
            + inverse_jacobian_t[0, 1] * (tempVel[node2, 0] - tempVel[node0, 0]) \
            + inverse_jacobian_t[0, 2] * (tempVel[node3, 0] - tempVel[node0, 0])
        velocity_gradient[2, 1] = \
            inverse_jacobian_t[1, 0] * (tempVel[node1, 1] - tempVel[node0, 1]) \
            + inverse_jacobian_t[1, 1] * (tempVel[node2, 1] - tempVel[node0, 1]) \
            + inverse_jacobian_t[1, 2] * (tempVel[node3, 1] - tempVel[node0, 1])
        velocity_gradient[2, 2] = \
            inverse_jacobian_t[2, 0] * (tempVel[node1, 2] - tempVel[node0, 2]) \
            + inverse_jacobian_t[2, 1] * (tempVel[node2, 2] - tempVel[node0, 2]) \
            + inverse_jacobian_t[2, 2] * (tempVel[node3, 2] - tempVel[node0, 2])
        # vorticity
        # vz,y - vy,z
        # vx,z - vz,x
        # vy,x - vx,y
        vort[node0, 0] = velocity_gradient[1, 2] - velocity_gradient[2, 1]
        vort[node0, 1] = velocity_gradient[2, 0] - velocity_gradient[0, 2]
        vort[node0, 2] = velocity_gradient[0, 1] - velocity_gradient[1, 0]
    
    return vort

