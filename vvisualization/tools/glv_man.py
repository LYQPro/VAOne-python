# 跨文件全局变量管理模块
from typing import Dict, Any


def _ini():
    global _dict
    _dict = {}


def setv(key, val):
    try:
        _dict[key] = val
        return True
    except KeyError:
        return False


def getv(key: object) -> object:
    try:
        return _dict[key]
    except KeyError:
        return "NotFound"


def delk(key):
    try:
        del _dict[key]
        return True
    except KeyError:
        return False
