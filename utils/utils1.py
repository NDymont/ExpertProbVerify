import numpy as np
import intvalpy as ip

from utils import number2interval as n2i


def lineOne(size):
    return np.array([size * [1]])


def unitMatrix(size):
    return np.eye(size)


def makeZeroOne():
    return ip.Interval([[0, 1]])


def makeZeroOneList(size):
    res = makeZeroOne()
    for i in range(1, size):
        res = n2i.concatInval(res, makeZeroOne())
    return res


def makeOneOne():
    return ip.Interval([[1, 1]])
