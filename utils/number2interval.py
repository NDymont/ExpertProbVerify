import intvalpy as ip
from intvalpy import *


def numer2interval(array):
    countLines = array.shape[0]
    countColumn = array.shape[1]
    res = None
    for i in range(0, countLines):
        for j in range(0, countColumn):
            inval1 = [array[i][j], array[i][j] + 1e-12]
            inval2 = [[inval1]]
            inval = ip.Interval(inval2)

            if res is not None:
                v1 = np.array(res)
                some = np.concatenate((v1, np.array(inval)))
                res = ip.ArrayInterval(some)
            else:
                res = ip.ArrayInterval(np.array(inval))
    result = ip.ArrayInterval(np.reshape(res, (countLines, countColumn)))
    return result


def concatInval(A, B):
    ABcon = np.concatenate((np.array(A), np.array(B)))
    C = ip.ArrayInterval(ABcon)
    return C
