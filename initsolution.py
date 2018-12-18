# %%
import numpy as np
import random
import settings as st
import matplotlib.pyplot as plt
import sys
import math
from scipy.optimize import leastsq

# %%


def solveLocation(seq):
    level = len(seq)
    if level == 1:
        theta = random.randint(0, 360)
        return [seq[1] + seq[0] * np.cos(math.radians(theta)), seq[2] + seq[0] * np.sin(math.radians(theta))]

    A = []
    B = []
    line1 = seq[0]
    for i in range(1, level):
        A.append([line1[1] - seq[i][1], line1[2] - seq[i][2]])
        B.append(0.5*(line1[0]**2-seq[i][0]**2+line1[1]**2-seq[i][1]**2 +
                      line1[2]**2-seq[i][2]**2))
    try:
        A = np.asmatrix(A)
        B = np.asmatrix(B).T
        AT = A.T
        ATA = AT * A
        ATA1 = ATA.I
    except Exception as e:
        print(A)
        print(B)
        print(seq)
        print(e)
        return [0, 0]
    return (ATA1 * AT * B).T.tolist()[0]

# %%


def calculateError(seq, p0, gamma, loc):
    totalErr = 0
    for line in seq:
        totalErr += abs(line[0] - p0 + 10 * gamma * np.log10(np.sqrt((loc[0]-line[1])**2+(loc[1]-line[2])**2
                                                                     )))
    return totalErr/len(seq)


def getDistanceSeq(seq, p0, gamma):
    dis = []
    for ms in seq:
        dis.append(
            [np.power(10, (p0 - ms[0]) / 10 * gamma), ms[1], ms[2]])

    return dis


def solveLoop(seq, p0, gamma, res):
    loc = solveLocation(getDistanceSeq(seq, p0, gamma))
    err = calculateError(seq, p0, gamma, loc)
    if err < res[4]:
        res[0] = p0
        res[1] = gamma
        res[2] = loc[0]
        res[3] = loc[1]
        res[4] = err

    return


def solveStrategyR12(seq):
    res = [100, 0, 0, 0, sys.maxsize]
    for p0 in range(st.POWER_MIN, st.POWER_MAX, st.POWER_SEARCH_STEP):
        for gamma in range(st.GAMMA_MIN, st.GAMMA_MAX, st.GAMMA_SEARCH_STEP):
            solveLoop(seq, p0, gamma/10, res)

    return res


def solveStrategyR3(seq):
    res = [100, 0, 0, 0, sys.maxsize]
    p0 = random.randint(st.POWER_MIN, st.POWER_MAX)
    for gamma in range(st.GAMMA_MIN, st.GAMMA_MAX, st.GAMMA_SEARCH_STEP):
        solveLoop(seq, p0, gamma/10, res)

    return res


def solveStartegyR45(seq):
    res = [100, 0, 0, 0, sys.maxsize]
    p0 = random.randint(st.POWER_MIN, st.POWER_MAX)
    gamma = random.randint(st.GAMMA_MIN, st.GAMMA_MAX)/10
    solveLoop(seq, p0, gamma, res)
    return res


def randomInit(seq):
    level = len(seq)
    if level > 3:
        return solveStrategyR12(seq)
    elif level == 3:
        return solveStrategyR3(seq)
    else:
        return solveStartegyR45(seq)
    return []

# %%


def trilaterate(apParam, msrs):
    dSeq = []
    for msr in msrs:
        param = apParam[msr[0]]
        dis = np.power(10, (param[0] - msr[1]) / (10 * param[1]))
        dSeq.append([dis, param[2], param[3]])
    return solveLocation(dSeq)


# %%
devdf = np.loadtxt('./data/uji/midfile/devicediff_0_0.txt')
msrs = np.loadtxt('./data/uji/midfile/simpledata_0_0.txt')

devdir = {}
for devl in devdf:
    devdir[devl[0]] = devl[1]

row, col = msrs.shape
apCount = col - 9

for line in msrs:
    for i in range(0, apCount):
        if line[i] != 100:
            line[i] += devdir[line[-2]]

knownLoc = random.sample(range(0, row), (int)(row * st.KNOWN_LOC_PERCENT))
knownLocSet = set(knownLoc)
unknownLocSet = set(range(0, row)).difference(knownLocSet)

knownApSet = set()
unknownApSet = set(range(0, apCount)).difference(knownApSet)

apParam = {}
locations = {}

level = 5
while level > 0:
    changed = False
    newKnownAP = []

    for i in unknownApSet:
        msrSeq = msrs[list(knownLocSet)]
        msrSeq = msrSeq[msrSeq[:, i] != 100]
        if len(msrSeq) < level:
            continue
        apParam[i] = randomInit(msrSeq[:, (i, -9, -8)])
        newKnownAP.append(i)
        changed = True

    if not changed:
        level -= 1
        continue

    for ap in newKnownAP:
        knownApSet.add(ap)
        unknownApSet.remove(ap)

    newKnownLoc = []

    for j in unknownLocSet:
        msrLine = msrs[j]
        msr = []
        for mi in range(0, apCount):
            if msrLine[mi] == 100:
                continue
            if mi not in knownApSet:
                continue
            msr.append([mi, msrLine[mi]])

        if len(msr) < 3:
            continue
        locations[j] = trilaterate(apParam, msr)
        newKnownLoc.append(j)

    for loc in newKnownLoc:
        knownLocSet.add(loc)
        unknownLocSet.remove(loc)
