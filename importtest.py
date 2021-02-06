# import sys
# sys.path.append('C:\\Program Files\\ESI Group\\VAOne2019\\Python36\\Lib\\site-packages\\VAOne')
# from pprint import pprint
# pprint(sys.path_importer_cache)
# import sys
# import importlib
# from pprint import pprint

# importlib.reload(VAOne)
# pprint(sys.modules)
# 定义一个指定范围的自然数类，并可以提供迭代

class Num:
    count = 0
    count1 = []
    def __init__(self, max_num):
        self.max_num = max_num
    
        
    def __iter__(self):
        return self

    def __next__(self):
        if self.count < self.max_num:
            self.count += 1
            self.count1.append(1)
            return self.count
        else:
            raise StopIteration('已经到达临界')
        
num = Num(10)
next(num)
next(num)
print(num.count)
print(locals())