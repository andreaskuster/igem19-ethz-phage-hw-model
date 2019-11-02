import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 24})
plt.rcParams['figure.dpi'] = 300

data = np.genfromtxt('log/2019-10-27_23_17_23_od0.csv', delimiter=',')
control_data = np.genfromtxt('log/2019-10-27_19_25_53_growth_rate.csv', delimiter=',')

xx = np.arange(len(data))

fig = plt.figure(figsize=(16, 12))

ax1 = fig.add_subplot(111)
ax1.plot(xx, [x[1] for x in data], label='measurements OD')
ax1.plot(xx, [0.35]*len(data), label='target OD')

ax1.set_xlabel('time [min]')
ax1.set_ylabel('host concentration OD')
ax1.set_title("Constant Concentration Controller")
ax1.set_ylim([0, 0.6])
ax1.set_xlim(xmin=0.0, xmax=130)
ax1.legend(loc="upper left")

ax2 = ax1.twinx()
ax2.bar(xx, [x[2]/20.0 for x in control_data], label='pump')
ax2.set_ylim([0.0, 2.5])
ax2.set_ylabel("pumping activity")
ax2.legend()


plt.show()
