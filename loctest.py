from initsolution import solveLocation
import pandas as pd
import numpy as np
import settings as st
import utils as ut
import matplotlib.pyplot as plt
from scipy import stats

vldata = pd.read_csv(st.VALIDATION_PATH)
filtAP = np.loadtxt(st.MIDFILE_DIR+'filter_aps_%d_%d.txt' %
                    (st.BUILDINGID, st.FLOORID), dtype=int)
offset = np.loadtxt(st.MIDFILE_DIR+'offset_%d_%d.txt' %
                    (st.BUILDINGID, st.FLOORID))
model = ut.loadData(st.MIDFILE_DIR+'solution_%d_%d.json' %
                    (st.BUILDINGID, st.FLOORID))
devdiff = np.loadtxt(st.MIDFILE_DIR+'devicediff_%d_%d.txt' %
                     (st.BUILDINGID, st.FLOORID))

apMap = {}
for i in range(0, len(filtAP)):
    apMap[filtAP[i]] = i

devMap = {}
for dv in devdiff:
    devMap[int(dv[0])] = dv[1]

data = vldata.values
row, col = data.shape
apCount = col-9

res = []

for line in data:
    seq = []
    for i in range(0, apCount):
        if line[i] != st.DEFAULT_RSSI and i in apMap:
            param = model[1][apMap[i]]
            dis = np.power(
                10, -(line[i]+devMap[int(line[-2])]-param[0])/(10*param[1]))
            seq.append([dis, param[2], param[3]])
    if len(seq) == 0:
        res.append([0, 0])
    else:
        res.append(solveLocation(seq))

ref=data[:,(-9,-8)]

err=[]
for i in range(0,len(res)):
    err.append(np.sqrt((res[i][0]-ref[i][0])**2+(res[i][1]-ref[i][1])**2))

print(np.average(err))
plt.figure(0)
cdf = stats.cumfreq(err)
plt.plot(cdf[0])
plt.show()