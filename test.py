import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.rcParams["font.family"] = "Times New Roman"
d = np.arange(10, 1000, dtype=float)
d /= 10
gamma = np.arange(15, 60, 5)
p0 = 0

plt.figure(0)
gm = 30
p = p0 - 10 * float(gm / 10) * np.log10(d)
dp = -10 * float(gm / 10) / (d * np.log(10))
# ddp = 10 * float(gm / 10) / (d ** 2 * np.log(10))
# plt.plot(d, p,label='p')
plt.plot(d, dp)
plt.xlabel("Distance (m)")
plt.ylabel("d(p)/d(d)")
plt.text(0,0,'γ = 3')
# plt.plot(d,ddp)
plt.show()

# p = np.arange(-100, 0)
# gm = 2

# d = np.power(10, (-10 - p) / (10 * gm))
# dd = -(np.log(10) / (10 * gm)) * np.power(10, (-10 - p) / (10 * gm))

# plt.figure(0)
# plt.plot(p, d)
# plt.plot(p, dd)
# plt.show()
