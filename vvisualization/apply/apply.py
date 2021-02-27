# 本文件是函数的集合
# 选取需要添加声学包的表面和添加的声学包
# 使用本脚本前应该在GUI界面选中plate对象       目前仅支持plate对象apply声学包
# num = GUI_GetSelected(index) -> int
# 找到plate类的迭代器iterator  iterator = pi_fNamedDBElementGetIterator(db, pi_fPlateGetClassId(), forward)
# 迭代
# obj = pi_fIteratorGetcurrent(iterator) -> CNeoPersist*
# 判断条件int(obj) == num  若True则obj为当前选中的那个物体的引用
#
from typing import List, Any, Tuple
from VAOne import *
import VAOneGUI as vagui
import sys

sys.path.append('d:/pythonproject')
from vvisualization.read.trimlayer import Fiber, Foam
from vvisualization.mix.layerup import solidSoftEvaLayerUp, trimLayerClassify
import win32com.client
import time

# todo
sys.path.append('d:/pythonproject')
from vvisualization.tools import glv_man as glvm
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets

ESCAPE_NUM = 666


class AskTrimIndex(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ipt = QtWidgets.QLineEdit()
        self.btn = QtWidgets.QPushButton('确定', self)
        self.setupUi()
        self.btn.clicked.connect(self.on_btn_clicked)

    def setupUi(self):
        vbl = QtWidgets.QVBoxLayout(self)
        vbl.addWidget(self.ipt)
        vbl.addWidget(self.btn)

    def getVal(self):
        return self.ipt.text()

    def accept(self) -> None:
        pass

    def on_btn_clicked(self):
        if GetSelectedPlate() or (self.getVal() == str(ESCAPE_NUM)):
            time.sleep(0.1)
            self.close()
        else:
            QtWidgets.QMessageBox.information(self, '消息', '先选择下一批plate！！')


def GetSelectedPlate():
    """
    返回3D窗口中选中的Plate
    返回形式list((plateName, plate_obj))
    """
    selected_plate_num = vagui.GUI_GetSelectionCount()
    if selected_plate_num < 1:
        print('select at least 1 plate before bush this button!!!')
    else:
        reference = []
        platelist: List[int] = []
        selectedplatelist: List[Tuple[Any, Any]] = []
        db = pi_fNeoDatabaseGetCurrent()
        # 搜索数据库中的所有Plate
        iterator = pi_fIteratorCreate(db, pi_fPlateGetClassID(), 1)
        while pi_fIteratorCurrent(iterator) is not None:
            # 此处千万不能使用reference = pi_fIteratorCurrent(iterator)
            # 千万不能产生左值!!!!!!!!!!!!! 赋值运算将会产生左值
            # 左值将会隐式改变数据库的结构!!!!!!!!!在iterator存在,不能改变数据库结构,必须报指针释放后才能改变数据库的结构
            reference.append(pi_fIteratorCurrent(iterator))
            platelist.append(int(pi_fIteratorCurrent(iterator)))
            # print(reference[-1], ' ', platelist[-1])
            pi_fIteratorNext(iterator)

        pi_fIteratorDispose(iterator)  # 不能重复释放迭代器 pi_fIteratorDelete()没有必要使用,也不能使用

        for index in range(selected_plate_num):
            ad = vagui.GUI_GetSelected(index)
            # print(ad)
            if ad in platelist:
                plate = reference[platelist.index(ad)]
                plate = pi_fConvertNeoPersistPlate(plate)
                plate_name = pi_fPlateGetCName(plate)
                selectedplatelist.append((plate_name, plate))
        return selectedplatelist


def trimPlate(plates, reverse):  # generator
    """
    平板上加装声学包
    平板：传入的参数
    声学包：layerups or mnct 在glvm中
    @param plates: list(tuple(any, any))
    @param reverse: 0正(A)面 1背(B)面
    """
    trim = 'init'
    while True:
        trim = yield trim
        if trim is None:
            break

        try:
            temp_trim = pi_fConvertLayeredTrimTrim(trim)
        except TypeError:
            temp_trim = pi_fConvertMultipleTrimTrim(trim)
        except:
            raise

        for plate in plates:
            if reverse:
                pi_fPlateSetTrimB(plate[1], temp_trim)
            else:
                pi_fPlateSetTrimA(plate[1], temp_trim)

        # todo 求解函数
    return trim


def trimPlateProxy(platelist, reverse):
    while True:
        trim = yield from trimPlate(platelist, reverse)
        if trim is None:
            break
        try:
            trimname = pi_fLayeredTrimGetCName(trim)  # 传入None将会引发不可恢复的错误,传入其他错误参数将会引发TypeError
        except TypeError:
            trimname = pi_fMultipleTrimGetCName(trim)
        except:
            raise
        print(f'have applied {trimname} to selected plates')


def trimPlateCaller(trims, reverse=1) -> bool:
    """
    @type trims: dict
    @param reverse: int {0,1}
    """
    names = list(trims.keys())
    trims = list(trims.values())
    if not trims:
        return False
    speaker = win32com.client.Dispatch("SAPI.SpVoice")  # 系统语音
    speaker.Speak(f'请先在3D界面选择平板,然后在对话框输入一个整数，这个整数代表了你选择的声学包, 输入{ESCAPE_NUM}退出')

    generator = None

    # 用户输入准备工作
    print(f'\n\n\n\ninput a int [1..{len(trims)}] to specify a trim that you want to apply\n'
          'the int is the index of the specified trim in trims you pass in\n'
          f'enter {ESCAPE_NUM} to escape\n\n')

    for i in range(len(names)):
        print(f'{i + 1} : {names[i]}')

    while True:  # 用户apply声学包循环, 输入ESCAPE_NUM退出

        num = ESCAPE_NUM
        while True:
            try:
                # 用户输入/ 获取输入
                myDialog = AskTrimIndex()
                myDialog.exec_()
                num = myDialog.getVal()

                num = int(num)
                if (len(trims) >= num > 0) or (num == ESCAPE_NUM):
                    break
                else:
                    print(f'int out of range, expect int ranging from 1 to {len(trims)}')
            except ValueError:
                print('please input a integer')
                continue
            except:
                raise

        # 输入ESCAPE_NUM退出循环
        if num == ESCAPE_NUM:
            break

        # 获取选中的平板信息
        generator = trimPlateProxy(GetSelectedPlate(), reverse)
        next(generator)
        # 装饰平板
        generator.send(trims[num - 1])
        print(f'have applied {names[num - 1]} to selected plates')

    # 结束生成器
    # generator.send(None)

    return True


def randomTrimPlateCaller():
    # 按照以下格式写都可以

    # 确定有平板选中
    # generator = trimPlateProxy(GetSelectedPlate(), 1)
    # next(generator)
    # 任意个generator.send()
    # generator.send(None) 终止
    pass


if __name__ == '__main__':
    loc1 = r'd:/fiber.xlsx'
    loc2 = r'd:/foam.xlsx'
    try:

        db = pi_fNeoDatabaseGetCurrent()
        temp = GetSelectedPlate()
        print(temp)
        fibers = Fiber(db, loc1)
        foams = Foam(db, loc2)
        trimLayerClassify(fibers.trimLayerCreate(), foams.trimLayerCreate())
        solidSoftEvaLayerUp(0.007, [0.01, 0.02])
        layerups = glvm.getv('layeredtrim')
        if trimPlateCaller(layerups, 0):
            print('ok')
        else:
            print('not ok')

    except:
        raise
