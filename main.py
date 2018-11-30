import pandas as pd
import numpy as np
import settings as st
import devicediff as dif


# ReadData
srcData = pd.read_csv(st.TRAIDATA_PATH)
data = srcData[(srcData.BUILDINGID == st.BUILDINGID)
                & (srcData.FLOOR == st.FLOORID)]

# Calculate Device Difference
devdiff = dif.calculateDeviceDiff(data)
