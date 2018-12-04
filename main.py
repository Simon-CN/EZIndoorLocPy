import numpy as np
import pandas as pd

import apselect as aps
import devicediff as dif
import locselect as locs
import settings as st
import utils as ut

# Load Data
srcData = pd.read_csv(st.TRAIDATA_PATH)
data = srcData[(srcData.BUILDINGID == st.BUILDINGID)
               & (srcData.FLOOR == st.FLOORID)]

# Calculate RSSI Gain
devdiff = dif.calculateDeviceDiff(data)
ut.saveNPtoFile("./data/uji/midfile/devicediff_%d_%d.txt" %
                (st.BUILDINGID, st.FLOORID), devdiff)

# Simplify Data
selectedAP = aps.selectAPs(data)
selectedLoc = locs.selectLocs(data)
sData = data.values[selectedLoc, :][:, selectedAP]
msrInfo = data.values[selectedLoc, st.LONGITUDE_INDEX:]
mgData = np.hstack((sData, msrInfo))
ut.saveNPtoFile("./data/uji/midfile/simpledata_%d_%d.txt" %
                (st.BUILDINGID, st.FLOORID), mgData)

# Solve LDPL
