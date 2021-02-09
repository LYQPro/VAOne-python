#跨文件全局变量初始化
import glv_man as glvm
from VAOne import *
import VAOneGUI as vagui
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
    vagui.GUI_DoEvents()
    vagui.GUI_ClearLog()
    glvm._setv("db",db)
    glvm._setv('network',network)
    glvm._setv("env",env)
    glvm._setv('fdom',fdom)
    # print(glvm._getv("db"))
    print("""access database done...\nglobal variable configured.....""")

except:
    if pi_fIsInit():
        db = pi_fNeoDatabaseGetCurrent()
        if pi_fNeoDatabaseIsOpen(db):
            pi_fNeoDatabaseClose(db)
            pi_fNeoDatabaseDispose(db)
    raise