# IND='ON'
# class Kls(object):
#     def __init__(self, data):
#         self.data = data

#     @staticmethod
#     def checkind():
#         return IND == 'ON'

#     def do_reset(self):
#         if self.checkind():
#             print('Reset done for: %s' % self.data)

#     def set_db(self):
#         if self.checkind():
#             print('DB connection made for: %s' % self.data)


# ik1 = Kls(24)
# ik1.do_reset()
# ik1.set_db()
# import tkinter
# import tkinter.messagebox


# def main():
#     flag = True

#     # 修改标签上的文字
#     def change_label_text():
#         nonlocal flag
#         flag = not flag
#         color, msg = ('red', 'Hello, world!')\
#             if flag else ('blue', 'Goodbye, world!')
#         label.config(text=msg, fg=color)

#     # 确认退出
#     def confirm_to_quit():
#         if tkinter.messagebox.askokcancel('温馨提示', '确定要退出吗?'):
#             top.quit()

#     # 创建顶层窗口
#     top = tkinter.Tk()
#     # 设置窗口大小
#     top.geometry('240x160')
#     # 设置窗口标题
#     top.title('小游戏')
#     # 创建标签对象并添加到顶层窗口
#     label = tkinter.Label(top, text='Hello, world!', font='Arial -32', fg='red')
#     label.pack(expand=1)
#     # 创建一个装按钮的容器
#     panel = tkinter.Frame(top)
#     # 创建按钮对象 指定添加到哪个容器中 通过command参数绑定事件回调函数
#     button1 = tkinter.Button(panel, text='修改', command=change_label_text)
#     button1.pack(side='left')
#     button2 = tkinter.Button(panel, text='退出', command=confirm_to_quit)
#     button2.pack(side='right')
#     panel.pack(side='bottom')
#     # 开启主事件循环
#     tkinter.mainloop()


# if __name__ == '__main__':
#     main()
# def main():
#     with open('测试文本.txt',encoding='utf-8') as f:
#         lines=f.readlines()
#     print(lines)
    
# if __name__=='__main__':
#     main()
from json import *
class A:
    def show(self):
        return 'mysql'
a=A()
f=dumps(a.show())
print(f)
print(loads(f))
print(dir(JSONDecoder))
    