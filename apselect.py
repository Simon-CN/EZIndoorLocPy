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
    return 1 - sm / count


srcData = pd.read_csv(st.TRAIDATA_PATH)
data = srcData.values[:, 0: st.AP_COUNT]

data = abs(data)
data[data > st.RSSI_THRESHOLD] = st.RSSI_THRESHOLD
data /= st.RSSI_THRESHOLD
tdata = np.asmatrix(data).T

dis = hcluster.distance.pdist(tdata, metric=calculateDistance)
