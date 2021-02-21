# 跨文件全局变量初始化
# 此module必须在最终top-level的脚本中调用一次，且仅能调用一次
from . import glv_man as glvm
from VAOne import *
import VAOneGUI as Vagui

import importlib
importlib.reload(glvm)

glvm._ini()

try:
    if not pi_fIsInit():
        pi_fIsInit()
    db = pi_fNeoDatabaseGetCurrent()
    network = pi_fNeoDatabaseGetNetwork(db)
    env = pi_fNetworkGetAnalysisEnv(network)
    fdom = pi_fAnalysisEnvGetFreqDomain(env)
    Vagui.GUI_DoEvents()
    Vagui.GUI_ClearLog()
    glvm.setv('layeredtrim', {})
    glvm.setv('mnct', {})
    # print(glvm.getv("db"))
    print("""access database done...\nglobal variable configured.....""")

except:
    if pi_fIsInit():
        db = pi_fNeoDatabaseGetCurrent()
        if pi_fNeoDatabaseIsOpen(db):
            pi_fNeoDatabaseClose(db)
            pi_fNeoDatabaseDispose(db)
    raise
