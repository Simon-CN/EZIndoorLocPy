import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

# settings
width = 80
height = 40
apcount = 80
mscount = 1000
vlcount = 200
devcount = 1

# gen dev
devs = []
if devcount == 1:
    devs.append(0)
else:
    for i in range(0, devcount):
        devs.append(random.randint(-20, 20))
print(devs)
# gen aps
apparam = {'lat': np.random.randint(1, width + 1, apcount),
           'lon': np.random.randint(1, height + 1, apcount),
           'pow': np.random.randint(-50, -10, apcount),
           'los': np.random.randint(15, 60, apcount) / 10}

aps = pd.DataFrame(apparam)
print(aps)

# gen msr
mspos = pd.DataFrame({'lat': np.random.randint(1, width + 1, mscount),
                      'lon': np.random.randint(1, height + 1, mscount)})

msrs = []
seq = 0
ct = 0
phoneids = []
for row in mspos.iterrows():
    rssi = {}
    phoneids.append(seq)
    for index, app in aps.iterrows():
        dis = np.sqrt((app.lat - row[1].lat) **
                      2 + (app.lon - row[1].lon) ** 2)
        rs = app['pow'] - 10 * app.los * \
            np.log10(dis) + np.random.normal() + devs[seq]
        if rs >= 0:
            rs = app['pow']
        elif rs < -70:
            rs = 100

        rssi["WAP%(api)03d" % {'api': index+1}] = rs
    msrs.append(rssi)
    ct += 1
    if ct > mscount / devcount:
        seq += 1
        ct = 0

msrsdf = pd.DataFrame(msrs)
msrsdf['LONGITUDE'] = mspos.lon
msrsdf['LATITUDE'] = mspos.lat
msrsdf['FLOOR'] = np.zeros(mscount, np.int8)
msrsdf['BUILDINGID'] = np.zeros(mscount, np.int8)
msrsdf['SPACEID'] = np.zeros(mscount, np.int8)
msrsdf['RELATIVEPOSITION'] = np.zeros(mscount, np.int8)
msrsdf['USERID'] = np.zeros(mscount, np.int8)
msrsdf['PHONEID'] = pd.DataFrame(phoneids)
msrsdf['TIMESTAMP'] = np.zeros(mscount, np.int8)


print(msrsdf)

# gen test
vlpos = pd.DataFrame({'lat': np.random.randint(1, width + 1, vlcount),
                      'lon': np.random.randint(1, height + 1, vlcount)})

msrs = []
seq = 0
ct = 0
phoneids = []
try:
    for row in vlpos.iterrows():
        rssi = {}
        phoneids.append(seq)
        for index, app in aps.iterrows():
            dis = np.sqrt((app.lat - row[1].lat) **
                          2 + (app.lon - row[1].lon) ** 2)
            rs = app['pow'] - 10 * app.los * \
                np.log10(dis) + np.random.normal() + devs[seq]
            if rs < -70:
                rs = 100
            rssi["WAP%(api)03d" % {'api': index+1}] = rs
        msrs.append(rssi)
        ct += 1
        if ct > vlcount/devcount:
            seq += 1
            ct = 0
except Exception as e:
    print(e)
vlmsrsdf = pd.DataFrame(msrs)
vlmsrsdf['LONGITUDE'] = mspos.lon
vlmsrsdf['LATITUDE'] = mspos.lat
vlmsrsdf['FLOOR'] = np.zeros(vlcount, np.int8)
vlmsrsdf['BUILDINGID'] = np.zeros(vlcount, np.int8)
vlmsrsdf['SPACEID'] = np.zeros(vlcount, np.int8)
vlmsrsdf['RELATIVEPOSITION'] = np.zeros(vlcount, np.int8)
vlmsrsdf['USERID'] = np.zeros(vlcount, np.int8)
vlmsrsdf['PHONEID'] = pd.DataFrame(phoneids)
vlmsrsdf['TIMESTAMP'] = np.zeros(vlcount, np.int8)


print(vlmsrsdf)

# save to file
aps.to_csv('./data/sim/aps.csv', index=False)
msrsdf.to_csv('./data/sim/trainingData.csv', index=False)
vlmsrsdf.to_csv('./data/sim/validationData.csv', index=False)
np.savetxt('./data/sim/dev.txt', np.asarray(devs))
