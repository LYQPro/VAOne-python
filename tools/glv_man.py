#跨文件全局变量管理模块

def _ini():
    global _dict
    _dict = {}


def _setv(key,val):

    try:
        _dict[key] = val
        return True
    except KeyError:
        return False


def _getv(key):
    try:
        return _dict[key]
    except KeyError:
        return "NotFound"

def _delk(key):
    try:
        del _dict[key]
        return True
    except KeyError:
        return False

