# Tests of the evolveddiskdf module
import numpy
from galpy.df import evolveddiskdf, dehnendf
from galpy.potential import LogarithmicHaloPotential, \
    SteadyLogSpiralPotential, \
    EllipticalDiskPotential
_GRIDPOINTS= 31
# globals to save the results from previous calculations to be re-used, pre-setting them allows one to skip tests
_maxi_surfacemass= 0.0672746475968
_maxi_meanvr= -0.000517132979969
_maxi_meanvt= 0.913328340109
_maxi_sigmar2= 0.0457686414529
_maxi_sigmat2= 0.0268245643697
_maxi_sigmart= -0.000541204894097
def test_axi_meanvr_grid():
    # Test that for a close to axisymmetric potential, the mean vr is close to zero
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          SteadyLogSpiralPotential(A=-0.005,omegas=0.2)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    mvr, grid= edf.meanvR(0.9,phi=0.2,integrate_method='rk6_c',grid=True,
                          returnGrid=True,gridpoints=_GRIDPOINTS)
    assert numpy.fabs(mvr) < 0.001, 'meanvR of evolveddiskdf for axisymmetric potential is not equal to zero'
    mvr= edf.meanvR(0.9,phi=0.2,integrate_method='rk6_c',grid=grid)
    assert numpy.fabs(mvr) < 0.001, 'meanvR of evolveddiskdf for axisymmetric potential is not equal to zero when calculated with pre-computed grid'
    #Pre-compute surfmass and use it
    smass= edf.vmomentsurfacemass(0.9,0,0,phi=0.2,integrate_method='rk6_c',
                                  grid=True,gridpoints=_GRIDPOINTS)
    mvr= edf.meanvR(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                    surfacemass=smass)
    assert numpy.fabs(mvr) < 0.001, 'meanvR of evolveddiskdf for axisymmetric potential is not equal to zero when calculated with pre-computed grid and surfacemass'
    global _maxi_meanvr
    _maxi_meanvr= mvr
    global _maxi_surfacemass
    _maxi_surfacemass= smass
    return None
                       
def test_axi_meanvr_direct():
    # Test that for an axisymmetric potential, the mean vr is close to zero
    # We do this for an axisymmetric potential, bc otherwise it takes too long
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.)]
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    mvr= edf.meanvR(0.9,phi=0.2,integrate_method='rk6_c',grid=False)
    assert numpy.fabs(mvr) < 0.001, 'meanvR of evolveddiskdf for axisymmetric potential is not equal to zero when calculated directly'
    return None
                       
def test_axi_meanvr_grid_tlist():
    # Test that for a close to axisymmetric potential, the mean vr is close to zero
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          SteadyLogSpiralPotential(A=-0.005,omegas=0.2)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    mvr, grid= edf.meanvR(0.9,t=[0.,-2.5,-5.,-7.5,-10.],
                          phi=0.2,integrate_method='rk6_c',
                          grid=True,returnGrid=True,gridpoints=_GRIDPOINTS)
    assert numpy.all(numpy.fabs(mvr) < 0.003), 'meanvR of evolveddiskdf for axisymmetric potential is not equal to zero for list of times'
    mvr= edf.meanvR(0.9,t=[0.,-5.,-10.],
                    phi=0.2,integrate_method='rk6_c',grid=grid)
    assert numpy.all(numpy.fabs(mvr) < 0.003), 'meanvR of evolveddiskdf for axisymmetric potential is not equal to zero when calculated with pre-computed grid for list of times'
    return None
                       
def test_axi_meanvt_grid():
    # Test that for a close to axisymmetric potential, the mean vt is close to that of the initial DF
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          SteadyLogSpiralPotential(A=-0.005,omegas=0.2)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    mvt, grid= edf.meanvT(0.9,phi=0.2,integrate_method='rk6_c',grid=True,
                          returnGrid=True,gridpoints=_GRIDPOINTS)
    assert numpy.fabs(mvt-idf.meanvT(0.9)) < 0.005, 'meanvT of evolveddiskdf for axisymmetric potential is not equal to that of the initial dehnendf'
    mvt= edf.meanvT(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                    gridpoints=_GRIDPOINTS,)
    assert numpy.fabs(mvt-idf.meanvT(0.9)) < 0.005, 'meanvT of evolveddiskdf for axisymmetric potential is not equal to that of the initial dehnendf when calculated with pre-computed grid'
    global _maxi_meanvt
    _maxi_meanvt= mvt
    return None
                       
