# %%
import numpy as np
import pandas as pd

import apselect as aps
import devicediff as dif
import locselect as locs
import settings as st

# %% ReadData
srcData = pd.read_csv(st.TRAIDATA_PATH)
data = srcData[(srcData.BUILDINGID == st.BUILDINGID)
               & (srcData.FLOOR == st.FLOORID)]

# %% Calculate Device Difference
devdiff = dif.calculateDeviceDiff(data)

# %% Simplify Data Set
selectedAP = aps.selectAPs(data)
selectedLoc = locs.selectLocs(data)
sData = data.values[selectedLoc, selectedAP]
msrInfo = data.values[selectedLoc, st.LONGITUDE_INDEX: st.TIMESTAMP_INDEX]

# %% Solve LDPL
