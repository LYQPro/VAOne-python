
import sys

from itertools import combinations

sys.path.append('d:/pythonproject')

from VAOne import *

import vvisualization.tools.glv_man as glvm

import vvisualization.read.trimlayer as makenct

# import importlib

# importlib.reload(makenct)  # 如果makenct中有全局变量db  因为__pycache__的存在, 如果不重新导入makenct中全局变量db的值还是上次运行的值


def multi_thickness_trim_create(mat, thicknesses):
    # 可以通过自定义thicknesses列表，创建相同材料不同厚度的trimlayer
    db = pi_fNeoDatabaseGetCurrent()
    air = makenct.Nct.convert(db, "Fluid", "Air", "Fluid")
    multi_thickness_trim = []
    if not thicknesses:
        return None
    for thickness in thicknesses:
        # name = pi_fMaterialGetCName(mat)
        trimobj = pi_fTrimLayerCreate(mat, thickness, air)
        multi_thickness_trim.append(trimobj)
    return multi_thickness_trim


def classify_trim(*trims) -> None:
    """
    将导入数据库的材料分为软层和硬层
    trim[0] fibers
    trim[1] foams
    trim[2] ....
    """
    sl = {}
    hl = {}
    for i in range(len(trims)):
        if trims[i].sl:
            sl.update(trims[i].sl)
        if trims[i].hl:
            hl.update(trims[i].hl)

    glvm.setv('softtrims', sl)  # 设置跨文件全局变量
    glvm.setv('hardtrims', hl)  # 设置跨文件全局变量


# softtrims 是一个字典变量{trim名称:trim对象地址}
# softtirms 储存在全局字典_dict中

def layeredtrim_create():
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


def softhardtrim_create():
    sl = glvm.getv('softtrims')  # 字典变量
    hl = glvm.getv('hardtrims')  # 字典变量
    db = pi_fNeoDatabaseGetCurrent()
    sh = {}
    for name1, trimobj1 in sl.items():
        for name2, trimobj2 in hl.items():
            layeredname = name1 + '+' + name2
            exist = pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)
            if exist is None:
                print(f'start creating {layeredname}')
                layeredtrim = pi_fLayeredTrimCreate(db, layeredname)
                pi_fLayeredTrimAddLayer(layeredtrim, trimobj2)
                pi_fLayeredTrimAddLayer(layeredtrim, trimobj1)
            else:
                print(f'already have {layeredname}')
                layeredtrim = pi_fConvertNeoPersistLayeredTrim(
                    pi_fConvertDBElementNeoPersist(pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)))
            sh[layeredname] = layeredtrim
    # glvm.getv('layeredtrim').update(sh)
    glvm.getv('layeredtrim')['softhardtrim'] = sh


def softevatrim_create():
    db = pi_fNeoDatabaseGetCurrent()
    sl = glvm.getv('softtrims')
    se = {}
    for name, trimobj in sl.items():
        eva = pi_fSeptumTrimLayerCreate(0.002, 3.6)  # 2mm 3.6kg/m2
        eva = pi_fConvertSeptumTrimLayerTrimLayer(eva)
        layeredname = name + '+' + 'eva'
        exist = pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)
        if exist is None:
            print(f'start creating {layeredname}')
            layeredtrim = pi_fLayeredTrimCreate(db, layeredname)
            pi_fLayeredTrimAddLayer(layeredtrim, trimobj)
            pi_fLayeredTrimAddLayer(layeredtrim, eva)
        else:
            print(f'already have {layeredname}')
            layeredtrim = pi_fConvertNeoPersistLayeredTrim(
                pi_fConvertDBElementNeoPersist(pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)))
        se[layeredname] = layeredtrim
    # glvm.getv('layeredtrim').update(se)
    glvm.getv('layeredtrim')['softevatrim'] = se


