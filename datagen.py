import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# settings
width = 40
height = 40
apcount = 20
mscount = 200

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
for row in mspos.iterrows():
    rssi = {}
    for index, app in aps.iterrows():
        dis = np.sqrt((app.lat - row[1].lat) **
                      2 + (app.lon - row[1].lon) ** 2)
        rs = app['pow'] - 10 * app.los * np.log10(dis) + np.random.normal()
        if rs < -70:
            rs = 100
        rssi["WAP%(api)03d" % {'api': index+1}] = rs
    msrs.append(rssi)

msrsdf = pd.DataFrame(msrs)
msrsdf['LONGITUDE'] = mspos.lon
msrsdf['LATITUDE'] = mspos.lat
msrsdf['BUILDINGID'] = np.zeros(mscount, np.int16)
msrsdf['FLOOR'] = np.zeros(mscount, np.int16)
print(msrsdf)


# save to file
aps.to_csv('./data/sim/aps.csv', index=False)
msrsdf.to_csv('./data/sim/msrs.csv', index=False)
