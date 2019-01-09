# %%
import random
import sys

import numpy as np
import pandas as pd

import initsolution as iis
import settings as st
import utils as ut


def randomSolutions(num):
    solutions = []
    for i in range(0, num):
        apParam = [[0] * 4 for i in range(st.AP_COUNT)]
        locations = [[0] * 2 for i in range(st.MSR_COUNT)]
        devDiff = {}
        for j in range(st.AP_COUNT):
            apParam[j] = np.asarray([random.randint(st.POWER_MIN, st.POWER_MAX), random.uniform(st.GAMMA_MIN, st.GAMMA_MAX), random.uniform(
                st.SPACE_RANGE[0], st.SPACE_RANGE[2]), random.uniform(st.SPACE_RANGE[3], st.SPACE_RANGE[1])])
        for k in range(st.MSR_COUNT):
            locations[k] = np.asarray([random.uniform(st.SPACE_RANGE[0], st.SPACE_RANGE[2]), random.uniform(
                st.SPACE_RANGE[3], st.SPACE_RANGE[1])])
        for dev in st.DEVICE_SET:
            devDiff[dev] = random.uniform(st.MIN_GAIN_DIFF, st.MAX_GAIN_DIFF)
        solutions.append([sys.maxsize, apParam, locations, devDiff])
    return solutions


def calculateFitness(msrs, solutions):
    for slu in solutions:
        err = 0
        count = 0
        apParam = slu[1]
        locations = slu[2]
        devDiff = slu[3]
        for i in range(0, st.MSR_COUNT):
            for j in range(0, st.AP_COUNT):
                if msrs[i][j] == st.DEFAULT_RSSI:
                    continue
                param = apParam[j]
                loc = locations[i]
                gain = devDiff[msrs[i, -2].astype(int)]
                err += abs(msrs[i][j] + gain - param[0] + 10 * param[1] * np.log10(np.sqrt(
                    (param[2]-loc[0])**2+(param[3]-loc[1])**2
                )))
                count += 1
        slu[0] = err / count

    solutions.sort(key=lambda x: x[0])
    return


def GASelect(oldSlu, newSlu):
    for i in range(0, int(len(oldSlu) * (st.SELECT_PERCENT / 100))):
        newSlu.append(oldSlu[i])
    return


def GAPick(oldSlu, newSlu):
    pickedIdx = random.sample(range(0, len(oldSlu)), int(
        len(oldSlu) * (st.PICK_PERCENT / 100)))
    for i in pickedIdx:
        newSlu.append(oldSlu[i])
    return


def mergeSolution(a, b):
    weight = random.random()
    newAp = [[0]*4 for i in range(st.AP_COUNT)]
    newLoc = [[0] * 2 for i in range(st.MSR_COUNT)]
    newGain = {}
    for i in range(0, st.AP_COUNT):
        newAp[i] = weight * a[1][i] + (1-weight) * b[1][i]
    for j in range(0, st.MSR_COUNT):
        newLoc[j] = weight * a[2][j] + (1 - weight) * b[2][j]
    for dev in st.DEVICE_SET:
        newGain[dev] = weight * a[3][dev] + (1 - weight) * b[3][dev]

    return [sys.maxsize, newAp, newLoc, newGain]


def GACross(oldSlu, newSlu):
    for i in range(0, int(len(oldSlu) * (st.CROSS_PERCENT/100))):
        pair = random.sample(range(0, len(oldSlu)), 2)
        newSlu.append(mergeSolution(oldSlu[pair[0]], oldSlu[pair[1]]))
    return


msrs = np.loadtxt("./data/uji/midfile/simpledata_%d_%d.txt" %
                  (st.BUILDINGID, st.FLOORID))
initSlu = ut.loadData(
    "./data/uji/midfile/init_solution_%d_%d.txt" % (st.BUILDINGID, st.FLOORID))

iDev = {}
for dev in initSlu[3]:
    iDev[int(dev)] = initSlu[3][dev]

initSlu[3] = iDev

for i in range(0, len(initSlu[1])):
    initSlu[1][i] = np.asarray(initSlu[1][i])[0:4]

for j in range(0, len(initSlu[2])):
    initSlu[2][j] = np.asarray(initSlu[2][j])


st.MSR_COUNT, col = msrs.shape
st.AP_COUNT = col - 9
st.DEVICE_SET = set(list(msrs[:, -2].astype(int)))

st.SPACE_RANGE = [min(msrs[:, -9] - st.POSITION_OFFSET), max(msrs[:, -8]) + st.POSITION_OFFSET,
                  max(msrs[:, -9]) + st.POSITION_OFFSET, min(msrs[:, -8]) - st.POSITION_OFFSET]

solutions = randomSolutions(st.SOLUTION_NUM)
solutions.append(initSlu)

loop = 0
while (loop < st.GA_ROUND):
    loop += 1
    print("loop %d" % loop)
    calculateFitness(msrs, solutions)
    print("min fit = %f" % solutions[0][0])
    newSolutions = randomSolutions(
        int(len(solutions) * (st.RANDOM_PERCENT/100)))
    GASelect(solutions, newSolutions)
    GACross(solutions, newSolutions)
    GAPick(solutions, newSolutions)
    solutions = newSolutions
