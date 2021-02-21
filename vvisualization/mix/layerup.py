import sys

from typing import List, Optional, Tuple, Dict

sys.path.append('d:/pythonproject')

from VAOne import *

import vvisualization.tools.glv_man as glvm

import vvisualization.read.trimlayer as makenct


# import importlib

# importlib.reload(makenct)

def trimLayerThicknessMultiply(mat, thicknesses):
    """
    可以通过自定义thicknesses列表，创建相同材料不同厚度的trimlayer
    @param mat: CMaterial*
    @type thicknesses: list or None
    @rtype: list

    """
    db = pi_fNeoDatabaseGetCurrent()
    air = makenct.Nct.convert(db, "Fluid", "Air", "Fluid")
    multi_thickness_trimlayer = []
    if not thicknesses:
        return []
    for thickness in thicknesses:
        trimobj = pi_fTrimLayerCreate(mat, thickness, air)
        multi_thickness_trimlayer.append(trimobj)
    return multi_thickness_trimlayer


def trimLayerClassify(*trims: Tuple[Dict, Dict]) -> None:
    """
    将导入数据库的材料分为软层和硬层
    trim[0] fibers
    trim[1] foams
    trim[2] ....
    """
    sl = {}
    hl = {}
    for i in range(len(trims)):
        if trims[i][0]:
            sl.update(trims[i][0])
        if trims[i][0]:
            hl.update(trims[i][1])

    glvm.setv('softtrims', sl)  # 设置跨文件全局变量
    glvm.setv('hardtrims', hl)  # 设置跨文件全局变量


def layerUp():
    """
    use trim create 3 types layered trim
    1) 1 softlayer + 1 hardlayer
    2) 1 softlayer + 1 EVA
    3）0.9mm/0.7mm Al + 1 softlayer + 1 EVA
    4) 1 softlayer
    5) 1 0.9mm steel
        ........... continue
    """
    pass


def softHardLayerUp(thicknesses: Optional[List[float]] = None) -> Dict:
    """
    soft + hard
    @param thicknesses: list or None
    @return: None
    """
    sl = glvm.getv('softtrims')  # 字典变量
    hl = glvm.getv('hardtrims')  # 字典变量
    db = pi_fNeoDatabaseGetCurrent()
    sh = {}
    for name1, trimobj1 in sl.items():
        mptrimlayers = trimLayerThicknessMultiply(pi_fTrimLayerGetMaterial(trimobj1), thicknesses)
        mptrimlayers.append(trimobj1)
        for elem in mptrimlayers:
            for name2, trimobj2 in hl.items():
                layeredname = str(round(pi_fTrimLayerGetThickness(elem) * 1000, 2)) + 'mm' + name1 + '+' + name2
                exist = pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)
                if exist is None:
                    print(f'start creating {layeredname}')
                    layeredtrim = pi_fLayeredTrimCreate(db, layeredname)
                    pi_fLayeredTrimAddLayer(layeredtrim, elem)
                    pi_fLayeredTrimAddLayer(layeredtrim, trimobj2)
                else:
                    print(f'already have {layeredname}')
                    layeredtrim = makenct.Nct.convert(db, 'LayeredTrim', layeredname, 'LayeredTrim')
                sh[layeredname] = layeredtrim
    glvm.getv('layeredtrim').update(sh)
    return sh


def softEvaLayerUp(thicknesses: Optional[List[float]] = None) -> Dict:
    """
    soft + EVA
    @param thicknesses: list or None
    @return: None
    """
    db = pi_fNeoDatabaseGetCurrent()
    sl = glvm.getv('softtrims')
    se = {}
    eva = pi_fConvertSeptumTrimLayerTrimLayer(pi_fSeptumTrimLayerCreate(0.002, 3.6))  # 2mm 3.6kg/m2
    for name, trimobj in sl.items():
        mptrimlayers = trimLayerThicknessMultiply(pi_fTrimLayerGetMaterial(trimobj), thicknesses)
        mptrimlayers.append(trimobj)
        for elem in mptrimlayers:
            layeredname = str(round(pi_fTrimLayerGetThickness(elem) * 1000, 2)) + 'mm' + name + '+' + 'EVA'
            exist = pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)
            if exist is None:
                print(f'start creating {layeredname}')
                layeredtrim = pi_fLayeredTrimCreate(db, layeredname)
                pi_fLayeredTrimAddLayer(layeredtrim, elem)
                pi_fLayeredTrimAddLayer(layeredtrim, eva)
            else:
                print(f'already have {layeredname}')
                layeredtrim = makenct.Nct.convert(db, 'LayeredTrim', layeredname, 'LayeredTrim')
            se[layeredname] = layeredtrim
    glvm.getv('layeredtrim').update(se)
    return se


