import numpy as np
import random
import settings as st


def randomInit(idx, seq, apParam):
    return


def trilaterate(idx, apParam, msrs, locations):
    return


devdf = np.loadtxt('./data/uji/midfile/devicediff_0_0.txt')
msrs = np.loadtxt('./data/uji/midfile/simpledata_0_0.txt')

devdir = {}
for devl in devdf:
    devdir[devl[0]] = devl[1]

row, col = msrs.shape
apCount = col - 9

for line in msrs:
    for i in range(0, apCount):
        if line[i] != 100:
            line[i] += devdir[line[-2]]

knownLoc = random.sample(range(0, row), (int)(row * st.KNOWN_LOC_PERCENT))
knownLocSet = set(knownLoc)
unknownLocSet = set(range(0, row)).difference(knownLocSet)

knownApSet = set()
unknownApSet = set(range(0, apCount)).difference(knownApSet)

apParam = {}
locations = {}

level = 5
while level > 0:
    changed = False
    for i in unknownApSet:
        msrSeq = msrs[list(knownLocSet)]
        msrSeq = msrSeq[msrSeq[:, i] != 100]
        if len(msrSeq) < level:
            continue
        randomInit(i, msrSeq[:, (i, -9, -8)], apParam)
        knownApSet.add(i)
        unknownApSet.remove(i)
        changed = True

    if not changed:
        level -= 1
        continue

    for j in unknownLocSet:
        msrLine = msrs[j]
        msr = []
        for mi in range(0, apCount):
            if msrLine[mi] == 100:
                continue
            if mi not in knownApSet:
                continue
            msr.append([mi, msrLine[mi]])

        if len(msr) < 3:
            continue
        trilaterate(j, apParam, msr, locations)
        knownLocSet.add(j)
        unknownLocSet.remove(j)
