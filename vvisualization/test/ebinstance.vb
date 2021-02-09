'****************************************************************************************'
'                              DESIGN OPTIMIZATION SCRIPT
'****************************************************************************************'
'
' This script is called by the Design Optimization module at every iteration of a Design
' Optimization method.  By default, the script is used to 'get' and 'set' the values of variables, 
' parameters and functions that have been defined through the GUI.  
'
' The script can, however, be edited in order to:
'
' (i) add custom input variables that are not currently available through the GUI
' (ii) add custom output variables that are not currently available through the GUI
' (iii) add customized functions
' (iv) add custom operations at each iteration of a design method (for example batch meshing etc.)
'
' Once the script has been modified, it becomes 'locked' and is no longer updated when a
' design optimization object is added or removed through the GUI (the GUI should then no
' longer be used to create or delete new optimization objects). To revert back to an 'unlocked'
' version of the script (and enable editing via the GUI), the user should choose the menu option: 
' Tools > Design Optimization > Script(advanced) > Reset  
'
' The recommended process for modifying the design optimization script is:
' 
' (i) use the GUI to set up an initial design optimization that already includes 
'     'placeholder' objects for parameters, variables, functions and dependencies
' (ii) open this script and look for the locations where the objects are referenced
' (iii) replace the PI calls for the objects that you would like to customize
' (iv) add any additional PI calls for custom steps you would like to perform at each iteration
' (v) save the script and then run a design optimization method through the GUI
'
'****************************************************************************************'
'
' The script is organized as follows:
'
' 1. Declarations : [Do not edit]
'   a. Global settings and database handles
'   b. Parameter declarations
'   c. Cached function value declarations (function values from previous script call)
'
' 2. Defining QuickScript functions to get/set the values of Design Optimization objects : [Sections a, b, e Editable]
'   a. QuickScript functions used to 'get' the values of input and output variables
'   b. Quickscript functions used to 'get' the values of Design Optimization functions
'   c. Quickscript functions used to 'pass' the values of parameters
'   d. Quickscript functions used to 'pass' the values of output variables
'   e. Quickscript functions used to 'set' the values of input variables
'
' 3. Main Function: [Sections c, d Editable] 
'   a. Assign the parameter values provided to the script by the Design Optimization method
'   b. Assign the cached values of the objects when the script was last run
'   c. Assign dependencies
'   d. Solve the model
'   e. Assign values of functions
'   f. Assign values of parameters
'   g. Assign values of output variables
'
'****************************************************************************************' 


'======================================================================================='
' 1. Declarations : [Do not edit]
'======================================================================================='

' a. Global settings and database handles
Option Base 0                                     '数据库句柄
Option Explicit                                   
Dim vaone_db As Long
 
' b. Parameter declarations                        ' 全局参数声明
Global parameter_density_TCF As Double
Global parameter_flow_resistivity_TCF As Double
Global parameter_thickness_TCF As Double
Global parameter_porosity_TCF As Double
Global parameter_tortuosity_TCF As Double
Global parameter_viscouslength_TCF As Double
Global parameter_thermallength_TCF As Double

' c. Cached function value declarations
Global function1_ As Double                                   '缓存函数值声明
Global overall_TL_ As Double
Global absorption_ As Double
Global vaone_parameter_density_TCF_ As Double
Global vaone_parameter_flow_resistivity_TCF_ As Double
Global vaone_parameter_thickness_TCF_ As Double
Global vaone_parameter_porosity_TCF_ As Double
Global vaone_parameter_tortuosity_TCF_ As Double
Global vaone_parameter_viscouslength_TCF_ As Double
Global vaone_parameter_thermallength_TCF_ As Double
Global vaone_Total_NCT_Mass_ As Double
Global vaone_Effective_TL_ As Double
Global vaone_Absorption_w_ As Double


'=================================================================================================================='
' 2. Defining QuickScript functions to get/set the values of Design Optimization objects : [Editable (2a, 2b, 2e)]
'=================================================================================================================='

' a. QuickScript functions used to 'get' the values of input and output variables      '获取输入输出变量值
Function Total_NCT_Mass() As Double
	Total_NCT_Mass = pi_fOptimizationOutputVariableGetValue(pi_fOptimizationFindOutputVariableByName(pi_fOptimizationGetCurrent(),"Total_NCT_Mass"))
