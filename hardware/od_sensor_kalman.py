from pykalman import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt('od.csv', delimiter=',')
x = np.arange(len(data))



kf = KalmanFilter(initial_state_mean=2200000000, n_dim_obs=1)
(mean, covariance) = kf.filter(data)


kf = kf.em(data, n_iter=5)
(filtered_state_means, filtered_state_covariances) = kf.filter(data)
(smoothed_state_means, smoothed_state_covariances) = kf.smooth(data)





fig = plt.figure(figsize=(20,10))



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




data_raw = np.genfromtxt('od_measurements.csv', delimiter=',')
data_x = [x[0] for x in data_raw]
data_y = [x[1] for x in data_raw]

kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
(mean, covariance) = kf.filter(data_y)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(data_x, data_y, label='raw sensor data')
ax.plot(data_x, mean, label='kalman filterered sensor data')

plt.legend()
plt.show()



from sklearn.svm import SVR

# extract sensor values at time points of the external od sensor measurements
X = np.array([data[int(x)*2] for x in data_x])

# define measured values
y = mean #data_y

clf = SVR(gamma='scale', C=10000.0, epsilon=0.01)
clf.fit(X.reshape(-1, 1), y)


fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(data_x, data_y, label='external od sensor data')
ax.plot(data_x, X, label='online od sensor data')

plt.legend()
plt.show()

"""
fig = plt.figure()
ax = fig.add_subplot(111)
x2 = np.arange(0, 2.2e9, 1e7)
y2 = [clf.predict(x.reshape(-1,1)) for x in x2]
ax.plot(x2, y2, label='predicted data')
plt.legend()
plt.show()
"""

fig = plt.figure()
ax = fig.add_subplot(111)
x2 = np.arange(0, 2.2e9, 1e7)
y2 = [clf.predict(x.reshape(-1,1)) for x in x2]
ax.plot(x2, y2, label='predicted function')
ax.scatter(X, y, label="actual measurements")
plt.legend()
plt.show()



fig = plt.figure()
ax = fig.add_subplot(111)
x2 = np.arange(0, len(data))
y2 = [clf.predict(np.array(data[x]).reshape(-1, 1)) for x in x2]
ax.plot(x2, np.array(y2).ravel(), label='predicted data')
plt.legend()
plt.show()