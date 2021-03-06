import random
from functools import cmp_to_key

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as hie

import settings as st


def calculateSimilarity(a, b):
    ref = -1
    for i in range(0, st.AP_COUNT):
        if a[i] != 1 and b[i] != 1:
            ref = i
            break
    if ref == -1:
        return 0
    a[a != 1] -= a[ref]
    b[b != 1] -= b[ref]

    tot = 0
    count = 0
    for i in range(0, st.AP_COUNT):
        if a[i] != 1 or b[i] != 1:
            tot += abs(a[i] - b[i])
            count += 1
    avg = tot / count
    if avg > 1:
        avg = 1
    return avg


def doCluster(data):
    sim = hie.distance.pdist(data, metric=calculateSimilarity)
    Z = hie.linkage(sim, method='average')
    hie.dendrogram(Z, color_threshold=st.LOC_CLU_THRESHOLD)
    res = hie.fcluster(Z, st.LOC_CLU_THRESHOLD,criterion='distance')
    print(res)
    return res


def doSelect(seq, data):
    if len(seq) == 1:
        return seq[0]
    lens = []
    for i in seq:
        lens.append([i, len(data[i][data[i] != 1])])
    sorted(lens, key=cmp_to_key(lambda a, b: b[1] - a[1]))
    eq = []
    ml = lens[0][1]
    for ln in lens:
        if ln[1] == ml:
            eq.append(ln[0])
        else:
            break
    if len(eq) == 1:
        return eq[0]
    maxsm = 0
    selectIdx = 0
    for i in eq:
        tot = 0
        for oth in seq:
            tot += calculateSimilarity(data[i], data[oth])
        if tot > maxsm:
            maxsm = tot
            selectIdx = i
    return selectIdx


def selectLocs(srcData):
    data = srcData.values[:, 0: st.AP_COUNT]
    data = abs(data)
    data[data > st.RSSI_THRESHOLD] = st.RSSI_THRESHOLD
    data /= st.RSSI_THRESHOLD

    cluArr = doCluster(data)
    cluDir = {}
    for i, val in enumerate(cluArr):
        if val in cluDir:
            cluDir[val].append(i)
        else:
            cluDir[val] = [i]

    res = []
    for clu in cluDir.items():
        res.append(doSelect(clu[1], data))

    return res

# srcData = pd.read_csv(st.TRAIDATA_PATH)
# srcData = srcData[(srcData.BUILDINGID == st.BUILDINGID)
#                & (srcData.FLOOR == st.FLOORID)]
# data = srcData.values[:, 0: st.AP_COUNT]
# data = abs(data)
# data[data > st.RSSI_THRESHOLD] = st.RSSI_THRESHOLD
# data /= st.RSSI_THRESHOLD

# sim = hie.distance.pdist(data, metric=calculateSimilarity)
# Z = hie.linkage(sim, method='average')
# res = hie.fcluster(Z, st.LOC_CLU_THRESHOLD)

# hie.dendrogram(Z, color_threshold=0.1)
# plt.show()
# res = hie.fcluster(Z, 0.1)


# res = selectLocs(data)
# import dataload as ld
# data, apMap = ld.loadData()
# ls = selectLocs(data)
# print(len(ls))
# print(data.shape)
# plt.show()
