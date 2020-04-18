# import PyQt5
# import pyqt5_tools
# import sqlite3
# import os
# import time

# f = (x ** 2 for x in range(1, 1000))  #f是一个生成器对象
# f1=[f] #f1是一个列表
# def fib(n):
#     a, b = 0, 1
#     for _ in range(n):
#         a, b = b, a + b
#         yield a #创建生成器函数


# def main():
#     for val in fib(20):
#         print(val)


# # if __name__ == '__main__':
# #     main()
# scores = {'骆昊': 95, '白元芳': 78, '狄仁杰': 82}
# print(scores)
# # 创建字典的构造器语法
# items1 = dict(one=1, two=2, three=3, four=4)
# # 通过zip函数将两个序列压成字典
# items2 = dict(zip(['a', 'b', 'c'], '122'))
# # 创建字典的推导式语法
# items3 = {num: num ** 2 for num in range(1, 10)}
# print(items1, items2, items3)
# def main():
#     content = '北京欢迎你为你开天辟地…………'
#     while True:
#         # 清理屏幕上的输出
#         # os.system('cls')  # os.system('clear')
#         print(content)
#         # 休眠200毫秒
#         time.sleep(0.2)
#         content = content[1:] + content[0]


# if __name__ == '__main__':
#     main()
# import random


# def generate_code(code_len=4):
#     """
#     生成指定长度的验证码

#     :param code_len: 验证码的长度(默认4个字符)

#     :return: 由大小写英文字母和数字构成的随机验证码
#     """
#     all_chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#     last_pos = len(all_chars) - 1
#     code = ''
#     for _ in range(code_len):
#         index = random.randint(0, last_pos)
#         code += all_chars[index]
#     return code
# print(generate_code())
# import os


# def print_board(board):
#     print(board['TL'] + '|' + board['TM'] + '|' + board['TR'])
#     print('-+-+-')
#     print(board['ML'] + '|' + board['MM'] + '|' + board['MR'])
#     print('-+-+-')
#     print(board['BL'] + '|' + board['BM'] + '|' + board['BR'])


# def main():
#     init_board = {
#         'TL': ' ', 'TM': ' ', 'TR': ' ',
#         'ML': ' ', 'MM': ' ', 'MR': ' ',
#         'BL': ' ', 'BM': ' ', 'BR': ' '
#     }
#     begin = True
#     while begin:
#         curr_board = init_board.copy()
#         begin = False
#         turn = 'x'
#         counter = 0
#         os.system('clear')
#         print_board(curr_board)
#         while counter < 9:
#             move = input('轮到%s走棋, 请输入位置: ' % turn)
#             if curr_board[move] == ' ':
#                 counter += 1
#                 curr_board[move] = turn
#                 if turn == 'x':
#                     turn = 'o'
#                 else:
#                     turn = 'x'
#             os.system('clear')
#             print_board(curr_board)
#         choice = input('再玩一局?(yes|no)')
#         begin = choice == 'yes'


# if __name__ == '__main__':
#     main()
# class Student(object):

#     # __init__是一个特殊方法用于在创建对象时进行初始化操作
#     # 通过这个方法我们可以为学生对象绑定name和age两个属性
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

#     def study(self, course_name):
#         print('%s正在学习%s.' % (self.name, course_name))

#     # PEP 8要求标识符的名字用全小写多个单词用下划线连接
#     # 但是部分程序员和公司更倾向于使用驼峰命名法(驼峰标识)
#     def watch_movie(self):
#         if self.age < 18:
#             print('%s只能观看《熊出没》.' % self.name)
#         else:
#             print('%s正在观看岛国爱情大电影.' % self.name)
# def main():
#     # 创建学生对象并指定姓名和年龄
#     stu1 = Student('骆昊', 38)
#     # 给对象发study消息
#     stu1.study('Python程序设计')
#     # 给对象发watch_av消息
#     stu1.watch_movie()
#     stu2 = Student('王大锤', 15)
#     stu2.study('思想品德')
#     stu2.watch_movie()


