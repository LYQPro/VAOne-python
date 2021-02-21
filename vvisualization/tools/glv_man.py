# 跨文件全局变量管理模块
from typing import Dict, Optional

def _ini():
    global _dict
    _dict = {}


def setv(key, val):
    try:
        _dict[key] = val
        return True
    except KeyError:
        return False


def getv(key) -> Optional[dict]:
    try:
        return _dict[key]
    except KeyError:
        return None


def delk(key):
    try:
        del _dict[key]
        return True
    except KeyError:
        return False
