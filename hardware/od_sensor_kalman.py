from pykalman import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt('od.csv', delimiter=',')

kf = KalmanFilter(initial_state_mean=2200000000, n_dim_obs=1)
(mean, covariance) = kf.filter(data)


kf = kf.em(data, n_iter=5)
(filtered_state_means, filtered_state_covariances) = kf.filter(data)
(smoothed_state_means, smoothed_state_covariances) = kf.smooth(data)





fig = plt.figure(figsize=(20,10))


x = np.arange(len(data))

fig = plt.figure()
ax = fig.add_subplot(111)


ax.plot(x, data, label='raw sensor data')
ax.plot(x, mean, label='kalman mean')
ax.plot(x, filtered_state_means, label='em kalman filter mean')
ax.plot(x, smoothed_state_means, label='em kalman smoothed mean')


plt.legend()
plt.show()






# credits:
# https://pykalman.github.io/
# https://medium.com/@jaems33/understanding-kalman-filters-with-python-2310e87b8f48




data = np.genfromtxt('od_measurements.csv', delimiter=',')

fig = plt.figure()
ax = fig.add_subplot(111)


ax.plot([x[0] for x in data], [x[1] for x in data], label='raw sensor data')

plt.legend()
plt.show()