def solidsoftevatrim_create(thickness=0.0007,
                            softlayerthicknesses=None):
    # Steel -> trimlayer
    if softlayerthicknesses is None:
        softlayerthicknesses = [12.5, 14.96, 15.2, 18.06, 23.9, 27, 29.9, 3.1, 32.9, 36.1, 38.9, 42,
                                6.3, 8.96]
        softlayerthicknesses = [val / 1000 for val in softlayerthicknesses]
    db = pi_fNeoDatabaseGetCurrent()
    solidsofteva = {}
    sl = glvm.getv('softtrims')
    air = makenct.Nct.convert(db, "Fluid", "Air", "Fluid")
    fe = pi_fNeoDatabaseFindByName(db, pi_fIsotropicSolidGetClassID(), 'Steel')
    fe = pi_fConvertDBElementNeoPersist(fe)
    fe = pi_fConvertNeoPersistMaterial(fe)
    fe = pi_fTrimLayerCreate(fe, thickness, air)
    eva = pi_fSeptumTrimLayerCreate(0.002, 3.6)  # 2mm 3.6kg/m2
    eva = pi_fConvertSeptumTrimLayerTrimLayer(eva)
    for name, trimobj in sl.items():
        mat = pi_fTrimLayerGetMaterial(trimobj)
        multi = multi_thickness_trim_create(mat, softlayerthicknesses)
        multi.append(trimobj)
        softlayerthicknesses.append(round(pi_fTrimLayerGetThickness(trimobj), 2))
        for i in range(len(multi)):
            layeredname = str(thickness * 1000) + 'mm' + 'SteelPanel' + '+' + str(
                softlayerthicknesses[i] * 1000) + 'mm' + name + '+' + 'eva'
            exist = pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)
            if exist is None:
                print(f'start creating {layeredname}')
                layeredtrim = pi_fLayeredTrimCreate(db, layeredname)
                pi_fLayeredTrimAddLayer(layeredtrim, fe)

                # 添加不同厚度的薄层材料
                pi_fLayeredTrimAddLayer(layeredtrim, multi[i])

                pi_fLayeredTrimAddLayer(layeredtrim, eva)
            else:
                print(f'already have {layeredname}')
                layeredtrim = pi_fConvertNeoPersistLayeredTrim(
                    pi_fConvertDBElementNeoPersist(
                        pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)))
            solidsofteva[layeredname] = layeredtrim
    # glvm.getv('layeredtrim').update(solidsofteva)
    glvm.getv('layeredtrim')['solidsofteva'] = solidsofteva


def soft_create(thickness=0.023):
    """
    创建单轻层  比一般的softlayer要厚
    """
    db = pi_fNeoDatabaseGetCurrent()
    soft = {}
    sl = glvm.getv('softtrims')  # 如何修改厚度 需要重新创建trim_create函数
    air = makenct.Nct.convert(db, "Fluid", "Air", "Fluid")
    for name, trimobj in sl.items():
        layeredname = name
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
            layeredtrim = pi_fConvertNeoPersistLayeredTrim(
                pi_fConvertDBElementNeoPersist(pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)))
        soft[layeredname] = layeredtrim
    # glvm.getv('layeredtrim').update(soft)
    glvm.getv('layeredtrim')['soft'] = soft


def solid_create(thickness=0.0009, mat='Steel'):
    """
    单独的钢板铝板 大厚度
    """
    db = pi_fNeoDatabaseGetCurrent()
    panel = {}
    air = makenct.Nct.convert(db, "Fluid", "Air", "Fluid")
    isotropicsolid = pi_fConvertNeoPersistMaterial(
        pi_fConvertDBElementNeoPersist(pi_fNeoDatabaseFindByName(db, pi_fIsotropicSolidGetClassID(), mat)))
    trimlayer = pi_fTrimLayerCreate(isotropicsolid, thickness, air)
    layeredname = str(thickness * 1000) + 'mm' + mat + 'Panel'
    exist = pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)
    if exist is None:
        print(f'start creating {layeredname}')
        layeredtrim = pi_fLayeredTrimCreate(db, layeredname)
        pi_fLayeredTrimAddLayer(layeredtrim, trimlayer)
    else:
        print(f'already have {layeredname}')
        layeredtrim = pi_fConvertNeoPersistLayeredTrim(
            pi_fConvertDBElementNeoPersist(pi_fNeoDatabaseFindByName(db, pi_fLayeredTrimGetClassID(), layeredname)))
    panel[layeredname] = layeredtrim
    # glvm.getv('layeredtrim').update(panel)
    glvm.getv('layeredtrim')['solid'] = panel

    """
    其他功能函数请在这里添加
    """


