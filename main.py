# %%
import json
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import apselect as aps
import dataload as ld
import devicediff as dif
import gaprocess as ga
import initsolution as inis
import locselect as locs
import settings as st
import utils as ut

# Load Data
data, apMap = ld.loadData()

# Calculate RSSI Gain
devdiff = dif.calculateDeviceDiff(data)
ut.saveNPtoFile(st.MIDFILE_DIR+"devicediff_%d_%d.txt" %
                (st.BUILDINGID, st.FLOORID), devdiff)

# Simplify Data
selectedAP = aps.selectAPs(data)
selectedLoc = locs.selectLocs(data)
sData = data.values[selectedLoc, :][:, selectedAP]
msrInfo = data.values[selectedLoc, -9:]
mgData = np.hstack((sData, msrInfo))
apMap = apMap[selectedAP]
ut.saveNPtoFile(st.MIDFILE_DIR+"simpledata_%d_%d.txt" %
                (st.BUILDINGID, st.FLOORID), mgData)
ut.saveNPtoFile(st.MIDFILE_DIR+"filter_aps_%d_%d.txt" %
                (st.BUILDINGID, st.FLOORID), apMap)

# Solve LDPL
# mgData = data
row, col = mgData.shape


knownLoc = []
for i in range(0, len(mgData)):
    if mgData[i][-9] != -1 or mgData[i][-8] != -1:
        knownLoc.append(i)

initSolution = inis.ERSGA(mgData, knownLoc, devdiff)
ut.saveToFile(st.MIDFILE_DIR+"init_solution_%d_%d.txt" %
              (st.BUILDINGID, st.FLOORID), initSolution)
optslu = ga.GASolve(mgData, initSolution)
ut.saveToFile(st.MIDFILE_DIR+'solution_%d_%d.json' %
              (st.BUILDINGID, st.FLOORID), optslu)