# if __name__ == '__main__':
#     main()
# class Test:

#     def __init__(self, foo):
#         self.__foo = foo

#     def __bar(self):
#         print(self.__foo)
#         print('__bar')


# def main():
#     test = Test('hello')
#     # AttributeError: 'Test' object has no attribute '__bar'
#     test.__bar()
#     # AttributeError: 'Test' object has no attribute '__foo'
#     print(test.__foo)


# if __name__ == "__main__":
#     main()
# class Test:

#     def __init__(self, foo):
#         self.__foo = foo

#     def __bar(self):
#         print(self.__foo)
#         print('__bar')


# def main():
#     test = Test('hello')
#     test._Test__bar()
#     print(test._Test__foo)


# if __name__ == "__main__":
#     main()
# class Student(object):

#     def __init__(self, name, age):
#         self._name = name
#         self._age = age

#     def __str__(self):
#         return self.__name + ': ' + str(self.__age)


# def main():
#     stu = Student('骆昊', 38)
#     # 'Student' object has no attribute '__name'
#     # print(stu.__name)
#     # 用下面的方式照样可以访问类中的私有成员
#     print(stu._name)
#     print(stu._age)


# if __name__ == '__main__':
#     main()

# def log(text):
#     def decrator(func):
#         def wrapper(*args,**kwargs):
#             print('%s call %s:' % (text,func.__name__))
#             return func(*args,**kwargs)
#         return wrapper
#     return decrator
# @log('exceute')
# def now():
#     print('2020-4-4')
# now()
# print(now.__name__)
# class Person(object):

#     # 限定Person对象只能绑定_name, _age和_gender属性
#     __slots__ = ('_name', '_age', '_gender')

#     def __init__(self, name, age):
#         self._name = name
#         self._age = age

#     @property
#     def name(self):
#         return self._name

#     @property
#     def age(self):
#         return self._age

#     @age.setter
#     def age(self, age):
#         self._age = age

#     def play(self):
#         if self._age <= 16:
#             print('%s正在玩飞行棋.' % self._name)
#         else:
#             print('%s正在玩斗地主.' % self._name)


# def main():
#     person = Person('王大锤', 22)
#     person.play()
#     person._gender = '男'
#     print(person._gender)
# if __name__=='__main__':
#     main()
# from time import time, localtime, sleep


# class Clock(object):
#     """数字时钟"""

#     def __init__(self, hour=0, minute=0, second=0):
#         self._hour = hour
#         self._minute = minute
#         self._second = second

#     @classmethod
#     def now(cls):
#         ctime = localtime(time())
#         return cls(ctime.tm_hour, ctime.tm_min, ctime.tm_sec)

#     def run(self):
#         """走字"""
#         self._second += 1
#         if self._second == 60:
#             self._second = 0
#             self._minute += 1
#             if self._minute == 60:
#                 self._minute = 0
#                 self._hour += 1
#                 if self._hour == 24:
#                     self._hour = 0

#     def show(self):
#         """显示时间"""
#         return '%02d:%02d:%02d'% (self._hour, self._minute, self._second)


# def main():
#     # 通过类方法创建对象并获取系统时间
#     clock = Clock.now()
#     while True:
#         print(clock.show())
#         sleep(1)
#         clock.run()


# if __name__ == '__main__':
#     main()
from abc import ABCMeta, abstractmethod
from random import randint, randrange


class Fighter(object, metaclass=ABCMeta):  #一个抽象类
    """战斗者"""

    # 通过__slots__魔法限定对象可以绑定的成员变量
    __slots__ = ('_name', '_hp')

    def __init__(self, name, hp):
        """初始化方法

        :param name: 名字
        :param hp: 生命值
        """
        self._name = name
        self._hp = hp

    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp):
        self._hp = hp if hp >= 0 else 0

    @property
    def alive(self):
        return self._hp > 0

    @abstractmethod          
    def attack(self, other):
        """攻击

        :param other: 被攻击的对象
        """
        pass