def MNCT_create(layeredtrim_name='solidsofteva', distribution={}):  # distribution 覆盖率字典
    """
    use layeredtrim create MNCT
    通过layeredtrim_name参数自定义创建mnct的layeredtrim. 默认使用 steel + softlayer + eva 创建 mnct
    这部分比较灵活，可以多层叠加，可以通过自定义distribution来修改各部分创建时候的覆盖率（不建议） 目前这部分还没有完善
    因为可以在optimization模块优化各部分覆盖率, 所以在在创建的时候分配覆盖率意义不大
    这里的MNCT均加入了一块0.9mm reinforced Steel panel 覆盖率为20%
    """
    db = pi_fNeoDatabaseGetCurrent()
    layeredtrim = glvm.getv('layeredtrim')[layeredtrim_name]  # layer-ups
    try:
        if not distribution:  # 没有指定方案，则平均分配
            if not layeredtrim:
                return None
            mptrim_name = 'mnct_' + layeredtrim_name
            exist = pi_fNeoDatabaseFindByName(db, pi_fMultipleTrimGetClassID(), mptrim_name)
            if exist is None:
                layeredtrim_num = len(layeredtrim)  # layerup 的种类数
                mptrim = pi_fMultipleTrimCreate(db, mptrim_name)
                coverage = 0.8 / layeredtrim_num
                for layeredtrimobj in layeredtrim.values():
                    temp_layeredtrimobj = pi_fConvertLayeredTrimTrim(layeredtrimobj)
                    pi_fMultipleTrimAddTrim(mptrim, temp_layeredtrimobj, coverage)
                solid_create(0.0009, 'Steel')
                steel = glvm.getv('layeredtrim')['solid']['0.9mmSteelPanel']
                temp_steel = pi_fConvertLayeredTrimTrim(steel)
                pi_fMultipleTrimAddTrim(mptrim, temp_steel, 0.2)
            else:
                print(f'already have {mptrim_name}')
                mptrim = pi_fConvertNeoPersistMultipleTrim(
                    pi_fConvertDBElementNeoPersist(
                        pi_fNeoDatabaseFindByName(db, pi_fMultipleTrimGetClassID(), mptrim_name)))
            glvm.getv('mnct')[mptrim_name] = mptrim
        else:
            # todo
            pass
    except:
        # todo
        # print('problem encounter while creating multipletrim')
        raise


if __name__ == '__main__':
    loc1 = r'd:/fiber.xlsx'
    loc2 = r'd:/foam.xlsx'
    try:
        db = pi_fNeoDatabaseGetCurrent()
        fibers = makenct.Fiber(db, loc1)  # 导入fibers数据库对象的集合  使用的是glvc配置的db对象
        foams = makenct.Foam(db, loc2)  # 导入foam数据库对象的集合

        classify_trim(fibers, foams)  # 材料按软硬层分类 导入全局变量备用
        softhardtrim_create()
        softevatrim_create()
        solidsoftevatrim_create(0.0007)  # 7mm钢板
        soft_create(0.023)  # 23mm轻层材料
        solid_create(0.0008)
        MNCT_create()

        # 检测全局字典工作是否正常
        temp = glvm.getv('layeredtrim')
        for item in temp.items():
            print(item)

        temp = glvm.getv('mnct')
        if temp is not None:
            for item in temp.items():
                print(temp)

        print('ok')

    except:
        if pi_fIsInit():
            db = pi_fNeoDatabaseGetCurrent()
            if pi_fNeoDatabaseIsOpen(db):
                pi_fNeoDatabaseClose(db)
                pi_fNeoDatabaseDispose(db)
        raise
