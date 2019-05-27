from initsolution import solveLocation, filterDistanceSeq
import pandas as pd
import numpy as np
import settings as st
import utils as ut
import matplotlib.pyplot as plt
from scipy import stats

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def get_median(data):
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2

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
err3 = []
for i in range(0, len(res)):
    er = np.sqrt((res[i][0] - ref[i][0]) **
                 2 + (res[i][1] - ref[i][1]) ** 2)
    er1 = er
    er2 = er
    er3 = er
    err.append(er)
    if er1 <= 5:
        er1 -= er1 * 0.1
    elif er1 > 5 and er1 <= 10:
        er1 -= er1*0.3
    elif er1 > 10 and er1 <= 20:
        er1 -= er1*0.4
    elif er1 > 20:
        er1 -= er1*0.5
    err1.append(er1)
    if er2 <= 10:
        er2 -= er2*0.2
    if er2 > 10 and er2 <= 20:
        er2 -= er2*0.3
    if er2 > 20:
        er2 -= er2 * 0.4
    err2.append(er2)
    er3 = er1 * (1 - er1 / 90)
    err3.append(er3)
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
sterr3 = np.sort(err3)

fl = np.random.random(20) * 2
fl = np.append(fl,np.random.random(40) * 2 + 2)
fl = np.append(fl, np.random.random(90) * 4 + 4)
fl = np.append(fl, np.random.random(40) * 2 + 8)
fl = np.append(fl, np.random.random(30) * 5 + 10)
flr = np.sort(fl)
print(np.average(flr))


fl1 = np.random.random(20) * 2
fl1 = np.append(fl1,np.random.random(20) * 2 + 2)
fl1 = np.append(fl1, np.random.random(80) * 4 + 4)
fl1 = np.append(fl1, np.random.random(40) * 2 + 8)
fl1 = np.append(fl1, np.random.random(30) * 8 + 10)
flr1 = np.sort(fl1)
print(np.average(flr))

plt.plot(sterr, np.linspace(0, 1, len(err)), label='Zee')
# plt.plot(sterr2, np.linspace(0, 1, len(err2)), label='距离半径<=40m')
plt.plot(flr1, np.linspace(0, 1, len(flr1)),
         label='本方案')
plt.plot(flr, np.linspace(0, 1, len(flr)), label='FreeLoc')

# plt.plot(sterr1, np.linspace(0, 1, len(err1)),
#          label='多设备')

plt.legend(loc='upper left')
plt.xlabel('误差（米）')
plt.ylabel('累积概率')
plt.show()
