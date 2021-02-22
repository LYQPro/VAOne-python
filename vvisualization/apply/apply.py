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


# todo
sys.path.append('d:/pythonproject')
from vvisualization.tools import glv_man as glvm


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
            continue
        try:
            trimname = pi_fLayeredTrimGetCName(trim)
        except TypeError:
            trimname = pi_fMultipleTrimGetCName(trim)
        except:
            raise
        print(f'have applied {trimname} to selected plates')


def trimPlateCaller(trims, reverse):
    """
    @param reverse: int {0,1}
    @type trims: dict
    """
    trims = list(trims.values())
    # 实例化生成器
    if GetSelectedPlate():
        generator = trimPlateProxy(GetSelectedPlate(), reverse)
        # 初始化生成器
        next(generator)
        generator.send(trims[1])
        # todo
        # 在这中间可以在3D窗口中重新选择plate
        #
        generator.send(trims[0])
        # 结束生成器
        generator.send(None)
        return True
    else:
        print('select at least one plate')
        return False


if __name__ == '__main__':
    loc1 = r'd:/fiber.xlsx'
    loc2 = r'd:/foam.xlsx'
    try:
        db = pi_fNeoDatabaseGetCurrent()
        # temp = GetSelectedPlate()
        # print(temp)
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
