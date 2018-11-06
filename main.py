import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame, Series

import ezimp as ez

data = pd.read_csv('./data/uji/trainingData.csv')

# settings
building = 0
floor = 0
apcount = 520

# filter
fdata = data[(data.BUILDINGID == building) & (
    data.FLOOR == floor)]

# generate AP set
apset = {}

for index in range(1, apcount+1):
    key = "WAP%(apid)03d" % {'apid': index}
    msrs = fdata[fdata[key] < 0][[key, 'LATITUDE', 'LONGITUDE']]
    if len(msrs) == 0:
        continue
    apparam = ez.solveByExhaustive(msrs)
    apset[str(index)] = apparam

print(apset)
