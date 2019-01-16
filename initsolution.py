# %%
import math
import random
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as hie
from scipy.optimize import leastsq

import settings as st


def convertSolution(aps, locs, devDiff):
    apParam = [[0] * 4 for i in range(len(aps))]
    locations = [[0] * 2 for i in range(len(locs))]

    for ap in aps:
        apParam[ap] = aps[ap]

    for lc in locs:
        locations[lc] = locs[lc]

    return [sys.maxsize, apParam, locations, devDiff]


def solveLocation(seq):
    level = len(seq)
    if level == 1:
        theta = random.randint(0, 360)
        line = seq[0]
        return [line[1] + line[0] * np.cos(math.radians(theta)), line[2] + line[0] * np.sin(math.radians(theta))]

    A = []
    B = []
    line1 = seq[0]
    for i in range(1, level):
        A.append([line1[1] - seq[i][1], line1[2] - seq[i][2]])
        B.append(0.5*(seq[i][0]**2
                      - line1[0]**2+line1[1]**2-seq[i][1]**2 +
                      line1[2]**2-seq[i][2]**2))

    A = np.asmatrix(A)
    B = np.asmatrix(B).T
    AT = A.T
    ATA = AT * A
    ATA1 = ATA.I
    return (ATA1 * AT * B).T.tolist()[0]


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
            [np.power(10, (p0 - ms[0]) / (10 * gamma)), ms[1], ms[2]])

    return dis


def drawCircles(r, x, y):
    theta = np.arange(0, 2 * np.pi, 0.01)
    sx = x + r * np.cos(theta)
    sy = y + r * np.sin(theta)
    plt.plot(sx, sy)
    return


def filterDistanceSeq(seq):
    newSeq = []
    for s in seq:
        if s[0] <= st.RADIUS_THRESHOLD:
            newSeq.append(s)
    return newSeq


def solveLoop(seq, p0, gamma, res):
    try:
        disSeq = getDistanceSeq(seq, p0, gamma)
        # disSeq = filterDistanceSeq(disSeq)
        if len(disSeq) == 0:
            return
        # plt.figure(0)
        # for line in disSeq:
        #     drawCircles(line[0], line[1], line[2])
        # plt.show()
        loc = solveLocation(disSeq)
        if loc[0] < st.SPACE_RANGE[0] or loc[0] > st.SPACE_RANGE[2] or loc[1] > st.SPACE_RANGE[1] or loc[1] < st.SPACE_RANGE[3]:
            return
        err = calculateError(seq, p0, gamma, loc)
        # print("p0: %d, gamma: %f, err: %f" % (p0, gamma, err))
        if err < res[4]:
            res[0] = p0
            res[1] = gamma
            res[2] = loc[0]
            res[3] = loc[1]
            res[4] = err
    except Exception as e:
        print(e)
    return


def solveStrategyR12(seq):
    res = [100, 0, 0, 0, sys.maxsize]
    for p0 in range(st.POWER_MIN, st.POWER_MAX, st.POWER_SEARCH_STEP):
        for gamma in range(st.GAMMA_MIN, st.GAMMA_MAX, st.GAMMA_SEARCH_STEP):
            solveLoop(seq, p0, gamma / 10, res)
    return res


def solveStrategyR3(seq):
    res = [100, 0, 0, 0, sys.maxsize]
    i = 20
    while True:
        i -= 1
        p0 = random.randint(st.POWER_MIN, st.POWER_MAX)
        for gamma in range(st.GAMMA_MIN, st.GAMMA_MAX, st.GAMMA_SEARCH_STEP):
            solveLoop(seq, p0, gamma / 10, res)
        if res[0] != 100 or i == 0:
            break
    return res


def solveStartegyR45(seq):
    res = [100, 0, 0, 0, sys.maxsize]
    i = 20
    while True:
        i -= 1
        p0 = random.randint(st.POWER_MIN, st.POWER_MAX)
        gamma = random.randint(st.GAMMA_MIN, st.GAMMA_MAX)/10
        solveLoop(seq, p0, gamma, res)
        if res[0] != 100 or i == 0:
            break

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


def positionFilter(seq):
    position = seq[:, (1, 2)]
    Y = hie.distance.pdist(position)
    Z = hie.linkage(Y, method='average')
    res = hie.fcluster(Z, t=st.GRID_DISTANCE_THRESHOLD, criterion='distance')

    cluDir = {}
    for i, v in enumerate(res):
        if v in cluDir.keys():
            cluDir[v].append(i)
        else:
            tmp = [i]
            cluDir[v] = tmp

    filMsrs = []
    for itm in cluDir.items():
        clu = seq[itm[1]]
        filMsrs.append([np.average(clu[:, 0]), np.average(
            clu[:, 1]), np.average(clu[:, 2])])
    filMsrs = filterDistanceSeq(filMsrs)
    return filMsrs


