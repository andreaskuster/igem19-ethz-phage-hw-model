import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(20,10))

data_1os = np.genfromtxt('od_1os.csv', delimiter=',')
data_4os = np.genfromtxt('od_4os.csv', delimiter=',')
data_8os = np.genfromtxt('od_8os.csv', delimiter=',')
data_16os = np.genfromtxt('od_16os.csv', delimiter=',')

x = np.arange(len(data_1os))

fig = plt.figure()
ax = fig.add_subplot(111)


ax.plot(x, data_1os, label='OS=1')
ax.plot(x, data_4os, label='OS=4')
ax.plot(x, data_8os, label='OS=8')
ax.plot(x, data_16os, label='OS=16')


plt.legend()
plt.show()


