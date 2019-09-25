import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(20,10))

data_temperature = np.genfromtxt('temperature22.csv', delimiter=',')
data_control_value = np.genfromtxt('control_value22.csv', delimiter=',')
data_kp = np.genfromtxt('kp22.csv', delimiter=',')
data_ki = np.genfromtxt('ki22.csv', delimiter=',')
data_kd = np.genfromtxt('kd22.csv', delimiter=',')


x = np.arange(len(data_temperature))

fig = plt.figure()
ax = fig.add_subplot(111)


ax.plot(x, data_temperature, c='b', label='Temperature')
#ax.plot(x, data_control_value, c='g', label='Control Value')
#ax.plot(x, data_kp, c='k', label='Kp')
#ax.plot(x, data_ki, c='r', label='Ki')
#ax.plot(x, data_kd, c='m', label='Kd')
ax.plot(x,[22.0]*len(data_temperature), c='k', label='Target Temperature')

plt.legend()
plt.show()