def test_axi_meanvt_hierarchgrid():
    # Test that for a close to axisymmetric potential, the mean vt is close to that of the initial DF
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          SteadyLogSpiralPotential(A=-0.005,omegas=0.2)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    mvt, grid= edf.meanvT(0.9,phi=0.2,integrate_method='rk6_c',grid=True,
                          hierarchgrid=True,
                          returnGrid=True,gridpoints=_GRIDPOINTS)
    assert numpy.fabs(mvt-idf.meanvT(0.9)) < 0.005, 'meanvT of evolveddiskdf for axisymmetric potential is not equal to that of the initial dehnendf when using hierarchgrid'
    mvt= edf.meanvT(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                    gridpoints=_GRIDPOINTS)
    assert numpy.fabs(mvt-idf.meanvT(0.9)) < 0.005, 'meanvT of evolveddiskdf for axisymmetric potential is not equal to that of the initial dehnendf when calculated with pre-computed grid when using hierarchgrid'
    return None
                       
def test_axi_meanvt_direct():
    # Test that for a close to axisymmetric potential, the mean vt is close to that of the initial DF
    # We do this for an axisymmetric potential, bc otherwise it takes too long
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.)]
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    mvt= edf.meanvT(0.9,phi=0.2,integrate_method='rk6_c',grid=False)
    assert numpy.fabs(mvt-idf.meanvT(0.9)) < 0.001, 'meanvT of evolveddiskdf for axisymmetric potential is not equal to that of the initial dehnendf when using direct integration'
    return None
                       
def test_axi_sigmar2_grid():
    # Test that for a close to axisymmetric potential, the sigmaR2 is close to the value of the initial DF
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          SteadyLogSpiralPotential(A=-0.005,omegas=0.2)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    sr2, grid= edf.sigmaR2(0.9,phi=0.2,integrate_method='rk6_c',grid=True,
                           returnGrid=True,gridpoints=_GRIDPOINTS)
    isr2= idf.sigmaR2(0.9)
    assert numpy.fabs(numpy.log(sr2)-numpy.log(isr2)) < 0.025, 'sigmar2 of evolveddiskdf for axisymmetric potential is not equal to that of initial DF'
    sr2= edf.sigmaR2(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                     gridpoints=_GRIDPOINTS)
    assert numpy.fabs(numpy.log(sr2)-numpy.log(isr2)) < 0.025, 'sigmar2 of evolveddiskdf for axisymmetric potential is not equal to that of initial DF when calculated with pre-computed grid'
    sr2= edf.sigmaR2(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                     meanvR=_maxi_meanvr,surfacemass=_maxi_surfacemass,
                     gridpoints=_GRIDPOINTS)
    assert numpy.fabs(numpy.log(sr2)-numpy.log(isr2)) < 0.025, 'sigmar2 of evolveddiskdf for axisymmetric potential is not equal to that of initial DF when calculated with pre-computed grid and meanvR,surfacemass'
    global _maxi_sigmar2
    _maxi_sigmar2= sr2
    return None
                       
def test_axi_sigmar2_direct():
    # Test that for an axisymmetric potential, the sigmaR2  is close to the value of the initial DF   
    # We do this for an axisymmetric potential, bc otherwise it takes too long
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.)]
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    sr2= edf.sigmaR2(0.9,phi=0.2,integrate_method='rk6_c',grid=False)
    isr2= idf.sigmaR2(0.9)
    assert numpy.fabs(numpy.log(sr2)-numpy.log(isr2)) < 0.025, 'sigmar2 of evolveddiskdf for axisymmetric potential is not equal to that of initial DF when calculated directly'
    return None
                       
def test_axi_sigmat2_grid():
    # Test that for a close to axisymmetric potential, the sigmaR2 is close to the value of the initial DF
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          SteadyLogSpiralPotential(A=-0.005,omegas=0.2)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    st2, grid= edf.sigmaT2(0.9,phi=0.2,integrate_method='rk6_c',grid=True,
                           returnGrid=True,gridpoints=_GRIDPOINTS)
    ist2= idf.sigmaT2(0.9)
    assert numpy.fabs(numpy.log(st2)-numpy.log(ist2)) < 0.025, 'sigmat2 of evolveddiskdf for axisymmetric potential is not equal to that of initial DF'
    st2= edf.sigmaT2(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                     gridpoints=_GRIDPOINTS)
    assert numpy.fabs(numpy.log(st2)-numpy.log(ist2)) < 0.025, 'sigmat2 of evolveddiskdf for axisymmetric potential is not equal to that of initial DF when calculated with pre-computed grid'
    st2= edf.sigmaT2(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                     meanvT=_maxi_meanvt,surfacemass=_maxi_surfacemass,
                     gridpoints=_GRIDPOINTS)
    assert numpy.fabs(numpy.log(st2)-numpy.log(ist2)) < 0.025, 'sigmat2 of evolveddiskdf for axisymmetric potential is not equal to that of initial DF when calculated with pre-computed grid and meanvR,surfacemass'
    global _maxi_sigmat2
    _maxi_sigmat2= st2
    return None
                       
