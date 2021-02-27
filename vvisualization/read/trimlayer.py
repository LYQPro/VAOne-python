from abc import abstractmethod
from VAOne import *
import pandas as pd
import sys
# sys.path.append(r'd:/pythonproject') # 如果直接以脚本运行此文件(top-level)需要将根包所在位置加入sys.path
from typing import List, Any , Tuple , Dict
import traceback






"""声学包抽象类"""


class Nct(object):

    def __init__(self, db, loc):
        # 基本信息
        self.type = 'Nct'
        self.loc = loc
        self.db = db
        # 材料信息
        self.df = self.read()["SoftLayer1 HardLayer2"]  # 记录软硬层分类信息
        self.mat = self.create()
        # trimlayer厚度信息
        self.thickness = [None, None]  # [softTrimlayer厚度, 硬层hardTrimlayer厚度]

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def create(self):
        pass

    @staticmethod
    def convert(db, oldtype, name, newtype):
        origin = pi_fNeoDatabaseFindByName(db , globals()["pi_f" + oldtype + "GetClassID"](), name)
        return globals()["pi_fConvertNeoPersist" + newtype]((pi_fConvertDBElementNeoPersist(origin)))

    def trimLayerCreate(self, softlayerthickness=0.01, hardlayerthickness=0.003) -> Tuple[Dict, Dict]:  # 用户输入
        """
        use material create trimlayer
        """
        soft_layer = {}
        hard_layer = {}
        air = Nct.convert(self.db, "Fluid", "Air", "Fluid")
        for i in range(len(self.mat)):
            temp = Nct.convert(self.db, self.type, self.df.index[i], "Material")
            if self.df[i] == 1:
                layer = pi_fTrimLayerCreate(temp, softlayerthickness, air)
                self.thickness[0] = softlayerthickness
                soft_layer[self.df.index[i]] = layer
            if self.df[i] == 2:
                layer = pi_fTrimLayerCreate(temp, hardlayerthickness, air)
                self.thickness[1] = hardlayerthickness
                hard_layer[self.df.index[i]] = layer
        return (soft_layer, hard_layer)


class Fiber(Nct):
    def __init__(self, db, loc):
        super().__init__(db, loc)
        self.type = 'Fiber'

    def read(self) -> pd.DataFrame:
        """
        读入Fiber excel文件
        """
        df = pd.read_excel(self.loc, header=None, sheet_name="Sheet1")  # 路径改为接受用户输入或用户选择文件 !!!

        df.columns = ["Name", "Density", "Flow Resistivity", "Porosity",
                      "Tortuosity", "ViscousLength", "ThermalLength",
                      "SoftLayer1 HardLayer2"]  # 输入文件各列格式 最后一列表明软层1还是硬层2
        df.index = df["Name"]
        df = df.sort_values(by=["SoftLayer1 HardLayer2"])  # 软层排在前 硬层排在后
        # print(df)
        print("import Excel done...")
        return df

    def create(self) -> List[Any]:
        """
        create fiber material
        """
        df = self.read()
        mat = []
        for name in df.index:
            fiber = pi_fNeoDatabaseFindByName(self.db, pi_fFiberGetClassID(), name)
            if fiber is None:
                print("start creating material")
                fiber = pi_fFiberCreate(self.db, name, float(
                    df["Flow Resistivity"][name]), float(df["Density"][name]))
                pi_fFiberSetPorosity(fiber, float(df["Porosity"][name]))
                pi_fFiberSetTortuosity(fiber, float(df["Tortuosity"][name]))
                pi_fFiberSetViscousLength(fiber, float(df["ViscousLength"][name]))
                pi_fFiberSetThermalLength(fiber, float(df["ThermalLength"][name]))
            else:
                fiber = Nct.convert(self.db, 'Fiber',name,'Fiber')
                print("already have {}".format(name))
            mat.append(fiber)
        return mat


class Foam(Nct):
    def __init__(self, db, loc):
        super().__init__(db, loc)
        self.type = 'Foam'

    def read(self) -> pd.DataFrame:
        """ 
        读入Foam excel文件
        """
        df = pd.read_excel(self.loc, header=None,
                           sheet_name="Sheet1")  # 路径改为接受用户输入或用户选择文件 !!!

        df.columns = ["Name", "Density", "Flow Resistivity", "Porosity",
                      "Tortuosity", "ViscousLength", "ThermalLength", "DLF", "Young's Modulus", "Poisson's Ratio",
                      "SoftLayer1 HardLayer2"]  # 输入文件各列格式 最后一列表明软层1还是硬层2
        df.index = df["Name"]
        df = df.sort_values(by=["SoftLayer1 HardLayer2"])  # 软层排在前 硬层排在后
        # print(df)
        print("import Excel done...")
        return df

    def create(self) -> List[Any]:
        """
        create foam material
        """
        df = self.read()
        mat = []
        for name in df.index:
            foam = pi_fNeoDatabaseFindByName(self.db, pi_fFoamGetClassID(), name)
            if foam is None:
                print("start creating material")
                foam = pi_fFoamCreate2(self.db, name, float(df["Density"][name]),
                                       float(df["Young's Modulus"][name]),
                                       float(df["Young's Modulus"][name]) / (2 * (1 + df["Poisson's Ratio"][name])),
                                       float(df["Poisson's Ratio"][name]), float(df["DLF"][name]),
                                       float(df["Porosity"][name]), float(df["Tortuosity"][name]),
                                       float(df["Flow Resistivity"][name]), float(df["ViscousLength"][name]),
                                       float(df["ThermalLength"][name]))
            else:
                foam = Nct.convert(self.db, 'Foam', name, 'Foam')
                print("already have {}".format(name))
            mat.append(foam)
        return mat


class isotropicsolid(Nct):

    def __init__(self, loc):
        super().__init__(loc)

    def read(self):
        pass

    def create(self):
        pass


if __name__ == '__main__':
    loc1 = r'd:/fiber.xlsx'
    loc2 = r'd:/foam.xlsx'
    try:
        db = pi_fNeoDatabaseGetCurrent()
        fibers = Fiber(db, loc1)
        # print(fibers.trimLayerCreate(0.02))
        foams = Foam(db, loc2)
        foams.trimLayerCreate(0.015, 0.002)
    except:
        if pi_fIsInit():
            db = pi_fNeoDatabaseGetCurrent()
        if pi_fNeoDatabaseIsOpen(db):
            pi_fNeoDatabaseClose(db)
            pi_fNeoDatabaseDispose(db)
        raise
