import math as mt
import os
import random

import matplotlib.pyplot
import numpy as np
import numpy.matlib
import pandas as pd
from progressbar import *

import settings as st


def getCommonMsr(msrs1, msrs2):
    commonIndex = []
    for i in range(0, st.AP_COUNT):
        if msrs1[i] != 100 and msrs2[i] != 100:
            commonIndex.append(i)
    return commonIndex


def isProximate(msrs1, msrs2):
    common = getCommonMsr(msrs1, msrs2)
    if (len(common) == 0):
        return False

    cm1 = (np.asarray(msrs1))[common]
    cm2 = (np.asarray(msrs2))[common]
    tmp = cm1[0]
    cm1 -= tmp
    tmp = cm2[0]
    cm2 -= tmp
    diff = abs(sum(cm1 - cm2))
    return diff <= st.PROXIMATE_THRESHOLD


def calculateGResult(dev1, dev2, proPair):
    print("calculateGResult...")
    count = 0
    deltaG = 0
    sigmaG = 0
    pb = ProgressBar().start()
    ct = 0
    tot = len(proPair) * 2
    # Calculate DelatG
    for pair in proPair:
        ct += 1
        pb.update(ct/tot*100)
        msrs1 = dev1[pair[0]]
        msrs2 = dev2[pair[1]]
        common = getCommonMsr(msrs1, msrs2)
        count += len(common)
        for cm in common:
            deltaG += msrs1[cm] - msrs2[cm]

    deltaG /= count

    # Calculate SigmaG
    for pair in proPair:
        ct += 1
        pb.update(ct/tot*100)
        msrs1 = dev1[pair[0]]
        msrs2 = dev2[pair[1]]
        common = getCommonMsr(msrs1, msrs2)
        for cm in common:
            sigmaG += (msrs1[cm] - msrs2[cm] - deltaG) ** 2

    sigmaG = mt.sqrt(sigmaG) / count
    pb.finish()

    return [deltaG, sigmaG]


def calculateGain(dev1, dev2):
    print("estimate proximate pair...")
    proximatePair = []
    pb = ProgressBar().start()
    count = 0
    im = len(dev1)
    jm = len(dev2)
    tot = im * jm
    for i in range(0, im):
        for j in range(0, jm):
            count += 1
            pb.update(count / tot * 100)
            if isProximate(dev1[i], dev2[j]):
                proximatePair.append([i, j])

    pb.finish()

    if (len(proximatePair) == 0):
        print("no proximate pair")
        return [0, 0, 0]

    res = calculateGResult(dev1, dev2, proximatePair)
    vl = [len(proximatePair), res[0], res[1]]
    print(vl)

    return vl


def calculateDeviceDiff(mdata):
    divMsrs = []
    ids = list(set(mdata.PHONEID))

    print("Device List: ")
    print(ids)
    print("Count %d" % len(ids))

    for id in ids:
        divMsrs.append(mdata[mdata.PHONEID == id])

    gainMatrix = []

    for i in range(0, len(divMsrs) - 1):
        for j in range(i + 1, len(divMsrs)):
            print("device %d <> device %d start..." % (i, j))
            gain = calculateGain(divMsrs[i].values, divMsrs[j].values)
            if (gain[0] == 0):
                continue
            gainMatrix.append([i, j, gain[1], gain[2]])

    # Weighted least mean square sense
    row = len(gainMatrix)+1
    col = len(ids)

    gm = np.asmatrix(gainMatrix)

    # Ax=B  WAx=WB  (WA)t(WA)x=(WA)tWB  x=((WA)t(WA))-1(WA)tWB
    A = np.matlib.zeros((row, col), int).tolist()
    B = np.matrix(gm[:, 2]).tolist()
    W = np.matlib.zeros((row, row)).tolist()

    # Random pick G0
    A[row - 1][0] = 1
    B.append([random.randint(st.MIN_GAIN_DIFF, st.MAX_GAIN_DIFF)])
    W[row - 1][row - 1] = 1

    for i in range(0, len(gainMatrix)):
        pair = gainMatrix[i]
        A[i][pair[0]] = 1
        A[i][pair[1]] = -1
        W[i][i] = pair[3]

    A = np.asmatrix(A)
    B = np.asmatrix(B)
    W = np.asmatrix(W)

    WA = W * A
    WAt = WA.T
    WAtWA = WAt * WA
    WAtWAI = WAtWA.I

    x = WAtWAI * WAt * W * B

    ref = A * x

    print("avg err: %f" % (sum(abs(ref - B)) / row))

    return np.hstack((np.asarray(np.asmatrix(ids).T).astype(int), np.asarray(x)))


# Test
# srcData = pd.read_csv('./data/sim/trainingData.csv')

# mdata = srcData[(srcData.BUILDINGID == st.BUILDINGID)
#                 & (srcData.FLOOR == st.FLOORID)]

# x = calculateDeviceDiff(mdata)
