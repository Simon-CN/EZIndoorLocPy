import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import locimp as li

data = pd.read_csv('./data/sim/msrs.csv')
aps = pd.read_csv('./data/sim/aps.csv')

plt.figure(0)
plt.plot(data.LONGITUDE, data.LATITUDE, 'ro')
plt.plot(aps.lon, aps.lat, 'bo')

locres = []

for index, row in data.iterrows():
    locin = []
    for ap in range(0, 20):
        rssi = row['WAP%(api)03d' % {'api': ap + 1}]
        if rssi < 0:
            app = aps.iloc[ap]
            dis = np.power(10, (app['pow'] - rssi) / (10 * app.los))
            locin.append([dis, app.lat, app.lon])

plt.show()
