import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui_VMainWindow import Ui_MainWindow
# from qtpandas.models.DataFrameModel import DataFrameModel

from Ui_Datashow import Ui_DatashowMainWindow
# import pandas as pd


class Mainwindow(QMainWindow):
    def __init__(self):
        super(Mainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 添加的信号
        self.ui.LoadFiber_pushButton.clicked.connect(self.LoadFiber)
        self.ui.LoadFoam_pushButton.clicked.connect(self.LoadFoam)
        self.ui.Navigate_pushButton.clicked.connect(self.DataNavigate)

    # 槽函数 LoadFiber_pushButton
    def LoadFiber(self):
        dlgFiber = QFileDialog()
        dlgFiber.setFileMode(QFileDialog.AnyFile)
        dlgFiber.setFilter(QDir.Files)

        if dlgFiber.exec_():
            FiberFilenames = dlgFiber.selectedFiles()  # FiberFilenames 文件的绝对路径

    # 槽函数 LoadFoam_pushButton
    def LoadFoam(self):
        dlgFoam = QFileDialog()
        dlgFoam.setFileMode(QFileDialog.AnyFile)
        dlgFoam.setFilter(QDir.Files)

        if dlgFoam.exec_():
            FoamFilenames = dlgFoam.selectedFiles()  # FoamFilenames 文件的绝对路径
            # print(filenames)

    # 槽函数 Navigate_pushButton
    def DataNavigate(self):
        # self.Datashow = DataMainWindow(data)#data 需要显示的数据
        # self.Datashow.show()
        pass


# 显示data的窗口类
# class DataMainWindow(QMainWindow, Ui_DatashowMainWindow):
#     def __init__(self, data):  # 需要显示的数据
#         super(DataMainWindow, self).__init__()
#
#         self.data = data
#
#         self.setWindowTitle("QtPandas")
#         self.setupUi(self)
#
#         widget = self.DatashowWidget
#         widget.resize(600, 500)
#         self.model = DataFrameModel()
#         widget.setViewModel(self.model)
#
#         self.model.setDataFrame(self.data)  # data 需要显示的数据


if __name__ == "__main__":

    if QApplication.instance() is None:
        app = QApplication(sys.argv)
        standalone = True
    else:
        standalone = False


  
    main = Mainwindow()
    main.show()
    # sys.exit(app.exec_())
