import importlib
import traceback

from VAOne import *

import glv_man as glvm

import glv_config as glvc

import ntc_create_import as makenct

importlib.reload(makenct)


def Layeredtrim_create():
    """
    use trim create 3 types layered trim
    1) 1 softlayer + 1 hardlayer
    2) 1 softlayer + 1 EVA
    3）0.9mm/0.7mm Al + 1 softlayer + 1 EVA
    4) 1 softlayer
    5) 1 0.9mm steel 
        ........... continue
    """
    pass

def MNCT_create():
    """
    use layeredtrim create MNCT
    这部分比较灵活，可以多层叠加，注意分配各部分的覆盖率

    """
    pass


if __name__ == '__main__':
    loc1 = r'd:/Fiber.xlsx'
    loc2 = r'd:/Foam.xlsx'
    try:
        if not pi_fIsInit():
            pi_fIsInit()
        db = pi_fNeoDatabaseGetCurrent()
        network = pi_fNeoDatabaseGetNetwork(db)
        env = pi_fNetworkGetAnalysisEnv(network)
        fdom = pi_fAnalysisEnvGetFreqDomain(env)
        # vagui.GUI_DoEvents()
        # vagui.GUI_ClearLog()

        fibers = makenct.Fiber(loc1)
        foams = makenct.Foam(loc2)

    except:
        if pi_fIsInit():
            db = pi_fNeoDatabaseGetCurrent()
            if pi_fNeoDatabaseIsOpen(db):
                pi_fNeoDatabaseClose(db)
                pi_fNeoDatabaseDispose(db)
        raise

