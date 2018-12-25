# %%
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
# %% Load Data
data = ld.loadData()

# %%Calculate RSSI Gain
devdiff = dif.calculateDeviceDiff(data)
ut.saveNPtoFile("./data/uji/midfile/devicediff_%d_%d.txt" %
                (st.BUILDINGID, st.FLOORID), devdiff)

# %% Simplify Data
selectedAP = aps.selectAPs(data)
selectedLoc = locs.selectLocs(data)
sData = data.values[selectedLoc, :][:, selectedAP]
msrInfo = data.values[selectedLoc, -9:]
mgData = np.hstack((sData, msrInfo))
ut.saveNPtoFile("./data/uji/midfile/simpledata_%d_%d.txt" %
                (st.BUILDINGID, st.FLOORID), mgData)

# %% Solve LDPL
row, col = mgData.shape
knownLoc = random.sample(range(0, row), (int)(row * st.KNOWN_LOC_PERCENT))
initAP,initLoc = inis.ERSGA(mgData, knownLoc, devdiff)

print(initAP)
print(initLoc)