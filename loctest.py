from initsolution import solveLocation, filterDistanceSeq
import pandas as pd
import numpy as np
import settings as st
import utils as ut
import matplotlib.pyplot as plt
from scipy import stats


def drawCircle(r, x, y):
    theta = np.arange(0, 2 * np.pi, 0.01)
    ax = x + r * np.cos(theta)
    ay = y + r * np.sin(theta)
    plt.plot(ax, ay)
    return


def drawCircleSeq(seq, loc):
    plt.figure(0)
    for ln in seq:
        drawCircle(ln[0], ln[1], ln[2])
    plt.plot(loc[0], loc[1], color='b', marker='o')
    plt.show()
    return


vldata = pd.read_csv(st.VALIDATION_PATH)
filtAP = np.loadtxt(st.MIDFILE_DIR+'filter_aps_%d_%d.txt' %
                    (st.BUILDINGID, st.FLOORID))
model = ut.loadData(st.MIDFILE_DIR+'solution_%d_%d.json' %
                    (st.BUILDINGID, st.FLOORID))
devdiff = np.loadtxt(st.MIDFILE_DIR+'devicediff_%d_%d.txt' %
                     (st.BUILDINGID, st.FLOORID))

vldata = vldata[(vldata.BUILDINGID == st.BUILDINGID)
                & (vldata.FLOOR == st.FLOORID)]

filtAP.astype(int)
apMap = {}
for i in range(0, len(filtAP)):
    apMap[filtAP[i]] = i

devMap = {0: 0}
# devMap = {}
# for dv in devdiff:
#     devMap[int(dv[0])] = dv[1]

data = vldata.values
row, col = data.shape
apCount = col-9

res = []

for line in data:
    seq = []
    for i in range(0, apCount):
        if line[i] != st.DEFAULT_RSSI and i in apMap:
            param = model[1][apMap[i]]
            a = int(line[-2])
            g = 0
            if a in devMap:
                g = devMap[a]
            dis = np.power(
                10, -(line[i]+g-param[0])/(10*param[1]))
            seq.append([dis, param[2], param[3]])
    if len(seq) == 0:
        res.append([0, 0])
    else:
        seq = filterDistanceSeq(seq)
        loc = solveLocation(seq)
        res.append(loc)
        # drawCircleSeq(seq,loc)
ref = data[:, (-9, -8)]

err = []
for i in range(0, len(res)):
    err.append(np.sqrt((res[i][0] - ref[i][0]) **
                       2 + (res[i][1] - ref[i][1]) ** 2))
    print(ref[i])
    print(res[i])
    print("...")

print(err)
print("avg")
print(np.average(err))
plt.figure(0)
sterr = np.sort(err)
plt.plot(np.linspace(0, 1, len(err)), sterr)
plt.show()
