import numpy as np
import pandas as pd

import settings as st
import utils as ut


def loadData():
    srcData = pd.read_csv(st.TRAIDATA_PATH)
    data = srcData[(srcData.BUILDINGID == st.BUILDINGID)
                   & (srcData.FLOOR == st.FLOORID)]
    row, col = data.shape
    apCount = col - 9

    apMap = list(range(0, apCount))

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
    apMap = np.delete(apMap, del_col, 0)

    row, col = vdata.shape

    st.AP_COUNT = col - 9

    datadf = pd.DataFrame(vdata)
    cols = {st.AP_COUNT: 'LONGITUDE', st.AP_COUNT+1: 'LATITUDE', st.AP_COUNT+2: 'FLOOR', st.AP_COUNT+3: 'BUILDINGID', st.AP_COUNT+4: 'SPACEID',
            st.AP_COUNT+5: 'RELATIVEPOSITION', st.AP_COUNT+6: 'USERID', st.AP_COUNT+7: 'PHONEID', st.AP_COUNT+8: 'TIMESTAMP'}
    datadf.rename(columns=cols, inplace=True)

    return datadf, apMap
