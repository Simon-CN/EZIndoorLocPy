import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series

data = pd.read_csv('./data/uji/trainingData.csv')

# settings
building = 0
floor = 0
apcount = 520

powRange = [-50, -10]
losRange = [1.5, 6]
lonRange = []
latRange = []
spcOffset = 30

# preprocess
fdata = data[(data.BUILDINGID == building) & (data.FLOOR == floor)]

lonRange.append(min(fdata.LONGITUDE))
lonRange.append(max(fdata.LONGITUDE))
latRange.append(min(fdata.LATITUDE))
latRange.append(max(fdata.LATITUDE))

fdata.LATITUDE -= latRange[0]
fdata.LONGITUDE -= lonRange[0]

lonRange[0] = min(fdata.LONGITUDE) - spcOffset
lonRange[1] = max(fdata.LONGITUDE) + spcOffset
latRange[0] = min(fdata.LATITUDE) - spcOffset
latRange[1] = max(fdata.LATITUDE) + spcOffset

print(lonRange)
print(latRange)

# solve method


def calculateErr(po, pm, los, lat, lon, lato, lono):
    return abs(pm - po + 10 * los * np.log10(np.sqrt((lat - lato) ** 2 + (lon - lono) ** 2)))


def exhaustiveMethod(msrs):
    presult = []
    count = len(msrs)

    for po in range(powRange[0], powRange[1]):
        for los in np.arange(losRange[0], losRange[1], step=0.1):
            for lat in np.arange(latRange[0], latRange[1], 1):
                for lon in np.arange(lonRange[0], lonRange[1], 1):
                    res = 0
                    minErr = -1
                    for msr in msrs.iterrows():
                        res += calculateErr(po, msr[1][0],
                                            los, lat, lon, msr[1][1], msr[1][2])
                    if minErr == -1 or res < minErr:
                        minErr = res
                        presult = [minErr/count, po, los, lat, lon]
    return presult


# generate AP set
apset = {}

for index in range(1, apcount+1):
    key = "WAP%(apid)03d" % {'apid': index}
    msrs = fdata[fdata[key] < 0][[key, 'LATITUDE', 'LONGITUDE']]
    if len(msrs) == 0:
        continue
    print('------Calculate Ap ' + key + '------')
    apparam = exhaustiveMethod(msrs)
    print(apparam)
    apset[key] = apparam

print(apset)
