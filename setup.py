from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize("readCheartData.pyx",language="c",compiler_directives={'profile': False}))
