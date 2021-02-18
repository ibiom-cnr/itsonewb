from setuptools import setup
from Cython.Build import cythonize


setup(
    name='biomas_function',
    ext_modules=cythonize("biomas_function.pyx",force=True,),
    zip_safe=False,
)

# compilazione manuale
# cython ITS1_parser_ITSoneDB_functions.pyx
# gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I/home/bfosso/anaconda2/include/python2.7 -o ITS1_parser_ITSoneDB_functions.so ITS1_parser_ITSoneDB_functions.c