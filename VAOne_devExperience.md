# 第一个脚本
基本作用:从excel中导入纤维材料的BIOT模型，两两组合建立“软层+硬层”的声学包，求解模型获得最优解

重点:
+ 如何在数据库中找到一个对象 `注意指针类型的转化` 必要时`建立对象列表保存创建的对象` 
+ pandas中`DataFrame`的使用 
+ 检索`APIreferenceGuide`的技巧 `"C+对象名"` , `递归检索`
+ 及时注释
+ 创建对象前注意`同名对象是否已经存在`
+ `pi_f...Unref函数`使用场景不清晰
+ 创建函数实现最大程度代码复用

# 第二个脚本



# 优化函数探索
+ optimizationcreate创建在对象在数据库中
+ pi_fOptimizationRun (COptimization *opt, void *ebInstance, CProgressThreadStruct *pThreadProgress) -> int
 
+ pi_fOptimizationSetScript (COptimization *opt, const char *script)  -> void 
+ pi_fOptimizationAddFunction (COptimization *opt, const char *name, const char *expression) ->COptimizationFunction
  const char *  pi_fOptimizationFunctionGetExpression (COptimizationFunction *function) 
+ objectiveFunctionSecond 
+ NCT的absoption 和 声腔的absorption不同
+ optimization一旦被修改之后，后面对任何的optimization对象进行更改都不会改变优化脚本
+ 一个database中，只能存在一个optimization对象
+ pi_fOptimization optimization回归到没有编辑的状态 脚本是，GUI也是
+ pi_fOptimizationgParameterIsDataComplete 用来写线程进度函数
+ pi_fOptimizationParameterOptimizationReset
+ 用python脚本更改优化对象，会在optimizationscript中引起相应的变化
+ ebinstance = GUI_GetCurrentScriptingInstance() 唯一的到 ebinstance的方法
+ iternal function for parameters and outputvariable
+ 增加optimization函数后需要进行参数更新

# Tips



# pyt
ui文件 用 QFile加载
layout 窗口缩放 空间间距也跟着缩放 layout 可以嵌套
sizepolicy  控件缩放策略  fixed 固定的

先摆放控件->container->layout
调整layout内部控件比例 使用layoutstretch  调整间距 space

pyinstaller 完成程序打包  程序运行中动态使用的外部文件需要复制到可执行文件得同一个目录下面 例如ui文件