import unittest
from SimPEG import *
from SimPEG import EM
import sys
from scipy.constants import mu_0
from SimPEG.EM.Utils.testingUtils import getFDEMProblem

testEB = True
testHJ = True

verbose = False

TOL = 1e-5
FLR = 1e-20 # "zero", so if residual below this --> pass regardless of order
CONDUCTIVITY = 1e1
MU = mu_0
freq = 1e-1
addrandoms = True

SrcType = 'RawVec' #or 'MAgDipole_Bfield', 'CircularLoop', 'RawVec'

def adjointTest(fdemType, comp):
    prb = getFDEMProblem(fdemType, comp, [SrcType], freq)
    print 'Adjoint %s formulation - %s' % (fdemType, comp)

    m  = np.log(np.ones(prb.mapping.nP)*CONDUCTIVITY)
    mu = np.ones(prb.mesh.nC)*MU

    if addrandoms is True:
        m  = m + np.random.randn(prb.mapping.nP)*np.log(CONDUCTIVITY)*1e-1
        mu = mu + np.random.randn(prb.mesh.nC)*MU*1e-1

    survey = prb.survey
    # prb.PropMap.PropModel.mu = mu
    # prb.PropMap.PropModel.mui = 1./mu
    u = prb.fields(m)

    v = np.random.rand(survey.nD)
    w = np.random.rand(prb.mesh.nC)

    vJw = v.dot(prb.Jvec(m, w, u))
    wJtv = w.dot(prb.Jtvec(m, v, u))
    tol = np.max([TOL*(10**int(np.log10(np.abs(vJw)))),FLR])
    print vJw, wJtv, vJw - wJtv, tol, np.abs(vJw - wJtv) < tol
    return np.abs(vJw - wJtv) < tol

class FDEM_AdjointTests(unittest.TestCase):

    if testHJ:
        def test_Jtvec_adjointTest_jxr_Jform(self):
            self.assertTrue(adjointTest('j', 'jxr'))
        def test_Jtvec_adjointTest_jyr_Jform(self):
            self.assertTrue(adjointTest('j', 'jyr'))
        def test_Jtvec_adjointTest_jzr_Jform(self):
            self.assertTrue(adjointTest('j', 'jzr'))
        def test_Jtvec_adjointTest_jxi_Jform(self):
            self.assertTrue(adjointTest('j', 'jxi'))
        def test_Jtvec_adjointTest_jyi_Jform(self):
            self.assertTrue(adjointTest('j', 'jyi'))
        def test_Jtvec_adjointTest_jzi_Jform(self):
            self.assertTrue(adjointTest('j', 'jzi'))

        def test_Jtvec_adjointTest_hxr_Jform(self):
            self.assertTrue(adjointTest('j', 'hxr'))
        def test_Jtvec_adjointTest_hyr_Jform(self):
            self.assertTrue(adjointTest('j', 'hyr'))
        def test_Jtvec_adjointTest_hzr_Jform(self):
            self.assertTrue(adjointTest('j', 'hzr'))
        def test_Jtvec_adjointTest_hxi_Jform(self):
            self.assertTrue(adjointTest('j', 'hxi'))
        def test_Jtvec_adjointTest_hyi_Jform(self):
            self.assertTrue(adjointTest('j', 'hyi'))
        def test_Jtvec_adjointTest_hzi_Jform(self):
            self.assertTrue(adjointTest('j', 'hzi'))

        def test_Jtvec_adjointTest_exr_Jform(self):
            self.assertTrue(adjointTest('j', 'exr'))
        def test_Jtvec_adjointTest_eyr_Jform(self):
            self.assertTrue(adjointTest('j', 'eyr'))
        def test_Jtvec_adjointTest_ezr_Jform(self):
            self.assertTrue(adjointTest('j', 'ezr'))
        def test_Jtvec_adjointTest_exi_Jform(self):
            self.assertTrue(adjointTest('j', 'exi'))
        def test_Jtvec_adjointTest_eyi_Jform(self):
            self.assertTrue(adjointTest('j', 'eyi'))
        def test_Jtvec_adjointTest_ezi_Jform(self):
            self.assertTrue(adjointTest('j', 'ezi'))

        def test_Jtvec_adjointTest_bxr_Jform(self):
            self.assertTrue(adjointTest('j', 'bxr'))
        def test_Jtvec_adjointTest_byr_Jform(self):
            self.assertTrue(adjointTest('j', 'byr'))
        def test_Jtvec_adjointTest_bzr_Jform(self):
            self.assertTrue(adjointTest('j', 'bzr'))
        def test_Jtvec_adjointTest_bxi_Jform(self):
            self.assertTrue(adjointTest('j', 'bxi'))
        def test_Jtvec_adjointTest_byi_Jform(self):
            self.assertTrue(adjointTest('j', 'byi'))
        def test_Jtvec_adjointTest_bzi_Jform(self):
            self.assertTrue(adjointTest('j', 'bzi'))

        # def test_Jtvec_adjointTest_hxr_Hform(self):
        #     self.assertTrue(adjointTest('h', 'hxr'))
        # def test_Jtvec_adjointTest_hyr_Hform(self):
        #     self.assertTrue(adjointTest('h', 'hyr'))
        # def test_Jtvec_adjointTest_hzr_Hform(self):
        #     self.assertTrue(adjointTest('h', 'hzr'))
        # def test_Jtvec_adjointTest_hxi_Hform(self):
        #     self.assertTrue(adjointTest('h', 'hxi'))
        # def test_Jtvec_adjointTest_hyi_Hform(self):
        #     self.assertTrue(adjointTest('h', 'hyi'))
        # def test_Jtvec_adjointTest_hzi_Hform(self):
        #     self.assertTrue(adjointTest('h', 'hzi'))

        # def test_Jtvec_adjointTest_hxr_Hform(self):
        #     self.assertTrue(adjointTest('h', 'jxr'))
        # def test_Jtvec_adjointTest_hyr_Hform(self):
        #     self.assertTrue(adjointTest('h', 'jyr'))
        # def test_Jtvec_adjointTest_hzr_Hform(self):
        #     self.assertTrue(adjointTest('h', 'jzr'))
        # def test_Jtvec_adjointTest_hxi_Hform(self):
        #     self.assertTrue(adjointTest('h', 'jxi'))
        # def test_Jtvec_adjointTest_hyi_Hform(self):
        #     self.assertTrue(adjointTest('h', 'jyi'))
        # def test_Jtvec_adjointTest_hzi_Hform(self):
        #     self.assertTrue(adjointTest('h', 'jzi'))


if __name__ == '__main__':
    unittest.main()
