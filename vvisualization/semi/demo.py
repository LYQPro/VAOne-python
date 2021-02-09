from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit

def handlecalc():                    #处理信号得函数 slot
    print('统计按钮被点击了')          #print打印在终端上
    info= textEdit.toPlainText()
    






app = QApplication([])        #首先创建

window = QMainWindow()
window.resize(500, 400)        #横向 纵向
window.move(300, 310)
window.setWindowTitle('薪资统计')

textEdit = QPlainTextEdit(window)     #纯文本编辑框
textEdit.setPlaceholderText("请输入薪资表")   #空内容时得提示文本
textEdit.move(10,25)            #move相对于父窗口window
textEdit.resize(300,350)         

button = QPushButton('统计', window)
button.move(380,80)
button.clicked.connect(handlecalc)
window.show()                           #最上层控件展示

app.exec_()                             #程序循环 等待用户输入