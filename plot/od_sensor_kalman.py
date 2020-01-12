#!/usr/bin/env python3
# encoding: utf-8

"""
    Copyright (C) 2019-2020  Andreas Kuster

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Andreas Kuster"
__copyright__ = "Copyright 2019-2020"
__license__ = "GPL"

from pykalman import KalmanFilter
import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt('data/calibration_sensor_data.csv', delimiter=',')
x = np.arange(len(data))



kf = KalmanFilter(initial_state_mean=2200000000, n_dim_obs=1)
(mean, covariance) = kf.filter(data)


kf = kf.em(data, n_iter=5)
(filtered_state_means, filtered_state_covariances) = kf.filter(data)
(smoothed_state_means, smoothed_state_covariances) = kf.smooth(data)





fig = plt.figure(figsize=(20,10))



fig = plt.figure()
ax = fig.add_subplot(111)

X = [val/2 for val in x]
ax.plot(X, data, label='raw sensor data')
#ax.plot(X, mean, label='kalman mean')
#ax.plot(X, filtered_state_means, label='em kalman filter mean')
#ax.plot(X, smoothed_state_means, label='em kalman smoothed mean')
ax.plot(X, smoothed_state_means, label='kalman filtered data')

ax.set_xlabel('Time [min]')
ax.set_ylabel('Light Intensity [Units]')
ax.set_title("Light Sensor Measurement Data")
ax.set_xlim(xmin=0)
plt.legend()
plt.show()






# credits:
# https://pykalman.github.io/
# https://medium.com/@jaems33/understanding-kalman-filters-with-python-2310e87b8f48




data_raw = np.genfromtxt('data/calibration_od_data.csv', delimiter=',')
data_x = [x[0] for x in data_raw]
data_y = [x[1] for x in data_raw]

kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
(mean, covariance) = kf.smooth(data_y)

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(data_x, data_y, label='reference od data')
ax.plot(data_x, mean, label='kalman filterered data')
ax.set_xlabel('Time [min]')
ax.set_ylabel('Optical Density [Units]')
ax.set_title("Reference Optical Density Measurement")
ax.set_xlim(xmin=0)
ax.set_ylim(ymin=0)

plt.legend()
plt.show()



from sklearn.svm import SVR

# extract sensor values at time points of the external od sensor measurements
X = np.array([data[int(x)*2] for x in data_x])

# define measured values
y = mean #data_y

clf = SVR(gamma='scale', C=10000.0, epsilon=0.01)
clf.fit(X.reshape(-1, 1), y)

"""
fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(data_x, data_y, label='external od sensor data')
ax.plot(data_x, X, label='online od sensor data')

plt.legend()
plt.show()
"""

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
ax.scatter(X, y, label="actual measurements")
ax.set_xlabel('Light Sensor Value [Units]')
ax.set_ylabel('Optical Density Value [Units]')
ax.set_title("Relation between Optical Density and Light Intensity")
plt.legend()
plt.show()


fig = plt.figure()
ax = fig.add_subplot(111)
x2 = np.arange(0, 2.2e9, 1e7)
y2 = [clf.predict(x.reshape(-1,1)) for x in x2]
ax.plot(x2, y2, label='predicted function')
ax.scatter(X, y, label="actual measurements")
ax.set_xlabel('Light Sensor Value [Units]')
ax.set_ylabel('Optical Density Value [Units]')
ax.set_title("Support Vector Regression")
plt.legend()
plt.show()


fig = plt.figure()
ax = fig.add_subplot(111)
x2 = np.arange(0, len(data))
y2 = [clf.predict(np.array(data[x]).reshape(-1, 1)) for x in x2]
ax.plot([val/2 for val in x2], np.array(y2).ravel())
ax.set_xlabel('Time [min]')
ax.set_ylabel('Optical Density [Units]')
ax.set_title("Sample Run: Growth Curve using the Calibrated Sensor")
#plt.legend()
plt.show()