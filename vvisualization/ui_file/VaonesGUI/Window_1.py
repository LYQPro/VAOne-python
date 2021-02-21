import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableView
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Ui_VMainWindow import Ui_MainWindow
import pandas as pd
from Ui_TableView import Ui_Form

df = pd.DataFrame({'a': ['Mary', 'Jim', 'John'],
                   'b': [100, 200, 300],
                   'c': ['a', 'b', 'c']})

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

        model = pandasModel(df)

        self.view = tableView()
        self.view.DtableView.setModel(model)
        self.view.DtableView.resize(800, 600)
        self.view.show()


# 显示data的窗口类


class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None


class tableView(QMainWindow, Ui_Form):
    def __init__(self):
        super(tableView, self).__init__()
        self.setupUi(self)


if __name__ == "__main__":
    if QApplication.instance() is None:
        app = QApplication(sys.argv)
        standalone = True
    else:
        standalone = False
    # app = QApplication(sys.argv)
    main = Mainwindow()
    main.show()
    sys.exit(app.exec_())  # 在VAOne里面运行需要把这行去掉
