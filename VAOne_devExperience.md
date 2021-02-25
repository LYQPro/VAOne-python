## 第一个脚本
基本作用:从excel中导入纤维材料的BIOT模型，两两组合建立“软层+硬层”的声学包，求解模型获得最优解

重点:
+ 如何在数据库中找到一个对象 `注意指针类型的转化` 必要时`建立对象列表保存创建的对象` 
+ pandas中`DataFrame`的使用 
+ 检索`APIreferenceGuide`的技巧 `"C+对象名"` , `递归检索`
+ 及时注释
+ 创建对象前注意`同名对象是否已经存在`
+ `pi_f...Unref函数`使用场景不清晰
+ 创建函数实现最大程度代码复用

## 第二个脚本



## 优化函数探索
+ optimizationCreate创建在对象在数据库中
+ pi_fOptimizationRun (COptimization *opt, void *ebInstance, CProgressThreadStruct *pThreadProgress) -> int
 
+ pi_fOptimizationSetScript (COptimization *opt, const char *script)  -> void 
+ pi_fOptimizationAddFunction (COptimization *opt, const char *name, const char *expression) ->COptimizationFunction
  const char *  pi_fOptimizationFunctionGetExpression (COptimizationFunction *function) 
+ objectiveFunctionSecond 
+ NCT的absorption 和 声腔的absorption不同
+ optimization一旦被修改之后，后面对任何的optimization对象进行更改都不会改变优化脚本
+ 一个database中，只能存在一个optimization对象
+ pi_fOptimization optimization回归到没有编辑的状态 脚本是，GUI也是
+ pi_fOptimizationParameterIsDataComplete 用来写线程进度函数
+ pi_fOptimizationParameterOptimizationReset
+ 用python脚本更改优化对象，会在optimizationScript中引起相应的变化
+ ebInstance = GUI_GetCurrentScriptingInstance() 唯一的到 ebInstance的方法
+ internal function for parameters and outputVariable
+ 增加optimization函数后需要进行参数更新

## Tips





##全局变量管理
__pycache__ 由于import module生成
__pycache__ 里面的*.pyc、 *.pyo 会在首次import module   (这里的首次是指对于python解释器启动后的首次)
或者 module源代码发生改变时重新生成   (importlib.reload(module)) 

glv_config 一定只能在最终的脚本里启动一次   
由于pycache的存在VAOne启动后 主脚本中的 import glv_config 将会使用pycache中的内容 所以主脚本不能检测到跨文件（VAOne）数据库的变化
而如果每次都reload(glv_config)的话 每次都会触发 glv_config 中的 glvm_ini() 将全局变量全部清空  这将导致本文件的上次导入信息丢失


为了检测文件的变化 必须使用 pi_fNeoDatabaseGetcurrent



##VAOne环境的天坑
+ **管理员模式**安装packages。仍然失败，更改python36文件的权限
+   不要随便安装pyqt5_tools会改变VAOne的固有动态链接库，后续会出现问题
+ 添加系统变量:
````
变量名:             QT_QPA_PLATFORM_PLUGIN_PATH
路径:   C:\Program Files\ESI Group\VAOne2019\Python36\Lib\site-packages\PyQt5\Qt\plugins\platforms
````
+ 安装pyqt5_plugins:
导致PyQt5版本改变 重新安装**PyQt5==5.11.2**  **必须是这个版本**

+ VAOne中运行PyQt5程序需要添加:     <font color=red>QApplication实例只能存在一个</font>

if QApplication.instance() is None:
app = QApplication(sys.argv)
standalone = True
else:
standalone=False
+ iterator的究极神坑 
>It is important to note that objects cannot be deleted from the database while an iterator exists.
>Modifying the database structure while iterating through it will cause unpredictable results
- [x]  **不要轻易使用赋值语句**
- [x]  **绝大多数的赋值语句产生的左值将会自动添加到数据库中，改变了数据库的结构。 如果这个时候有任何<CIterator\*>存在将会发生不可预测的错误**

+ 永远不要向api函数传入None参数，这会引发不可恢复的错误。传入其他错误参数则会有类型报错。因此<font color=grean>出现unrecoverable mistake首先考虑是否传入了None</font>

+ 在VAOne内部运行python脚本， sys.stdout自动被定向到python console, sys.stdin = None 
如果要得到用户输入只能通过QT界面获得用户输入


##模块化
+ 尽可能不要在子模块中使用全局变量
+ 函数功能尽可能解耦，同时保持传入参数不能过多

##字符串模式匹配


##todo
+ 子模块编写完成把绝对引用改成相对引用？
+ 消除sys.path.append


##语音助手
````python
import win32com.client
# 直接调用操作系统的语音接口
speaker = win32com.client.Dispatch("SAPI.SpVoice")
# 输入你想要说的话，前提是操作系统语音助手要认识。一般中文和英文是没有问题的
speaker.Speak("他能秒我，他能秒杀我？他要是能把我秒了，我当场······")
````

##C/C++ Python混合编程 通过dll库和ctypes
```shell
gcc -o example.dll -shared example.c
lib = ctypes.CDLL(‘dll所在路径’)
getattr(dll,“func”,) is not None
lib.func
```

## pyqt多进程、界面数据同步
+ <font color = pink>无法通过对象成员变量进行成员函数的通讯</font> 
+ 类成员变量能够随意在类的对象成员之间任意传递(目前看起来是这样)
+ 线程、进程
+ 进程间通信
+ pyqtSignal、pyqtSlot
+ 不同子窗口之间的通信
  + 自定义信号
  + 自定义槽函数
  + 链接信号与槽
  + 自定义发送信号函数

```python
from PyQt5.QtCore import pyqtSignal, QObject
import pandas as pd
class A(QObject):
    my = pyqtSignal(object)
    def __init__(self):
        super().__init__()
        self.my.connect(self.recv)
    def recv(self, df):
        print(df)
    def send(self):
      df = pd.read_excel(r'd:/fiber.xlsx', header=None,sheet_name="Sheet1")
      self.my.emit(df)
        
 if __name__ == '__main__':         
    a = A()
    a.send()
  ```
> 




## pyqt
ui文件 用 QFile加载
layout 窗口缩放 空间间距也跟着缩放 layout 可以嵌套
sizePolicy  控件缩放策略  fixed 固定的

先摆放控件->container->layout
调整layout内部控件比例 使用layoutStretch  调整间距 space
QProgressbar


pyInstaller 完成程序打包  程序运行中动态使用的外部文件需要复制到可执行文件得同一个目录下面 例如ui文件


# todo
+ navigate目前只能看fiber材料, 需要再增加一个按钮
