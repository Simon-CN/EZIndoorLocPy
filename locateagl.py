import matplotlib.pyplot as plt
import numpy as np

from initsolution import solveLocation


def drawCircle(r, x, y):
    theta = np.arange(0, 2 * np.pi, 0.01)
    ax = x + r * np.cos(theta)
    ay = y + r * np.sin(theta)
    plt.plot(ax, ay)
    return


def drawCircleSeq(seq, loc):
    plt.figure(0)
    for ln in seq:
        drawCircle(ln[0], ln[1], ln[2])
    plt.plot(loc[0], loc[1], color='b', marker='o')
    plt.show()
    return


x = np.random.choice(np.arange(0, 50), 5)
y = np.random.choice(np.arange(0, 50), 5)

refx = 23
refy = 30

seq = []
for i in range(len(x)):
    dis = np.sqrt((refx - x[i]) ** 2 + (refy - y[i]) ** 2)
    seq.append([dis, x[i], y[i]])

loc = solveLocation(seq)

plt.figure(0)
plt.scatter(x, y)
plt.plot(loc[0], loc[1], color='r',marker='o')
for ln in seq:
    drawCircle(ln[0], ln[1], ln[2])

plt.show()