def test_axi_sigmat2_direct():
    # Test that for an axisymmetric potential, the sigmaT2  is close to the value of the initial DF   
    # We do this for an axisymmetric potential, bc otherwise it takes too long
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.)]
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    st2= edf.sigmaT2(0.9,phi=0.2,integrate_method='rk6_c',grid=False)
    ist2= idf.sigmaT2(0.9)
    assert numpy.fabs(numpy.log(st2)-numpy.log(ist2)) < 0.025, 'sigmat2 of evolveddiskdf for axisymmetric potential is not equal to that of initial DF when calculated directly'
    return None
                       
def test_axi_sigmart_grid():
    # Test that for a close to axisymmetric potential, the sigmaR2 is close to zero
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          SteadyLogSpiralPotential(A=-0.005,omegas=0.2)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    srt, grid= edf.sigmaRT(0.9,phi=0.2,integrate_method='rk6_c',grid=True,
                           returnGrid=True,gridpoints=_GRIDPOINTS)
    assert numpy.fabs(srt) < 0.01, 'sigmart of evolveddiskdf for axisymmetric potential is not equal to zero'
    srt= edf.sigmaRT(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                     gridpoints=_GRIDPOINTS)
    assert numpy.fabs(srt) < 0.01, 'sigmart of evolveddiskdf for axisymmetric potential is not equal zero when calculated with pre-computed grid'
    srt= edf.sigmaRT(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                     meanvR=_maxi_meanvr,
                     meanvT=_maxi_meanvt,surfacemass=_maxi_surfacemass,
                     gridpoints=_GRIDPOINTS)
    assert numpy.fabs(srt) < 0.01, 'sigmart of evolveddiskdf for axisymmetric potential is not equal to zero when calculated with pre-computed grid and meanvR,surfacemass'
    global _maxi_sigmart
    _maxi_sigmart= srt
    return None
                       
def test_axi_sigmart_direct():
    # Test that for an axisymmetric potential, the sigmaRT is close zero
    # We do this for an axisymmetric potential, bc otherwise it takes too long
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.)]
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    srt= edf.sigmaRT(0.9,phi=0.2,integrate_method='rk6_c',grid=False)
    assert numpy.fabs(srt) < 0.01, 'sigmart of evolveddiskdf for axisymmetric potential is not equal to zero when calculated directly'
    return None
                       
def test_axi_vertexdev_grid():
    # Test that for a close to axisymmetric potential, the vertex deviation is close to zero
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          SteadyLogSpiralPotential(A=-0.005,omegas=0.2)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    vdev, grid= edf.vertexdev(0.9,phi=0.2,integrate_method='rk6_c',grid=True,
                              returnGrid=True,gridpoints=_GRIDPOINTS)
    assert numpy.fabs(vdev) < 2., 'vertexdev of evolveddiskdf for axisymmetric potential is not close to zero' #2 is pretty big, but the weak spiral creates that
    vdev= edf.vertexdev(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                        gridpoints=_GRIDPOINTS)
    assert numpy.fabs(vdev) < 2., 'vertexdev of evolveddiskdf for axisymmetric potential is not equal zero when calculated with pre-computed grid'
    vdev= edf.vertexdev(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                        sigmaR2=_maxi_sigmar2,sigmaT2=_maxi_sigmat2,
                        sigmaRT=_maxi_sigmart,gridpoints=_GRIDPOINTS)
    assert numpy.fabs(vdev) < 2., 'sigmart of evolveddiskdf for axisymmetric potential is not equal to zero when calculated with pre-computed sigmaR2,sigmaT2,sigmaRT'
    return None
                       
def test_axi_vertexdev_direct():
    # Test that for an axisymmetric potential, the vertex deviation is close zero
    # We do this for an axisymmetric potential, bc otherwise it takes too long
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.)]
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    vdev= edf.vertexdev(0.9,phi=0.2,integrate_method='rk6_c',grid=False)
    assert numpy.fabs(vdev) < 0.01, 'vertexdev of evolveddiskdf for axisymmetric potential is not equal to zero when calculated directly'
    return None
                       