def solidSoftEvaLayerUp(solidthickness=0.0007, softlayerthicknesses=None) -> Dict:
    """
    Steel + soft + EVA
    @param solidthickness: float
    @param softlayerthicknesses: list
    @return: None
    """
    db = pi_fNeoDatabaseGetCurrent()
    air = makenct.Nct.convert(db, "Fluid", "Air", "Fluid")
    sse = {}
    sl = glvm.getv('softtrims')
    solid = pi_fTrimLayerCreate(makenct.Nct.convert(db, 'IsotropicSolid', 'Steel', 'Material'), solidthickness, air)
    eva = pi_fConvertSeptumTrimLayerTrimLayer(pi_fSeptumTrimLayerCreate(0.002, 3.6))  # 2mm 3.6kg/m2
    for name, trimobj in sl.items():
        mptrimlayers = trimLayerThicknessMultiply(pi_fTrimLayerGetMaterial(trimobj), softlayerthicknesses)
        mptrimlayers.append(trimobj)
        for elem in mptrimlayers:
            layeredname = str(round(solidthickness * 1000, 2)) + 'mm' + 'SteelPanel' + '+' + str(
                round(pi_fTrimLayerGetThickness(elem) * 1000, 2)) + 'mm' + name + '+' + 'EVA'
            exist = pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)
            if exist is None:
                print(f'start creating {layeredname}')
                layeredtrim = pi_fLayeredTrimCreate(db, layeredname)
                pi_fLayeredTrimAddLayer(layeredtrim, solid)
                pi_fLayeredTrimAddLayer(layeredtrim, elem)
                pi_fLayeredTrimAddLayer(layeredtrim, eva)
            else:
                print(f'already have {layeredname}')
                layeredtrim = makenct.Nct.convert(db, 'LayeredTrim', layeredname, 'LayeredTrim')
            sse[layeredname] = layeredtrim
    glvm.getv('layeredtrim').update(sse)
    return sse


def softLayerUP(thickness=0.023):
    """
    创建单轻层  比一般的softlayer要厚
    @type thickness: float
    """
    db = pi_fNeoDatabaseGetCurrent()
    soft = {}
    sl = glvm.getv('softtrims')  # 如何修改厚度 需要重新创建trim_create函数
    air = makenct.Nct.convert(db, "Fluid", "Air", "Fluid")
    for name, trimobj in sl.items():
        layeredname = str(round(thickness * 1000, 2)) + 'mm' + name
        exist = pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)
        if exist is None:
            print(f'start creating {layeredname}')
            # 创建trimlayer
            mat = pi_fTrimLayerGetMaterial(trimobj)
            trimobj = pi_fTrimLayerCreate(mat, thickness, air)
            layeredtrim = pi_fLayeredTrimCreate(db, layeredname)
            pi_fLayeredTrimAddLayer(layeredtrim, trimobj)
        else:
            print(f'already have {layeredname}')
            layeredtrim = makenct.Nct.convert(db, 'LayeredTrim', layeredname, 'LayeredTrim')
        soft[layeredname] = layeredtrim
    glvm.getv('layeredtrim').update(soft)
    return soft