class Ultraman(Fighter):
    """奥特曼"""

    __slots__ = ('_name', '_hp', '_mp')

    def __init__(self, name, hp, mp):
        """初始化方法

        :param name: 名字
        :param hp: 生命值
        :param mp: 魔法值
        """
        super().__init__(name, hp)
        self._mp = mp

    def attack(self, other):
        other.hp -= randint(15, 25)

    def huge_attack(self, other):
        """究极必杀技(打掉对方至少50点或四分之三的血)

        :param other: 被攻击的对象

        :return: 使用成功返回True否则返回False
        """
        if self._mp >= 50:
            self._mp -= 50
            injury = other.hp * 3 // 4
            injury = injury if injury >= 50 else 50
            other.hp -= injury
            return True
        else:
            self.attack(other)
            return False

    def magic_attack(self, others):
        """魔法攻击

        :param others: 被攻击的群体

        :return: 使用魔法成功返回True否则返回False
        """
        if self._mp >= 20:
            self._mp -= 20
            for temp in others:
                if temp.alive:
                    temp.hp -= randint(10, 15)
            return True
        else:
            return False

    def resume(self):
        """恢复魔法值"""
        incr_point = randint(1, 10)
        self._mp += incr_point
        return incr_point

    def __str__(self):
        return '~~~%s奥特曼~~~\n' % self._name + \
            '生命值: %d\n' % self._hp + \
            '魔法值: %d\n' % self._mp


class Monster(Fighter):
    """小怪兽"""

    __slots__ = ('_name', '_hp')

    def attack(self, other):
        other.hp -= randint(10, 20)

    def __str__(self):
        return '~~~%s小怪兽~~~\n' % self._name + \
            '生命值: %d\n' % self._hp


def is_any_alive(monsters):
    """判断有没有小怪兽是活着的"""
    for monster in monsters:
        if monster.alive > 0:
            return True
    return False


def select_alive_one(monsters):
    """选中一只活着的小怪兽"""
    monsters_len = len(monsters)
    while True:
        index = randrange(monsters_len)
        monster = monsters[index]
        if monster.alive > 0:
            return monster


def display_info(ultraman, monsters):
    """显示奥特曼和小怪兽的信息"""
    print(ultraman)
    for monster in monsters:
        print(monster, end='')


def main():
    u = Ultraman('骆昊', 1000, 120)
    m1 = Monster('狄仁杰', 250)
    m2 = Monster('白元芳', 500)
    m3 = Monster('王大锤', 750)
    ms = [m1, m2, m3]
    fight_round = 1
    while u.alive and is_any_alive(ms):
        print('========第%02d回合========' % fight_round)
        m = select_alive_one(ms)  # 选中一只小怪兽
        skill = randint(1, 10)   # 通过随机数选择使用哪种技能
        if skill <= 6:  # 60%的概率使用普通攻击
            print('%s使用普通攻击打了%s.' % (u.name, m.name))
            u.attack(m)
            print('%s的魔法值恢复了%d点.' % (u.name, u.resume()))
        elif skill <= 9:  # 30%的概率使用魔法攻击(可能因魔法值不足而失败)
            if u.magic_attack(ms):
                print('%s使用了魔法攻击.' % u.name)
            else:
                print('%s使用魔法失败.' % u.name)
        else:  # 10%的概率使用究极必杀技(如果魔法值不足则使用普通攻击)
            if u.huge_attack(m):
                print('%s使用究极必杀技虐了%s.' % (u.name, m.name))
            else:
                print('%s使用普通攻击打了%s.' % (u.name, m.name))
                print('%s的魔法值恢复了%d点.' % (u.name, u.resume()))
        if m.alive > 0:  # 如果选中的小怪兽没有死就回击奥特曼
            print('%s回击了%s.' % (m.name, u.name))
            m.attack(u)
        display_info(u, ms)  # 每个回合结束后显示奥特曼和小怪兽的信息
        fight_round += 1
    print('\n========战斗结束!========\n')
    if u.alive > 0:
        print('%s奥特曼胜利!' % u.name)
    else:
        print('小怪兽胜利!')


if __name__ == '__main__':
    main()