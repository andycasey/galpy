import numpy as nu
import ctypes
import ctypes.util
from numpy.ctypeslib import ndpointer
import os
from galpy import potential, potential_src
#Find and load the library
_lib = None
_libname = ctypes.util.find_library('galpy_integrate_c')
if _libname:
    _lib = ctypes.CDLL(_libname)
if _lib is None:
    import sys
for path in sys.path:
    try:
        _lib = ctypes.CDLL(os.path.join(path,'galpy_integrate_c.so'))
    except OSError:
        _lib = None
    else:
        break
if _lib is None:
    raise IOError('galpy integration module not found')

def integratePlanarOrbit_leapfrog(pot,yo,t,rtol=None,atol=None):
    """
    NAME:
       integratePlanarOrbit_leapfrog
    PURPOSE:
       leapfrog integrate an ode for a planarOrbit
    INPUT:
       pot - Potential or list of such instances
       yo - initial condition [q,p]
       t - set of times at which one wants the result
       rtol, atol
    OUTPUT:
       y : array, shape (len(y0), len(t))
       Array containing the value of y for each desired time in t, \
       with the initial value y0 in the first row.
    HISTORY:
       2011-10-03 - Written - Bovy (IAS)
    """
    #Process atol and rtol
    if rtol is None:
        rtol= 1.49012e-10
    if atol is None:
        atol= 0.  
    #Figure out what's in pot
    if not isinstance(pot,list):
        pot= [pot]
    #Initialize everything
    pot_type= []
    pot_args= []
    npot= len(pot)
    for p in pot:
        if isinstance(p,potential.LogarithmicHaloPotential):
            pot_type.append(0)
            pot_args.extend([p._amp,p._core2])
        elif isinstance(p,potential_src.planarPotential.planarPotentialFromRZPotential) \
                 and isinstance(p._RZPot,potential.LogarithmicHaloPotential):
            pot_type.append(0)
            pot_args.extend([p._RZPot._amp,p._RZPot._core2])
        elif isinstance(p,potential.DehnenBarPotential):
            pot_type.append(1)
            pot_args.extend([p._amp,p._tform,p._tsteady,p._rb,p._af,p._omegab,
                             p._barphi])
    pot_type= nu.array(pot_type,dtype=nu.int32,order='C')
    pot_args= nu.array(pot_args,dtype=nu.float64,order='C')
            
    #Set up result array
    result= nu.empty((len(t),4))

    #Set up the C code
    ndarrayFlags= ('C_CONTIGUOUS','WRITEABLE')
    integrationFunc= _lib.integratePlanarOrbit
    integrationFunc.argtypes= [ndpointer(dtype=nu.float64,flags=ndarrayFlags),
                               ctypes.c_int,                             
                               ndpointer(dtype=nu.float64,flags=ndarrayFlags),
                               ctypes.c_int,
                               ndpointer(dtype=nu.int32,flags=ndarrayFlags),
                               ndpointer(dtype=nu.float64,flags=ndarrayFlags),
                               ctypes.c_double,
                               ctypes.c_double,
                               ndpointer(dtype=nu.float64,flags=ndarrayFlags)]

    #Array requirements, first store old order
    f_cont= [yo.flags['F_CONTIGUOUS'],
             t.flags['F_CONTIGUOUS']]
    yo= nu.require(yo,dtype=nu.float64,requirements=['C','W'])
    t= nu.require(t,dtype=nu.float64,requirements=['C','W'])
    result= nu.require(result,dtype=nu.float64,requirements=['C','W'])

    #Run the C code
    integrationFunc(yo,
                    ctypes.c_int(len(t)),
                    t,
                    ctypes.c_int(npot),
                    pot_type,
                    pot_args,
                    ctypes.c_double(rtol),ctypes.c_double(atol),
                    result)

    #Reset input arrays
    if f_cont[0]: yo= nu.asfortranarray(yo)
    if f_cont[1]: t= nu.asfortranarray(t)

    return result
