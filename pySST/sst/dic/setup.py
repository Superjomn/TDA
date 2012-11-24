from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext


files = [
    'dic.py',
    'nodedatas.py',
]

for f in files:
    r = f.rfind('.')
    fname = f[:r]
    setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [Extension(fname, [f])] 
    )



