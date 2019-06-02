import os

import numpy as np
import pandas as pd

import settings as st

dir = './data/f7/'
umdir = dir + 'unmarked'
mdir = dir + 'marked'
vmdir = dir + 'validation'

speAPSet = {'28:2c:b2:3F:19:f4', '34:96:72:38:88:ac',
            'ec:26:ca:f3:ee:9c', '14:e6:e4:44:d7:0c'}

apSet = set()
msrs = []
vmsrs = []

apIndex = 0
umfiles = os.listdir(umdir)
for f in umfiles:
    pt = os.path.join(umdir, f)
    if os.path.isfile(pt) and os.path.splitext(pt)[1] == '.txt':
        lines = open(pt, 'r').readlines()
        poi = [-1, -1]
        for i in range(1, len(lines)):
            line = lines[i].split(',')
            tmp = {}
            stp = len(line)
            if stp % 2 == 0:
                continue
            for j in range(1, stp, 2):
                if line[j] in speAPSet:
                    tmp[line[j]] = int(line[j + 1])
                    apSet.add(line[j])
            if len(tmp)>0:
                msrs.append([line[0], poi, tmp])


mfiles = os.listdir(mdir)
for f in mfiles:
    pt = os.path.join(mdir, f)
    if os.path.isfile(pt) and os.path.splitext(pt)[1] == '.txt':
        lines = open(pt, 'r').readlines()
        poi = lines[0].split(',')
        poi = [float(poi[0]), float(poi[1])]
        for i in range(1, len(lines)):
            line = lines[i].split(',')
            tmp = {}
            stp = len(line)
            if stp % 2 == 0:
                continue
            for j in range(1, stp, 2):
                if line[j] in speAPSet:
                    tmp[line[j]] = int(line[j + 1])
                    apSet.add(line[j])
            if len(tmp)>0:
                msrs.append([line[0], poi, tmp])

vfiles = os.listdir(vmdir)
for f in vfiles:
    pt = os.path.join(vmdir, f)
    if os.path.isfile(pt) and os.path.splitext(pt)[1] == '.txt':
        lines = open(pt, 'r').readlines()
        poi = lines[0].split(',')
        poi = [float(poi[0]), float(poi[1])]
        for i in range(1, len(lines)):
            line = lines[i].split(',')
            tmp = {}
            stp = len(line)
            if stp % 2 == 0:
                continue
            for j in range(1, stp, 2):
                if line[j] in speAPSet:
                    tmp[line[j]] = int(line[j + 1])
                    apSet.add(line[j])
            if len(tmp)>0:
                vmsrs.append([line[0], poi, tmp])


apMap = {}

for mac in apSet:
    apMap[mac] = apIndex
    apIndex += 1


st.AP_COUNT = len(apSet)

dataset = []
for msr in msrs:
    line = np.zeros(st.AP_COUNT + 9)
    line[-1] = int(msr[0])
    line[-9] = msr[1][0]
    line[-8] = msr[1][1]
    for mr in msr[2].items():
        line[apMap[mr[0]]] = mr[1]
    dataset.append(line)

vdataset = []
for msr in vmsrs:
    line = np.zeros(st.AP_COUNT + 9)
    line[-1] = int(msr[0])
    line[-9] = msr[1][0]
    line[-8] = msr[1][1]
    for mr in msr[2].items():
        line[apMap[mr[0]]] = mr[1]
    vdataset.append(line)

dataset = np.asarray(dataset)
dataset[:, 0: st.AP_COUNT][dataset[:, 0: st.AP_COUNT] == 0] = st.DEFAULT_RSSI
poi = dataset[:, (-9, -8)]
poi[poi != -1] = poi[poi != -1] / st.MAP_SCALE
dataset[:, (-9, -8)] = poi
ddf = pd.DataFrame(dataset)
cols = {st.AP_COUNT: 'LONGITUDE', st.AP_COUNT+1: 'LATITUDE', st.AP_COUNT+2: 'FLOOR', st.AP_COUNT+3: 'BUILDINGID', st.AP_COUNT+4: 'SPACEID',
        st.AP_COUNT+5: 'RELATIVEPOSITION', st.AP_COUNT+6: 'USERID', st.AP_COUNT+7: 'PHONEID', st.AP_COUNT+8: 'TIMESTAMP'}
ddf.rename(columns=cols, inplace=True)
ddf.to_csv(dir + 'trainingData.csv', index=False)

vdataset = np.asarray(vdataset)
vdataset[:, 0: st.AP_COUNT][vdataset[:, 0: st.AP_COUNT] == 0] = st.DEFAULT_RSSI
vdataset[:, (-9, -8)] = vdataset[:, (-9, -8)] / st.MAP_SCALE
vddf = pd.DataFrame(vdataset)
vddf.rename(columns=cols, inplace=True)
vddf.to_csv(dir + 'validationData.csv', index=False)
