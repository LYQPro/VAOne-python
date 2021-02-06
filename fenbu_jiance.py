
from VAOne import *
from VAOneGUI import *
import iterator
import math
import time
from datetime import timedelta
# from importlib import reload
# reload(iterator)
try:
    db = pi_fNeoDatabaseGetCurrent()
    network = pi_fNeoDatabaseGetNetwork(db)
    env = pi_fNetworkGetAnalysisEnv(network)
    fdom = pi_fAnalysisEnvGetFreqDomain(env)
    # print(pi_fFreqDomainGetFreq(fdom,14))

    opt = pi_fOptimizationGetCurrent()
    pi_fOptimizationInit(opt)  # back to origin
    # print(pi_fOptimizationParameterOptimizationIsDataComplete(opt))
    # pi_fOptimizationParameterOptimizationReset(opt)   # not reset script
    fiberlist = []
    fibernamelist = []
    iterator.Find.FindNamedDBElementByIterator(
        db, "Fiber", fiberlist, fibernamelist)
    # print(fibernamelist)
    # print(type(fiberlist[0]))


    pi_fOptimizationAddFiberDensityInputVar(
        opt, 'inputvar_density_fiber1', pi_fConvertNeoPersistFiber(fiberlist[fibernamelist.index("TCF")]))
    fiber1 = pi_fOptimizationFindInputVariableByName(opt,"inputvar_density_fiber1")
    
   
    param1 = pi_fOptimizationAddParameter(opt,"param_density_fiber1",300.0,250.0,400.0,True,True)
    # print(param1)


    func_param = pi_fOptimizationFindFunctionForParameterByName(opt, "param_density_fiber1")      # ! internal function
    #currentval = pi_fOptimizationFunctionGetCurrentValue(func)



    
    dep = pi_fOptimizationAddDependency(opt,"dep_density_fiber1",fiber1,func_param)         #问题解决
    # inpVar = pi_fOptimizationDependencyGetInputVariable(dep)
    # print(inpVar)


    # vaone_ok = pi_fDatabaseSolveEx(db,1)
    # print(vaone_ok)
  
#####################################################################################
    plate = iterator.Find(db,"Plate", "p1" ).FindandConvert("Plate")
    cav1 = iterator.Find(db,"Cavity", "cavity").FindandConvert("Cavity")
    cav2 = iterator.Find(db,"Cavity", "cavity-13").FindandConvert("Cavity")
    junction = iterator.Find(db,"AreaJunction", "Area-1").FindandConvert("AreaJunction")
    NumFreqs = pi_fFreqDomainGetCount(fdom)

    #布置声学包
    pass




    solution = pi_fDatabaseSolve(db)
    ResultsPointer = pi_fResultsGetEffectiveTL(cav1, cav2, junction, fdom)

    #添加输出变量

    TL_outvar = pi_fOptimizationAddEffectiveSEATLOLVar(opt,"TL",cav2,cav1,junction,fdom)     #透射声功率系数
    TL_outvar = pi_fConvertOptimizationVariableOptimizationOutputVariable(TL_outvar)        #添加成功

    TL_func = pi_fOptimizationFindFunctionForOutputVariableByName(opt,"TL")     

    func1 = pi_fOptimizationAddFunction(opt,"Effective_TL","10*log(1/TL)/log(10)")   #添加真实的传递损失函数

    # ebInstance = GUI_GetCurrentScriptingInstance()
    # ebInstance = pi_fInitializeQuickScript()
    # success = pi_fOptimizationParametricUpdate(opt,ebInstance)                           #这里需要参数更新
    # print(success)

                 





#######################################设置优化选项#######################################

    #设置优化算法
    pi_fOptimizationSetAlgorithm(opt,LD_MMA)

    
    #勾选目标函数
    pi_fOptimizationSetObjectiveFunction(opt,TL_func)          #添加成功  
    
    #勾选优化参数
    param = pi_fOptimizationAddCurrentParameter(opt,param1)          #添加param成功



    #添加约束函数
    func_constrain = pi_fOptimizationFindFunctionForOutputVariableByName(opt,"Total_NCT_Mass")
    constraint = pi_fOptimizationAddConstraint(opt, func_constrain, -1 , 2.8)




######################################################################################
    #优化脚本运行

    # def ThreadProgress():                          #线程进度结构
    #     microsencond = timedelta(0,0,1)
    #     while not pi_fOptimizationParameterVariationIsDataComplete(opt):
    #     pass
    
    ebscript = pi_fOptimizationGetScript(opt)
    ebInstance = GUI_GetCurrentScriptingInstance()
    success = pi_fOptimizationParametricUpdate(opt,None)
    # print(type(ebinstance))
    # success = pi_fOptimizationRun(opt,ebInstance,0)
    # print(success)
######################################################################################
    #保存结果

    
except:
    pi_fNeoDatabaseCommit(db,False)
    pi_fNeoDatabaseClose(db)
    pi_fNeoDatabaseDispose(db)
    raise