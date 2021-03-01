from VAOne import *
import pandas as pd
from operator import methodcaller
import math
import traceback
import VAOneGUI as vagui
import sys

sys.path.append('d:/pythonproject')
from vvisualization.read.trimlayer import Nct, Fiber, Foam
from vvisualization.tools import glv_man as glvm
from vvisualization.tools.iterator import findNamedDBElementByIterator


###########################################################################
#   This Script is used to solve Models and select the optimal solution.  #
#                       2020-8-20     Lyq                                 #
#                                                                         #
###########################################################################


# ------------------Excel File Import And Preproccess------------------------#
# df = pd.read_excel(r'd:/fiber.xlsx', header=None, sheet_name="Sheet1")  # 路径改为接受用户输入或用户选择文件
# df.columns = ["Name", "Density", "Flow Resistivity", "Porosity",
#               "Tortuosity", "ViscousLength", "ThermalLength", "SoftLayer1 HardLayer2"]
# df.index = df["Name"]
# df = df.sort_values(by=["SoftLayer1 HardLayer2"])


# with pd.ExcelWriter(r'd:/123_out.xlsx') as writer:  # export to another excel file
#    df.to_excel(writer, sheet_name = "FiberDatabase",index = False)
# testcellread = df.loc["Pufoam"]["Density"]
# print(testcellread)

def batchSolve(plate_name, cav1_name, cav2_name, junction_name, mnct_layup, allin):  # 求解传递损失
    """
    @rtype: tuple(str, double) = (bestsolu_name, best_TL)
    @param plate_name: str
    @param cav1_name: str
    @param cav2_name: str
    @param junction_name: str
    @type mnct_layup: 0 or 1  mnct_layup = 1  选择mnct  mnct_layup = 0 选择layup
    @param allin: 0 or 1  allin = 1 选择database中的所有声学包， allin = 0 选择本次生成的声学包

    """
    db = pi_fNeoDatabaseGetCurrent()
    network = pi_fNeoDatabaseGetNetwork(db)
    env = pi_fNetworkGetAnalysisEnv(network)
    fdom = pi_fAnalysisEnvGetFreqDomain(env)
    vagui.GUI_ClearLog()  # 清空log窗口
    vagui.GUI_DoEvents()  # 准备输出结果到log窗口

    plate = Nct.convert(db, "Plate", plate_name, "Plate")  # p1
    cav1 = Nct.convert(db, "Cavity", cav1_name, "Cavity")  # cavity
    cav2 = Nct.convert(db, "Cavity", cav2_name, "Cavity")  # cavity-13
    junction = Nct.convert(db, "AreaJunction", junction_name, "AreaJunction")  # Area-1
    NumFreqs = pi_fFreqDomainGetCount(fdom)

    NCTs = {}
    if allin and mnct_layup:
        NCTs = findNamedDBElementByIterator(db, 'MultipleTrim')
    if allin and (not mnct_layup):
        NCTs = findNamedDBElementByIterator(db, 'LayeredTrim')
    if (not allin) and mnct_layup:
        NCTs = glvm.getv('mnct')
    if (not allin) and (not mnct_layup):
        NCTs = glvm.getv('layeredtrim')

    best = -1
    best_name = ''

    for elem in NCTs.values():
        if mnct_layup:
            pi_fPlateSetTrimB(plate, pi_fConvertMultipleTrimTrim(elem))
        else:
            pi_fPlateSetTrimB(plate, pi_fConvertLayeredTrimTrim(elem))
        pi_fPlateSetTrimA(plate, None)
        pi_fDatabaseSolve(db)
        ResultsPointer = pi_fResultsGetEffectiveTL(cav1, cav2, junction, fdom)
        temp_sum = 0
        for seq in range(NumFreqs):
            temp_sum += pi_fFloatSpectralFunctionGetVal(ResultsPointer, seq)
        RMS_aver = 10 * math.log(1 / temp_sum) / math.log(10)
        if best < RMS_aver:
            best = RMS_aver
            if mnct_layup:
                best_name = pi_fMultipleTrimGetCName(elem)
            else:
                best_name = pi_fLayeredTrimGetCName(elem)

    print(f"BestSolution:  {best_name}  MaximumAverageTL:  {best}dB")
    return best_name, best


if __name__ == '__main__':
    batchSolve('p1', 'cavity', 'cavity-13', 'Area-1', 0, 1)
