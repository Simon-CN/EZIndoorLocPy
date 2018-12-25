import numpy as np
import pandas as pd

import settings as st


def loadData():
    srcData = pd.read_csv(st.TRAIDATA_PATH)
    data = srcData[(srcData.BUILDINGID == st.BUILDINGID)
                   & (srcData.FLOOR == st.FLOORID)]

    row, col = data.shape
    apCount = col - 9

    vdata = data.values
    vdata[:, 0:apCount][vdata[:, 0:apCount] <
                        st.MIN_VALID_RSSI] = st.DEFAULT_RSSI

    del_row = []
    del_col = []

    for i in range(0, row):
        line = vdata[i, 0:apCount]
        if len(line[line != st.DEFAULT_RSSI]) == 0:
            del_row.append(i)

    for j in range(0, apCount):
        col = vdata[:, j]
        if len(col[col != st.DEFAULT_RSSI]) == 0:
            del_col.append(j)

    vdata = np.delete(vdata, del_row, 0)
    vdata = np.delete(vdata, del_col, 1)

    row, col = vdata.shape

    st.AP_COUNT = col - 9

    min_long = min(vdata[:, -9])
    min_lat = min(vdata[:, -8])
    max_long = max(vdata[:, -9])
    max_lat = max(vdata[:, -8])

    vdata[:, -9] -= min_long
    vdata[:, -8] -= min_lat

    datadf = pd.DataFrame(vdata)
    cols = {st.AP_COUNT: 'LONGITUDE', st.AP_COUNT+1: 'LATITUDE', st.AP_COUNT+2: 'FLOOR', st.AP_COUNT+3: 'BUILDINGID', st.AP_COUNT+4: 'SPACEID',
            st.AP_COUNT+5: 'RELATIVEPOSITION', st.AP_COUNT+6: 'USERID', st.AP_COUNT+7: 'PHONEID', st.AP_COUNT+8: 'TIMESTAMP'}
    datadf.rename(columns=cols, inplace=True)

    return datadf
