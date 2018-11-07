import numpy as np


def execLoc(dis):
    A = []
    B = []

    row1 = dis.loc(0)

    for index in range(1, len(dis)):
        A.append([-2 * (row1[1] - equ[index][1]), -2 * (row1[2] - equ[index][2])])
        B.append(row1[0]** 2 - equ[index][0]** 2)
        
    ma = np.asmatrix(A)
    mb = np.asmatrix(B)
    
    mat = ma.T
    masq = mat * ma
    res = masq.I * mat * mb

    return res