def solidLayerUp(thickness=0.0009, mat='Steel'):
    """
    单独的钢板铝板 大厚度
    @param mat: str
    @type thickness: float
    """
    db = pi_fNeoDatabaseGetCurrent()
    panel = {}
    air = makenct.Nct.convert(db, "Fluid", "Air", "Fluid")
    trimlayer = pi_fTrimLayerCreate(makenct.Nct.convert(db, 'IsotropicSolid', mat, 'Material'), thickness, air)
    layeredname = str(round(thickness * 1000, 2)) + 'mm' + mat + 'Panel'
    exist = pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)
    if exist is None:
        print(f'start creating {layeredname}')
        layeredtrim = pi_fLayeredTrimCreate(db, layeredname)
        pi_fLayeredTrimAddLayer(layeredtrim, trimlayer)
    else:
        print(f'already have {layeredname}')
        layeredtrim = makenct.Nct.convert(db, 'LayeredTrim', layeredname, 'LayeredTrim')
    panel[layeredname] = layeredtrim
    glvm.getv('layeredtrim').update(panel)
    return panel


def MultipleNoiseControlTreatment(name, layerupdict, distribution: Optional[Dict] = None):
    """
    use layeredtrim create MNCT
    通过layeredtrim_name参数自定义创建mnct的layeredtrim. 默认使用 steel + softlayer + eva 创建 mnct
    这部分比较灵活，可以多层叠加，可以通过自定义distribution来修改各部分创建时候的覆盖率（不建议） 目前这部分还没有完善
    因为可以在optimization模块优化各部分覆盖率, 所以在在创建的时候分配覆盖率意义不大
    这里的MNCT均加入了一块0.9mm reinforced Steel panel 覆盖率为20%
    @param name: str
    @param layerupdict: list
    @type distribution: dict
    """
    NUM_LAYUP = 5
    db = pi_fNeoDatabaseGetCurrent()
    layerups = layerupdict
    mptrim = pi_fMultipleTrimCreate(db, name)
    if distribution is None:
        # todo 一类layeredtrim中(<=5)个layup进行组合
        temp = list(layerups.values())
        for elem in temp[:NUM_LAYUP]:
            pi_fMultipleTrimAddTrim(mptrim, pi_fConvertLayeredTrimTrim(elem), 0.8/NUM_LAYUP)
    else:
        # 按照distribution中的layerup和coverage创建mnct
        try:
            for item in distribution.items():
                layeredtrim = glvm.getv('layeredtrim')
                pi_fMultipleTrimAddTrim(mptrim, pi_fConvertLayeredTrimTrim(layeredtrim[item[0]]), item[1])
        except KeyError:
            print('some layerup does not exist while creating mnct')
    panel = solidLayerUp(0.0009)
    pi_fMultipleTrimAddTrim(mptrim, pi_fConvertLayeredTrimTrim(panel['0.9mmSteelPanel']), 0.2)
    glvm.getv('mnct').update({name: mptrim})


if __name__ == '__main__':
    loc1 = r'd:/fiber.xlsx'
    loc2 = r'd:/foam.xlsx'
    try:
        db1 = pi_fNeoDatabaseGetCurrent()
        fibers = makenct.Fiber(db1, loc1)  # 导入fibers数据库对象的集合  使用的是glvc配置的db对象
        fiberTrimLayers = fibers.trimLayerCreate(0.02)
        foams = makenct.Foam(db1, loc2)  # 导入foam数据库对象的集合
        foamTrimLayers = foams.trimLayerCreate(0.035, 0.002)
        trimLayerClassify(fiberTrimLayers, foamTrimLayers)  # 材料按软硬层分类 导入全局变量备用
        softHardLayerUp([0.01, 0.02, 0.03])
        softEvaLayerUp([0.005, 0.0075])
        solidSoftEvaLayerUp(0.0007)  # solid层采用7mm钢板
        softLayerUP(0.023)  # 23mm轻层材料
        solidLayerUp(0.0008)
        MultipleNoiseControlTreatment(
            'mnct1', solidSoftEvaLayerUp(0.0007, [0.01, 0.02, 0.03]), {'0.8mmSteelPanel': 0.8})

        # 检测全局字典工作是否正常
        # temp = glvm.getv('layeredtrim')
        # for item in temp.items():
        #     print(item)
        #
        # temp = glvm.getv('mnct')
        # if temp is not None:
        #     for item in temp.items():
        #         print(temp)

        print('ok')

    except:
        if pi_fIsInit():
            db1 = pi_fNeoDatabaseGetCurrent()
            if pi_fNeoDatabaseIsOpen(db1):
                pi_fNeoDatabaseClose(db1)
                pi_fNeoDatabaseDispose(db1)
        raise