End Function

Function density_TCF() As Double
	density_TCF = pi_fOptimizationInputVariableGetValue(pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"density_TCF"))
End Function

Function flow_resistivity_TCF() As Double
	flow_resistivity_TCF = pi_fOptimizationInputVariableGetValue(pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"flow_resistivity_TCF"))
End Function

Function thickness_TCF() As Double
	thickness_TCF = pi_fOptimizationInputVariableGetValue(pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"thickness_TCF"))
End Function

Function porosity_TCF() As Double
	'porosity_TCF = pi_fOptimizationInputVariableGetValue(pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"porosity_TCF"))
    dim j as long
	j=pi_fNeoDatabaseFindByName(vaone_db,pi_fFiberGetClassID,"TCF")
	porosity_TCF=pi_fFiberGetPorosity(j)
End Function

Function tortuosity_TCF() As Double
	'tortuosity_TCF = pi_fOptimizationInputVariableGetValue(pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"tortuosity_TCF"))
    dim j as long
	j=pi_fNeoDatabaseFindByName(vaone_db,pi_fFiberGetClassID,"TCF")
	tortuosity_TCF=pi_fFiberGetTortuosity(j)
End Function

Function viscouslength_TCF() As Double
	'viscouslength_TCF = pi_fOptimizationInputVariableGetValue(pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"viscouslength_TCF"))
    dim j as long
	j=pi_fNeoDatabaseFindByName(vaone_db,pi_fFiberGetClassID,"TCF")
	viscouslength_TCF=pi_fFiberGetViscousLength(j)
End Function

Function thermallength_TCF() As Double
	'thermallength_TCF = pi_fOptimizationInputVariableGetValue(pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"thermallength_TCF"))
    dim j as long
	j=pi_fNeoDatabaseFindByName(vaone_db,pi_fFiberGetClassID,"TCF")
	thermallength_TCF=pi_fFiberGetThermalLength(j)
End Function

Function Effective_TL() As Double
	Effective_TL = pi_fOptimizationOutputVariableGetValue(pi_fOptimizationFindOutputVariableByName(pi_fOptimizationGetCurrent(),"Effective_TL"))
End Function

Function Absorption_w() As Double
	'Absorption_w = pi_fOptimizationOutputVariableGetValue(pi_fOptimizationFindOutputVariableByName(pi_fOptimizationGetCurrent(),"Absorption_w"))
Dim network As Long, db As Long, env As Long, fdom As Long
dim air as long,alu as long	 

db = pi_fNeoDatabaseGetCurrent	 
network = pi_fNeoDatabaseGetNetwork(db) 
env = pi_fNetworkGetAnalysisEnv(network)
fdom = pi_fAnalysisEnvGetFreqDomain(env)

dim index as integer
dim Freq(1 to 20) as single
dim P2(1 to 20) as single
dim NumFreqs as integer
dim j as long,a as single
NumFreqs=pi_fFreqDomainGetCount(fdom)
air=pi_fNeoDatabaseFindByName(db,pi_fFluidGetClassID,"Air")
j=pi_fNeoDatabaseFindByName(db,pi_fLayeredTrimGetClassID,"HMP+TCF")           '这里只是得到了一种声学包的吸收率么
                                                                               
for index=1 To NumFreqs
            Freq(index) = pi_fFreqDomainGetFreq(fdom,index-1)
			P2(index)=pi_fLayeredTrimGetAbsorption(j,Freq(index),air)
next
a=0
for index=1 To NumFreqs
            a=a+P2(index)
next
a=a/15
Absorption_w=a
End Function

' b. Quickscript functions used to 'get' the values of Design Optimization functions
Function function1() As Double
	function1 = 0
End Function

Function overall_TL() As Double
	overall_TL = -1*Effective_TL
End Function

Function absorption() As Double
	absorption = -1*Absorption_w
End Function

' c. Quickscript functions used to 'pass' the values of parameters
Function vaone_parameter_density_TCF() As Double
	vaone_parameter_density_TCF = parameter_density_TCF
End Function

Function vaone_parameter_flow_resistivity_TCF() As Double
	vaone_parameter_flow_resistivity_TCF = parameter_flow_resistivity_TCF
