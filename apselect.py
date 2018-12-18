from functools import cmp_to_key

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.cluster.hierarchy as hcluster

import settings as st


def calculateDistance(a, b):
    l = len(a)
    count = 0
    sm = 0
    for i in range(0, l):
        if a[i] == 1 and b[i] == 1:
            continue
        sm += abs(a[i] - b[i])
        count += 1

    if count == 0:
        return 1
    return sm / count


def doCluster(tdata):
    dis = hcluster.distance.pdist(tdata, metric=calculateDistance)
    Z = hcluster.linkage(dis, method='average')
    res = hcluster.fcluster(Z, st.AP_CLU_THRESHOLD)

    return res


def doSelect(idxs, data):
    lens = []
    for idx in idxs:
        line = data[:, idx]
        lens.append([idx, len(line[line < 1])])

    sorted(lens, key=cmp_to_key(lambda x, y: y[1] - x[1]))

    if lens[0][1] > lens[1][1]:
        return lens[0][0]

    eqs = []
    mx = lens[0][1]
    for i in lens:
        if i[1] != mx:
            break
        eqs.append(i[0])

    res = [0, 0]
    for idx in eqs:
        sim = 0
        for ot in idxs:
            sim += calculateDistance(data[:, idx], data[:, ot])
        if sim > res[1]:
            res[0] = idx
            res[1] = sim

    return res[0]


def selectAPs(srcData):
    # Normalize RSSI
    data = srcData.values[:, 0: st.AP_COUNT]
    data = abs(data)
    data[data > st.RSSI_THRESHOLD] = st.RSSI_THRESHOLD
    data /= st.RSSI_THRESHOLD
    tdata = np.asmatrix(data).T

    # Cluster
    cluRes = doCluster(tdata)
    cluDic = {}
    for i, val in enumerate(cluRes):
        if val in cluDic.keys():
            cluDic[val].append(i)
        else:
            cluDic[val] = [i]

    # Select AP
    selectIndex = []
    for apidxs in cluDic.items():
        if len(apidxs[1]) == 1:
            selectIndex.append(apidxs[0])
        else:
            selectIndex.append(doSelect(apidxs[1], data))
    return selectIndex


# srcData = pd.read_csv(st.TRAIDATA_PATH)
# srcData = srcData[(srcData.BUILDINGID == st.BUILDINGID)
#                   & (srcData.FLOOR == st.FLOORID)]
# data = srcData.values[:, 0: st.AP_COUNT]
# data = abs(data)
# data[data > st.RSSI_THRESHOLD] = st.RSSI_THRESHOLD
# data /= st.RSSI_THRESHOLD
# tdata = np.asmatrix(data).T

# dis = hcluster.distance.pdist(tdata, metric=calculateDistance)
# Z = hcluster.linkage(dis, method='average')

# hcluster.dendrogram(Z, color_threshold=0.1)

# res = hcluster.fcluster(Z, st.AP_CLU_THRESHOLD)
