"""
删除
VAOne没有提供获得对象被引用次数的API 盲目删除会报错
pi_f...unref在哪里
"""
from VAOne import *
from vvisualization.tools import glv_man as glvm
import VAOneGUI as vagui


def delNct():
    pass
    # pi_fLayeredTrimDeleteAllLayers()
    # pi_fMultipleTrimRemoveTrim()


def delMat():
    pass


def clearLog():
    vagui.GUI_ClearLog()


def clearSelection():
    vagui.GUI_GlearSelection()