End Function

Function vaone_parameter_thickness_TCF() As Double
	vaone_parameter_thickness_TCF = parameter_thickness_TCF
End Function

Function vaone_parameter_porosity_TCF() As Double
	vaone_parameter_porosity_TCF = parameter_porosity_TCF
End Function

Function vaone_parameter_tortuosity_TCF() As Double
	vaone_parameter_tortuosity_TCF = parameter_tortuosity_TCF
End Function

Function vaone_parameter_viscouslength_TCF() As Double
	vaone_parameter_viscouslength_TCF = parameter_viscouslength_TCF
End Function

Function vaone_parameter_thermallength_TCF() As Double
	vaone_parameter_thermallength_TCF = parameter_thermallength_TCF
End Function

' d. Quickscript functions used to 'pass' the values of output variables
Function vaone_Total_NCT_Mass() As Double
	vaone_Total_NCT_Mass = Total_NCT_Mass
End Function

Function vaone_Effective_TL() As Double
	vaone_Effective_TL = Effective_TL
End Function

Function vaone_Absorption_w() As Double
	vaone_Absorption_w = Absorption_w
End Function

' e. Quickscript functions used to 'set' the values of input variables
Sub set_density_TCF(ByVal arg As Double)
	pi_fOptimizationInputVariableSetValue pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"density_TCF"), arg
End Sub

Sub set_flow_resistivity_TCF(ByVal arg As Double)
	pi_fOptimizationInputVariableSetValue pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"flow_resistivity_TCF"), arg
End Sub

Sub set_thickness_TCF(ByVal arg As Double)
	pi_fOptimizationInputVariableSetValue pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"thickness_TCF"), arg
End Sub

Sub set_porosity_TCF(ByVal arg As Double)
	'pi_fOptimizationInputVariableSetValue pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"porosity_TCF"), arg
    dim j as long
	j=pi_fNeoDatabaseFindByName(vaone_db,pi_fFiberGetClassID,"TCF")
	pi_fFiberSetPorosity j,arg
End Sub

Sub set_tortuosity_TCF(ByVal arg As Double)
	'pi_fOptimizationInputVariableSetValue pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"tortuosity_TCF"), arg
    dim j as long
	j=pi_fNeoDatabaseFindByName(vaone_db,pi_fFiberGetClassID,"TCF")
	pi_fFiberSetTortuosity j,arg
End Sub

Sub set_viscouslength_TCF(ByVal arg As Double)
	'pi_fOptimizationInputVariableSetValue pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"viscouslength_TCF"), arg
    dim j as long
	j=pi_fNeoDatabaseFindByName(vaone_db,pi_fFiberGetClassID,"TCF")
	pi_fFiberSetViscousLength j,arg
End Sub

Sub set_thermallength_TCF(ByVal arg As Double)
	'pi_fOptimizationInputVariableSetValue pi_fOptimizationFindInputVariableByName(pi_fOptimizationGetCurrent(),"thermallength_TCF"), arg
    dim j as long
	j=pi_fNeoDatabaseFindByName(vaone_db,pi_fFiberGetClassID,"TCF")
	pi_fFiberSetThermalLength j,arg
End Sub


'============================================================================================'
' 3. Main function : Editable (3c, 3d)
'============================================================================================'

Sub MainFunction(ByRef vaone_theta() As Double, ByVal vaone_solveFlag As Boolean, ByRef vaone_function() As Double, ByRef vaone_functionPrevious() As Double, vaone_IsInit As Boolean)

vaone_db = pi_fNeoDatabaseGetCurrent()

' a. Assign the parameter values provided to the script by the Design Optimization method
parameter_density_TCF = vaone_theta(0)
parameter_flow_resistivity_TCF = vaone_theta(1)
parameter_thickness_TCF = vaone_theta(2)
parameter_porosity_TCF = vaone_theta(3)
parameter_tortuosity_TCF = vaone_theta(4)
parameter_viscouslength_TCF = vaone_theta(5)
parameter_thermallength_TCF = vaone_theta(6)