def test_axi_oortA_grid():
    # Test that for a close to axisymmetric potential, the oortA is close to the value of the initial DF
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          EllipticalDiskPotential(twophio=0.001)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    oa, grid, dgridR, dgridphi=\
        edf.oortA(0.9,phi=0.2,integrate_method='rk6_c',
                  grid=True,derivRGrid=True,derivphiGrid=True,
                  returnGrids=True,
                  gridpoints=_GRIDPOINTS,derivGridpoints=_GRIDPOINTS)
    ioa= idf.oortA(0.9)
    assert numpy.fabs(oa-ioa) < 0.005, 'oortA of evolveddiskdf for axisymmetric potential is not equal to that of initial DF'
    oa= edf.oortA(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                  derivRGrid=dgridR,derivphiGrid=dgridphi,
                  gridpoints=_GRIDPOINTS,derivGridpoints=_GRIDPOINTS)
    assert numpy.fabs(oa-ioa) < 0.005, 'oortA of evolveddiskdf for axisymmetric potential is not equal to that of initial DF when calculated with pre-computed grid'
    return None
                       
def test_axi_oortB_grid():
    # Test that for a close to axisymmetric potential, the oortB is close to the value of the initial DF
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          EllipticalDiskPotential(twophio=0.001)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    ob, grid, dgridR, dgridphi=\
        edf.oortB(0.9,phi=0.2,integrate_method='rk6_c',
                  grid=True,derivRGrid=True,derivphiGrid=True,
                  returnGrids=True,
                  gridpoints=_GRIDPOINTS,derivGridpoints=_GRIDPOINTS)
    iob= idf.oortB(0.9)
    assert numpy.fabs(ob-iob) < 0.005, 'oortB of evolveddiskdf for axisymmetric potential is not equal to that of initial DF'
    ob= edf.oortB(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                  derivRGrid=dgridR,derivphiGrid=dgridphi,
                  gridpoints=_GRIDPOINTS,derivGridpoints=_GRIDPOINTS)
    assert numpy.fabs(ob-iob) < 0.005, 'oortB of evolveddiskdf for axisymmetric potential is not equal to that of initial DF when calculated with pre-computed grid'
    return None
                       
def test_axi_oortC_grid():
    # Test that for a close to axisymmetric potential, the oortC is close to zero
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          EllipticalDiskPotential(twophio=0.001)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    oc, grid, dgridR, dgridphi=\
        edf.oortC(0.9,phi=0.2,integrate_method='rk6_c',
                  grid=True,derivRGrid=True,derivphiGrid=True,
                  returnGrids=True,
                  gridpoints=_GRIDPOINTS,derivGridpoints=_GRIDPOINTS)
    assert numpy.fabs(oc) < 0.005, 'oortC of evolveddiskdf for axisymmetric potential is not equal to that of initial DF'
    oc= edf.oortC(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                    derivRGrid=dgridR,derivphiGrid=dgridphi,
                  gridpoints=_GRIDPOINTS,derivGridpoints=_GRIDPOINTS)
    assert numpy.fabs(oc) < 0.005, 'oortC of evolveddiskdf for axisymmetric potential is not equal to that of initial DF when calculated with pre-computed grid'
    return None
                       
def test_axi_oortK_grid():
    # Test that for a close to axisymmetric potential, the oortK is close to zero
    idf= dehnendf(beta=0.)
    pot= [LogarithmicHaloPotential(normalize=1.),
          EllipticalDiskPotential(twophio=0.001)] #very mild non-axi
    edf= evolveddiskdf(idf,pot=pot,to=-10.)
    ok, grid, dgridR, dgridphi=\
        edf.oortK(0.9,phi=0.2,integrate_method='rk6_c',
                  grid=True,derivRGrid=True,derivphiGrid=True,
                  returnGrids=True,
                  gridpoints=_GRIDPOINTS,derivGridpoints=_GRIDPOINTS)
    assert numpy.fabs(ok) < 0.005, 'oortK of evolveddiskdf for axisymmetric potential is not equal to that of initial DF'
    ok= edf.oortK(0.9,phi=0.2,integrate_method='rk6_c',grid=grid,
                    derivRGrid=dgridR,derivphiGrid=dgridphi,
                  gridpoints=_GRIDPOINTS,derivGridpoints=_GRIDPOINTS)
    assert numpy.fabs(ok) < 0.005, 'oortK of evolveddiskdf for axisymmetric potential is not equal to that of initial DF when calculated with pre-computed grid'
    return None
                       