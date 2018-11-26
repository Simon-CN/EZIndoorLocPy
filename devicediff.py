import math as mt

import matplotlib.pyplot
import numpy as np
import numpy.matlib
import pandas as pd

import settings as st


def getCommonMsr(msrs1, msrs2):
    commonIndex = []
    for i in range(0, st.AP_COUNT):
        if msrs1[i] != 100 and msrs2[i] != 100:
            commonIndex.append(i)

    return commonIndex


def isProximate(msrs1, msrs2):
    common = getCommonMsr(msrs1, msrs2)
    if (len(common == 0)):
        return False
    diff = 0
    cm1 = (np.asarray(msrs1))[common]
    cm2 = (np.asarray(msrs2))[common]
    tmp = cm1[0]
    cm1 -= tmp
    tmp = cm2[0]
    cm2 -= tmp
    for i in common:
        diff += cm1[i] - cm2[i]
    diff /= len(common)

    return abs(diff) <= st.PROXIMATE_THRESHOLD


def calculateGResult(dev1, dev2, proPair):
    count = 0
    deltaG = 0
    sigmaG = 0

    # Calculate DelatG
    for pair in proPair:
        msrs1 = dev1[pair[0]]
        msrs2 = dev2[pair[1]]
        common = getCommonMsr(msrs1, msrs2)
        count += len(common)

        for cm in common:
            deltaG += msrs1[cm] - msrs2[cm]

    deltaG /= count

    # Calculate SigmaG
    for pair in proPair:
        msrs1 = dev1[pair[0]]
        msrs2 = dev2[pair[1]]
        common = getCommonMsr(msrs1, msrs2)

        for cm in common:
            sigmaG += (msrs1[cm] - msrs2[cm] - deltaG) ** 2

    sigmaG = mt.sqrt(sigmaG) / count

    return [deltaG, sigmaG]


def calculateGain(dev1, dev2):
    proximatePair = []

    for i in range(0, len(dev1)):
        for j in range(0, len(dev2)):
            if isProximate(dev1[i], dev2[j]):
                proximatePair.append(i, j)

    if (len(proximatePair) == 0):
        return [0, 0, 0]

    res = calculateGResult(dev1, dev2, proximatePair)
    return [len(proximatePair), res[0], res[1]]


srcData = pd.read_csv('./data/uji/trainingData.csv')

data = srcData.values

divMsrs = []
ids = list(set(srcData['PHONEID']))
for id in ids:
    divMsrs.append(srcData[srcData['PHONEID'] == id])

gainMatrix = []

for i in range(0, len(divMsrs) - 1):
    for j in range(i + 1, len(divMsrs)):
        gain = calculateGain(divMsrs[i], divMsrs[j])
        if (gain[0] == 0):
            continue
        gainMatrix.append([i, j, gain[1], gain[2]])

# Weighted least mean square sense
row = len(gainMatrix)
col = len(ids)

gm = np.asmatrix(gainMatrix)

# Ax=B  WAx=WB  (WA)t(WA)x=(WA)tWB  x=((WA)t(WA))-1(WA)tWB
A = np.matlib.zeros((row, col), int)
B = np.matrix(gm[:, 2])
W = np.matlib.zeros((row, row))

for i in range(0, len(gainMatrix)):
    pair = gainMatrix[i]
    A[i][pair[0]] = 1
    A[i][pair[1]] = -1
    W[i][i] = pair[3]
    
WA = W * A
WAt = WA.T
WAtWA = WAt * WA
WAtWAI = WAtWA.I

x = WAtWAI * WAt * W * B