' b. Assign the cached values of the objects when the script was last run
function1_ = vaone_functionPrevious(0)
overall_TL_ = vaone_functionPrevious(1)
absorption_ = vaone_functionPrevious(2)
vaone_parameter_density_TCF_ = vaone_functionPrevious(3)
vaone_parameter_flow_resistivity_TCF_ = vaone_functionPrevious(4)
vaone_parameter_thickness_TCF_ = vaone_functionPrevious(5)
vaone_parameter_porosity_TCF_ = vaone_functionPrevious(6)
vaone_parameter_tortuosity_TCF_ = vaone_functionPrevious(7)
vaone_parameter_viscouslength_TCF_ = vaone_functionPrevious(8)
vaone_parameter_thermallength_TCF_ = vaone_functionPrevious(9)
vaone_Total_NCT_Mass_ = vaone_functionPrevious(10)
vaone_Effective_TL_ = vaone_functionPrevious(11)
vaone_Absorption_w_ = vaone_functionPrevious(12)

' c. Assign dependencies
' dependency_density_TCF dependency
If vaone_IsInit Or Not(vaone_parameter_density_TCF=vaone_parameter_density_TCF_) Then
	set_density_TCF vaone_parameter_density_TCF
End If

' dependency_flow_resistivity_TCF dependency
If vaone_IsInit Or Not(vaone_parameter_flow_resistivity_TCF=vaone_parameter_flow_resistivity_TCF_) Then
	set_flow_resistivity_TCF vaone_parameter_flow_resistivity_TCF
End If

' dependency_thickness_layer_1_HMP_TCF dependency
If vaone_IsInit Or Not(vaone_parameter_thickness_TCF=vaone_parameter_thickness_TCF_) Then
	set_thickness_TCF vaone_parameter_thickness_TCF
End If

' dependency_coverage_treatment_1_opti dependency
If vaone_IsInit Or Not(vaone_parameter_porosity_TCF=vaone_parameter_porosity_TCF_) Then
	set_porosity_TCF vaone_parameter_porosity_TCF
End If

' dependency_density_TCF1 dependency
If vaone_IsInit Or Not(vaone_parameter_tortuosity_TCF=vaone_parameter_tortuosity_TCF_) Then
	set_tortuosity_TCF vaone_parameter_tortuosity_TCF
End If

' dependency_flow_resistivity_TCF1 dependency
If vaone_IsInit Or Not(vaone_parameter_viscouslength_TCF=vaone_parameter_viscouslength_TCF_) Then
	set_viscouslength_TCF vaone_parameter_viscouslength_TCF
End If

' dependency_thickness_layer_2_diy dependency
If vaone_IsInit Or Not(vaone_parameter_thermallength_TCF=vaone_parameter_thermallength_TCF_) Then
	set_thermallength_TCF vaone_parameter_thermallength_TCF
End If


' Code for custom operations (e. g. remeshing) performed at each iteration must be inserted here
' (Inserted code can either contain API functions or calls to some
' custom subroutines that need to be defined before the start of the MainFunction)

' d. Solve the model
If vaone_solveFlag Then
	Dim vaone_ok As Boolean

	' Code for resolving intermediate results at each iteration must be inserted here
	' (Inserted code can either contain API functions or calls to some
	' custom subroutines that need to be defined before the start of the MainFunction)

	vaone_ok = pi_fDatabaseSolveEx(vaone_db,1)
	If Not vaone_ok Then
		' raise an error here
		Print "Error: Could not solve database"
		Err.Raise 22001
	End If
End If

' e. Assign values of functions
vaone_function(0) = function1
vaone_function(1) = overall_TL
vaone_function(2) = absorption

' f. Assign values of parameters
vaone_function(3) = vaone_parameter_density_TCF
vaone_function(4) = vaone_parameter_flow_resistivity_TCF
vaone_function(5) = vaone_parameter_thickness_TCF
vaone_function(6) = vaone_parameter_porosity_TCF
vaone_function(7) = vaone_parameter_tortuosity_TCF
vaone_function(8) = vaone_parameter_viscouslength_TCF
vaone_function(9) = vaone_parameter_thermallength_TCF

' g. Assign values of output variables
vaone_function(10) = vaone_Total_NCT_Mass
vaone_function(11) = vaone_Effective_TL
vaone_function(12) = vaone_Absorption_w

End Sub