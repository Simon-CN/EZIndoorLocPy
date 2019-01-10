import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import apselect as aps
import dataload as ld
import devicediff as dif
import locselect as locs
import settings as st
import utils as ut
import initsolution as inis
import random
import json

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
row, col = mgData.shape
knownLoc = random.sample(range(0, row), (int)(row * st.KNOWN_LOC_PERCENT))
initSolution = inis.ERSGA(mgData, knownLoc, devdiff)
ut.saveToFile(st.MIDFILE_DIR+"init_solution_%d_%d.txt" %
              (st.BUILDINGID, st.FLOORID), initSolution)
