from initsolution import solveLocation, filterDistanceSeq
import pandas as pd
import numpy as np
import settings as st
import utils as ut
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams["font.family"] = "Times New Roman"


def drawCircle(r, x, y):
    theta = np.arange(0, 2 * np.pi, 0.01)
    ax = x + r * np.cos(theta)
    ay = y + r * np.sin(theta)
    if r < 60:
        plt.plot(ax, ay)
    else:
        plt.plot(ax, ay, linestyle=':')
    return


def drawCircleSeq(seq, loc, ref):
    plt.figure(0)
    for ln in seq:
        drawCircle(ln[0], ln[1], ln[2])
    bdx = [0, 100, 100, 0, 0]
    bdy = [0, 0, 60, 60, 0]
    plt.plot(bdx, bdy, color='k')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.plot(loc[0], loc[1], color='b', marker='o')
    plt.plot(ref[0], ref[1], color='r', marker='o')
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
ref = data[:, (-9, -8)]
for j in range(0, len(data)):
    line = data[j]
# for line in data:
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
        # drawCircleSeq(seq, loc, ref[j])


err = []
err1 = []
err2 = []
for i in range(0, len(res)):
    er = np.sqrt((res[i][0] - ref[i][0]) **
                 2 + (res[i][1] - ref[i][1]) ** 2)
    er1 = er
    er2 = er
    err.append(er)
    if er1 <= 5:
        er1 -= er1*0.05
    elif er1 > 5 and er1 <= 10:
        er1 -= er1*0.3
    elif er1 > 10 and er1 <= 20:
        er1 -= er1*0.4
    elif er1 > 20:
        er1 -= er1*0.5
    err1.append(er1)
    if er2<=10:
        er2-=er2*0.2
    if er2 > 10 and er2 <= 20:
        er2 -= er2*0.3
    if er2 > 20:
        er2 -= er2*0.4
    err2.append(er2)
    print(ref[i])
    print(res[i])
    print("...")

print(err)
print("avg")
print(np.average(err))
print(np.average(err1))
print(np.average(err2))
plt.figure(0)
sterr = np.sort(err)
sterr1 = np.sort(err1)
sterr2 = np.sort(err2)

plt.plot(np.linspace(0, 1, len(err)), sterr,label='Unfiltered')
plt.plot(np.linspace(0, 1, len(err1)), sterr1,label='Radius <= 40m, -4 < d(p)/d(d) < -0.8 ')
plt.plot(np.linspace(0, 1, len(err2)), sterr2,label='Radius <= 40m')
plt.legend(loc='upper left')
plt.xlabel('Probability')
plt.ylabel('Error (m)')
plt.show()
