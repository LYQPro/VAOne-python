from VAOne import *


class Find(object):
    # classid = 1
    def __init__(self, db, Class, name):
        self.db = db
        self.Class = Class
        self.name = name

    def FindandConvert(self, aim=None):
        origin = pi_fNeoDatabaseFindByName(
            self.db, globals()["pi_f"+self.Class+"GetClassID"](), self.name)
        if aim == None:
            return origin
        return globals()["pi_fConvertNeoPersist"+aim]((pi_fConvertDBElementNeoPersist(origin)))

    @staticmethod
    def FindNamedDBElementByIterator(db,name, NeoList, ObjectNameList):  # return value by two lists
        iterator = pi_fIteratorCreate(
            db, globals()["pi_f"+name+"GetClassID"](), 1)
        while pi_fIteratorCurrent(iterator) != None:
            NeoList.append(pi_fIteratorCurrent(iterator))
            ObjectNameList.append(pi_fNamedDBElementGetCName(pi_fConvertNeoPersistNamedDBElement(
                NeoList[-1])))  # get object's name by NamedDBElement method
            #print(ObjectNameList[-1])
            # return　NeoPersist and move iterator forward
            pi_fIteratorNext(iterator)
        pi_fNeoIteratorDelete(iterator)  # delete pointer
    # @classmethod
    # def clsmtd(cls):
    #     print("calssmethod")

# try:
#     db = pi_fNeoDatabaseGetCurrent()
#     PlateNeoList = []
#     PlateNameList = []
#     Find.FindNamedDBElementByIterator("Plate", PlateNeoList, PlateNameList)
#     print(PlateNameList)
#     # Find.clsmtd()
# except:
#     raise