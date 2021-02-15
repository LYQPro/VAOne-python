from VAOne import *
import pandas as pd
from operator import methodcaller
import math
import traceback
import VAOneGUI as vagui

###########################################################################
#   This Script is used to create TrimLayers , Treatment Lay-ups          #
#   solve Models and select the optimal solution.                         #
#                       2020-8-20     Lyq                                 #
#                                                                         #
###########################################################################


# ------------------Excel File Import And Preproccess------------------------#
df = pd.read_excel(r'd:/Fiber.xlsx', header=None, sheet_name="FiberDatabase")  # 路径改为接受用户输入或用户选择文件
df.columns = ["Name", "Density", "Flow Resistivity", "Porosity",
              "Tortuosity", "ViscousLength", "ThermalLength", "SoftLayer1 HardLayer2"]
df.index = df["Name"]
df = df.sort_values(by=["SoftLayer1 HardLayer2"])


# with pd.ExcelWriter(r'd:/123_out.xlsx') as writer:  # export to another excel file
#    df.to_excel(writer, sheet_name = "FiberDatabase",index = False)
# testcellread = df.loc["Pufoam"]["Density"]
# print(testcellread)

# ---------------------------type convert function-------------------------#


def FindandConvert(Class, name, aim):
    origin = pi_fNeoDatabaseFindByName(
        db, globals()["pi_f" + Class + "GetClassID"](), name)
    return globals()["pi_fConvertNeoPersist" + aim]((pi_fConvertDBElementNeoPersist(origin)))


# -----------------------perate  Database----------------------------------#
try:
    if not pi_fIsInit():
        pi_fInit()  # Initialized API Function
    db = pi_fNeoDatabaseGetCurrent()
    network = pi_fNeoDatabaseGetNetwork(db)
    env = pi_fNetworkGetAnalysisEnv(network)
    fdom = pi_fAnalysisEnvGetFreqDomain(env)
    vagui.GUI_ClearLog()  # 清空log窗口
    vagui.GUI_DoEvents()  # 准备输出结果到log窗口

    # -----------------------Creat Mateirals Obect-------------------------------#
    for i in df.index:
        Fiber = pi_fNeoDatabaseFindByName(
            db, pi_fFiberGetClassID(), i)  # refenrence
        if Fiber == None:
            print("start creating Materials")
            Fiber = pi_fFiberCreate(db, i, float(
                df["Flow Resistivity"][i]), float(df["Density"][i]))
            pi_fFiberSetPorosity(Fiber, float(df["Porosity"][i]))
            pi_fFiberSetTortuosity(Fiber, float(df["Tortuosity"][i]))
            pi_fFiberSetViscousLength(Fiber, float(df["ViscousLength"][i]))
            pi_fFiberSetThermalLength(Fiber, float(df["ThermalLength"][i]))
        else:
            print("already have {}".format(i))

    #	print("Fibers created")

    air = FindandConvert("Fluid", "Air", "Fluid")
    SoftLayer = []
    HardLayer = []
    combinedNCTs = []
    # ------------------------Creat single layer NCT------------------------------------#
    for i in df.index:
        Fiber = FindandConvert("Fiber", i, "Material")
        if df["SoftLayer1 HardLayer2"][i] == 1:
            NCT = pi_fTrimLayerCreate(Fiber, 0.01, air)  # 软层10mm
            SoftLayer.append((NCT, i))
        else:
            NCT = pi_fTrimLayerCreate(Fiber, 0.003, air)  # 硬层3mm
            HardLayer.append((NCT, i))
    #    print(SoftLayer[0][1])
    # -------------------------Create double layer NCT-------------------------------------#
    for softmat in SoftLayer:
        for hardmat in HardLayer:
            combinedNCTname = softmat[1] + "+" + hardmat[1]
            print(combinedNCTname)
            exist = pi_fNeoDatabaseFindByName(
                db, pi_fLayeredTrimGetClassID(), combinedNCTname)
            if exist is None:
                combinedNCT = pi_fLayeredTrimCreate(db, combinedNCTname)
                pi_fLayeredTrimAddLayer(combinedNCT, hardmat[0])
                pi_fLayeredTrimAddLayer(combinedNCT, softmat[0])
                combinedNCTs.append((combinedNCT, combinedNCTname))
            else:
                print("already haved {}".format(combinedNCTname))
                combinedNCT = FindandConvert(
                    "LayeredTrim", combinedNCTname, "LayeredTrim")
                combinedNCTs.append((combinedNCT, combinedNCTname))
            # print(combinedNCTs)

    # -----------------------------------Apply NCTs---------------------------------------------------#
    plate = FindandConvert("Plate", "p1", "Plate")
    cav1 = FindandConvert("Cavity", "cavity", "Cavity")
    cav2 = FindandConvert("Cavity", "cavity-13", "Cavity")
    junction = FindandConvert("AreaJunction", "Area-1", "AreaJunction")
    NumFreqs = pi_fFreqDomainGetCount(fdom)
    ansval = []

    for i in combinedNCTs:
        pi_fPlateSetTrimB(plate, pi_fConvertLayeredTrimTrim(combinedNCT))
        # pi_fPlateSetTrimA(plate,None)
        solution = pi_fDatabaseSolve(db)
        ResultsPointer = pi_fResultsGetEffectiveTL(cav1, cav2, junction, fdom)
        sum = 0
        for seq in range(NumFreqs):
            sum += pi_fFloatSpectralFunctionGetVal(ResultsPointer, seq)
        RMS_aver = 10 * math.log(1 / sum) / math.log(10)
        ansval.append(RMS_aver)

    # --------------------------------Output----------------------------------------------#
    bestsolu = [0, 0]
    for index, item in enumerate(ansval):
        if bestsolu[1] <= item:
            bestsolu[1] = item  # TL Value
            bestsolu[0] = combinedNCTs[index][1]  # Solution name
    print("BestSolution:{} MaximumAverageTL:{}".format(
        bestsolu[0], bestsolu[1]))


# ---------------------File Close And  Exceptations Operations----------------------------#
except:
    if pi_fIsInit():
        db = pi_fNeoDatabaseGetCurrent
        if pi_fNeoDatabaseIsOpen(db):
            pi_fNeoDatabaseClose(db)
            pi_fNeoDatabaseDispose(db)
    raise
