class node(object):
    def __int__(self,data):
        self._data=data
        self._next=None
    def get_data(self):
        return self._data
    def get_next(self):
        return self._next
    def set_data(self,data):
        self._data=data
    def set_next(self,next):
        self._next=next
class Linklist(object):
    def __int__(self):
        self.head=None
    def add(self,data):
        new_node=node(data)
        new_node.set_next(head)
        head=new_node
    def search(self,data):
        checking=self.head
        while checking != None:
            if checking.get_data()==data : break
            checking=checking.get_next()
        if checking==None :
            return 0
        else : 
            return 1
    def remove(self,data):
        left=None
        right=self.head
        while right != None :
            if right.get_data()==data : break
            left=right
            right=right.get_next()
        if left == None :
            self.head=None
        else :
            left.set_next(right.get_next())
    def isempty(self):
        return self.head == None
    def size(self):
        sum=0
        checking=head
        while checking != None :
            sum=sum+1
            checking=checking.get_next()
        return sum
a=Linklist()
b=node(1)
print(b.get_data())
print(a.isempty())
