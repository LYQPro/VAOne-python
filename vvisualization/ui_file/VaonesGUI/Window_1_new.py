import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, QDir, QAbstractTableModel, Qt
from Ui_VMainWindow_new import Ui_MainWindow
import pandas as pd
from Ui_TableView import Ui_Form
import importlib
import time

sys.path.append('d:/pythonproject')
import vvisualization.tools.glv_config as glvc
from vvisualization.read.trimlayer import Fiber, Foam
from vvisualization.mix.layerup import *
from vvisualization.apply.apply import GetSelectedPlate, trimPlateCaller, randomTrimPlateCaller

importlib.reload(glvc)


def is_number(num: str):
    """
    如果是数字返回转化后的值，如果不是数字返回false
    @param num:
    @return:
    """
    try:
        num = float(num)
    except ValueError:
        return False
    return True


class MainWindow(QMainWindow):
    # 自定义信号
    sig1 = pyqtSignal(object, name='loadfiber')
    sig2 = pyqtSignal(object, name='loadfoam')
    sig3 = pyqtSignal(object, name='param_fiber')
    sig4 = pyqtSignal(object, name='param_foam')
    sig5 = pyqtSignal(object, name='layup_make')
    sig6 = pyqtSignal(object, name='mnct_make')

    # 保存的材料信息
    df_fiber = pd.DataFrame()
    df_foam = pd.DataFrame()

    layups = {"soft and hard-layer": {}, "soft-layer and Eva": {}, "steel and soft-layer and Eva": {},
              "thick soft-layer": {}, "thick isotropic solid": {}}

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 连接信号与槽
        # self.ui.LoadFoam_pushButton.clicked.connect(self.preprocess_input)
        # self.sig2.connect(self.datanavigate)
        self.ui.LoadFiber_pushButton.clicked.connect(self.preprocess_input)
        self.sig3.connect(self.loadfiber)
        self.ui.LoadFoam_pushButton.clicked.connect(self.preprocess_input)
        self.sig4.connect(self.loadfoam)
        self.ui.Navigate_pushButton.clicked.connect(self.dataNavigate)
        self.ui.navigate_pushButton.clicked.connect(self.datanavigate)
        self.ui.SumApply_pushButton.clicked.connect(self.apply)
        self.ui.TLayUpsApply_pushButton.clicked.connect(self.preprocess_input)
        self.sig5.connect(self.make_layup)
        self.ui.MultipleNCTApply_pushButton.clicked.connect(self.preprocess_input)
        self.sig6.connect(self.make_mnct)
        self.sig1.connect(self.updatefiber)
        self.sig2.connect(self.updatefoam)
        self.ui.SumApply_pushButton.clicked.connect(self.apply)

    # 槽函数 LoadFiber_pushButton
    def loadfiber(self, param):  # 如果关闭会重复触发
        dlg_fiber = QFileDialog(parent=self)
        dlg_fiber.setFileMode(QFileDialog.AnyFile)
        dlg_fiber.setFilter(QDir.Files)
        # fibers = None
        if dlg_fiber.exec_():
            fiber_filenames = dlg_fiber.selectedFiles()  # FiberFilenames 文件的绝对路径
            print(fiber_filenames)
            db = pi_fNeoDatabaseGetCurrent()
            try:
                fibers = Fiber(db, fiber_filenames[0])
                # 导入材料的时候如果厚度输入框有数字就按照当时的厚度数值创建trimlayer
                # 如果没有数值就用默认厚度创建trimlayer
                st = 0.01
                ht = 0.003
                # print(param)
                if param['soft_t']:
                    st = param['soft_t'][0]
                    # print(st)
                if param['hard_t'] > 0:
                    ht = param['hard_t']

                # 分类并存入全局变量
                trimLayerClassify(fibers.trimLayerCreate(softlayerthickness=st, hardlayerthickness=ht))

                # 发出信号更新self.df_fiber
                self.sig1.emit(fibers.read())
            except:
                print('maybe file format error')
                raise
        # return fibers

    # 槽函数 LoadFoam_pushButton
    def loadfoam(self, param):
        dlg_foam = QFileDialog(parent=self)
        dlg_foam.setFileMode(QFileDialog.AnyFile)
        dlg_foam.setFilter(QDir.Files)
        # foams = None
        if dlg_foam.exec_():
            foam_filenames = dlg_foam.selectedFiles()  # FoamFilenames 文件的绝对路径
            print(foam_filenames)
            db = pi_fNeoDatabaseGetCurrent()
            try:
                # 导入数据
                foams = Foam(db, foam_filenames[0])
                # print(param)
                st = 0.01
                ht = 0.003
                if param['soft_t']:
                    st = param['soft_t'][0]
                if param['hard_t'] > 0:
                    ht = param['hard_t']
                # 分类并存入全局变量
                trimLayerClassify(foams.trimLayerCreate(softlayerthickness=st, hardlayerthickness=ht))
                self.sig2.emit(foams.read())
            except:
                print('maybe file format error')
                raise
        # return foams

    # 槽函数 Navigate_pushButton
    def dataNavigate(self):
        self.view = TableView()
        model = PandasModel(self.df_fiber)
        self.view.DtableView.setModel(model)
        self.view.DtableView.resize(1500, 600)
        # self.view.DtableView.adjustSize()
        self.view.show()

    def datanavigate(self):
        self.view = TableView()
        model = PandasModel(self.df_foam)
        self.view.DtableView.setModel(model)
        self.view.DtableView.resize(1500, 600)
        self.view.show()

    def apply(self):
        if glvm.getv('layeredtrim'):
            trimPlateCaller(glvm.getv('layeredtrim'), reverse=1)
        else:
            QMessageBox.information(self, '提示', '还没有生成任何声学包')

    def make_layup(self, param):
        option = self.layer_up_option()
        # 确定参数的合法性 如何在参数不合法的情况下，正确使用缺省参数
        if option == "soft and hard-layer":
            self.layups['soft and hard-layer'].update(softHardLayerUp(param['soft_t']))
        elif option == "soft-layer and Eva":
            self.layups['soft-layer and Eva'].update(softEvaLayerUp(param['soft_t']))
        elif option == "steel and soft-layer and Eva":
            if param['solid_t'] > 0:
                self.layups['steel and soft-layer and Eva'].update(
                    solidSoftEvaLayerUp(param['solid_t'], param['soft_t']))
            else:
                self.layups['steel and soft-layer and Eva'].update(
                    solidSoftEvaLayerUp(softlayerthicknesses=param['soft_t']))
        elif option == "thick soft-layer":
            if param['tsoft_t'] > 0:
                self.layups['thick soft-layer'].update(softLayerUP(param['tsoft_t']))
            else:
                self.layups['thick soft-layer'].update(softLayerUP())
        else:
            if param['solid_t'] > 0:
                self.layups['thick isotropic solid'].update(solidLayerUp(param['solid_t']))
            else:
                self.layups['thick isotropic solid'].update(solidLayerUp())

    def make_mnct(self, param):
        option = self.multiple_trim_option()
        if self.get_multiple_trim_name():
            name = self.get_multiple_trim_name()
        else:
            name = 'mnct' + str(round(time.time()))

        # dis = self.get_multiple_trim_dis()
        # todo 处理用户输入覆盖率字典
        if self.layups[option]:
            MultipleNoiseControlTreatment(name, self.layups[option], distribution=None)
        else:
            QMessageBox.information(self, '消息', '没有layups可供选择，请先生成layup')

    def preprocess_input(self):
        """
        读取用户数据并预处理
        返回字典
        @return: dict
        """
        soft_t = self.get_softlayer_thickness()  # 软层厚度
        hard_t = self.get_hardlayer_thickness()  # 硬层厚度
        solid_t = self.get_steel_thickness()  # 固体厚度
        tsoft_t = self.get_tsoftlayer_thickness()  # 软层大厚度
        if is_number(hard_t):
            hard_t = float(hard_t)
        else:
            hard_t = -1
        if is_number(solid_t):
            solid_t = float(solid_t)
        else:
            solid_t = -1
        if is_number(tsoft_t):
            tsoft_t = float(tsoft_t)
        else:
            tsoft_t = -1
        soft_t = soft_t.split(' ')
        temp = []
        for elem in soft_t:
            if is_number(elem):
                temp.append(float(elem))

        # 分辨信号发出者分别执行
        if self.sender() == self.ui.LoadFiber_pushButton:
            self.sig3.emit({'soft_t': temp, 'hard_t': hard_t, 'solid_t': solid_t, 'tsoft_t': tsoft_t})
        if self.sender() == self.ui.LoadFoam_pushButton:
            self.sig4.emit({'soft_t': temp, 'hard_t': hard_t, 'solid_t': solid_t, 'tsoft_t': tsoft_t})
        if self.sender() == self.ui.TLayUpsApply_pushButton:
            self.sig5.emit({'soft_t': temp, 'hard_t': hard_t, 'solid_t': solid_t, 'tsoft_t': tsoft_t})
        if self.sender() == self.ui.MultipleNCTApply_pushButton:
            self.sig6.emit({'soft_t': temp, 'hard_t': hard_t, 'solid_t': solid_t, 'tsoft_t': tsoft_t})

    def updatefiber(self, df):
        if self.df_fiber.empty:
            self.df_fiber = pd.concat([self.df_fiber, df], axis=0)
        else:
            self.df_fiber.append(df)
        # self.getdf()

    def updatefoam(self, df):
        if self.df_foam.empty:
            self.df_foam = pd.concat([self.df_foam, df], axis=0)
        else:
            self.df_foam.append(df)

    def layer_up_option(self):
        return self.ui.Combination_comboBox.currentText()

    def multiple_trim_option(self):
        return self.ui.MNCTcomboBox.currentText()

    def get_multiple_trim_name(self):
        return self.ui.Name_lineEdit.text()

    def get_multiple_trim_dis(self):
        return self.ui.Distribution_lineEdit.text()

    def get_softlayer_thickness(self):
        return self.ui.SoftThickness_lineEdit.text()

    def get_hardlayer_thickness(self):
        return self.ui.HardThickness_lineEdit.text()

    def get_steel_thickness(self):
        return self.ui.SteelThickness_lineEdit.text()

    def get_tsoftlayer_thickness(self):
        return self.ui.TSoftThickness_lineEdit.text()

    # debug 辅助函数
    def getdf(self):
        print(self.df_fiber)


# 显示data的窗口类
class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None, *args, **kwargs):
        return self._data.shape[0]

    def columnCount(self, parent=None, *args, **kwargs):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class TableView(QMainWindow, Ui_Form):
    def __init__(self):
        super(TableView, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    if QApplication.instance() is None:
        app = QApplication(sys.argv)
        standalone = True
    else:
        standalone = False
    # app = QApplication(sys.argv)
    main = MainWindow()
    main.show()

    # sys.exit(app.exec_())  # 在VAOne里面运行需要把这行去掉