def ERSGA(msrs, knownLoc, devdf):
    st.SPACE_RANGE = [min(msrs[:, -9] - st.POSITION_OFFSET), max(msrs[:, -8]) + st.POSITION_OFFSET,
                      max(msrs[:, -9]) + st.POSITION_OFFSET, min(msrs[:, -8]) - st.POSITION_OFFSET]
    st.RADIUS_THRESHOLD = np.sqrt(
        (st.SPACE_RANGE[0]-st.SPACE_RANGE[2])**2+(st.SPACE_RANGE[1]-st.SPACE_RANGE[3])**2)/2
    devdir = {}
    for devl in devdf:
        devdir[int(devl[0])] = devl[1]
    row, col = msrs.shape
    apCount = col - 9

    for line in msrs:
        for i in range(0, apCount):
            if line[i] != 100:
                line[i] += devdir[line[-2]]

    # knownLoc = random.sample(range(0, row), (int)(row * st.KNOWN_LOC_PERCENT))
    knownLocSet = set(knownLoc)
    unknownLocSet = set(range(0, row)).difference(knownLocSet)

    knownApSet = set()
    unknownApSet = set(range(0, apCount)).difference(knownApSet)

    apParam = {}
    locations = {}

    for poi in knownLoc:
        locations[poi] = msrs[poi, (-9, -8)].tolist()

    level = 5
    while level > 0:
        changed = False
        newKnownAP = []

        for i in unknownApSet:
            msrSeq = []
            for knap in knownLocSet:
                if msrs[knap, i] != st.DEFAULT_RSSI:
                    msrSeq.append(
                        [msrs[knap, i], locations[knap][0], locations[knap][1]])
            if len(msrSeq) < level:
                continue
            if len(msrSeq) == 1:
                pram = randomInit(msrSeq)
            else:
                filt = positionFilter(np.asarray(msrSeq))
                if len(filt) < level:
                    continue
                pram = randomInit(filt)
            if pram[0] == 100:
                continue
            apParam[i] = pram
            newKnownAP.append(i)
            changed = True
            print("AP %d Solved..." % i)
            print(pram)

        if not changed:
            level -= 1
            print("level = %d ====================" % level)
            continue

        for ap in newKnownAP:
            knownApSet.add(ap)
            unknownApSet.remove(ap)

        newKnownLoc = []

        for j in unknownLocSet:
            msrLine = msrs[j]
            msr = []
            for mi in range(0, apCount):
                if msrLine[mi] == st.DEFAULT_RSSI:
                    continue
                if mi not in knownApSet:
                    continue
                msr.append([mi, msrLine[mi]])

            if len(msr) < 3:
                continue
            dSeq = []
            for mr in msr:
                param = apParam[mr[0]]
                dis = np.power(10, (param[0] - mr[1]) / (10 * param[1]))
                dSeq.append([dis, param[2], param[3]])

            filt = positionFilter(np.asarray(dSeq))
            if len(filt) < 3:
                continue
            locations[j] = solveLocation(filt)
            newKnownLoc.append(j)

        for loc in newKnownLoc:
            knownLocSet.add(loc)
            unknownLocSet.remove(loc)

    for ua in unknownApSet:
        apParam[ua] = [random.randint(st.POWER_MIN, st.POWER_MAX), random.uniform(st.GAMMA_MIN, st.GAMMA_MAX), random.uniform(
            st.SPACE_RANGE[0], st.SPACE_RANGE[2]), random.uniform(st.SPACE_RANGE[3], st.SPACE_RANGE[1])]

    for ul in unknownLocSet:
        locations[ul] = [random.uniform(st.SPACE_RANGE[0], st.SPACE_RANGE[2]), random.uniform(
            st.SPACE_RANGE[3], st.SPACE_RANGE[1])]

    return convertSolution(apParam, locations, devdir)


# devdf = np.loadtxt("./data/uji/midfile/devicediff_%d_%d.txt" %
#                    (st.BUILDINGID, st.FLOORID))
# msrs = np.loadtxt("./data/uji/midfile/simpledata_%d_%d.txt" %
#                   (st.BUILDINGID, st.FLOORID))
# row, col = msrs.shape
# knownLoc = random.sample(range(0, row), (int)(row * st.KNOWN_LOC_PERCENT))
# initSlu = ERSGA(msrs, knownLoc, devdf)
# #%%
# initSlu = convertSolution(initAP, initLoc, devDir)

# #%%
# print(initSlu)
