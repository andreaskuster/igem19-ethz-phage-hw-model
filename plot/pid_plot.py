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

import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(20,10))

data_temperature = np.genfromtxt('data/temperature39.csv', delimiter=',')
data_control_value = np.genfromtxt('data/control_value39.csv', delimiter=',')
data_kp = np.genfromtxt('data/kp39.csv', delimiter=',')
data_ki = np.genfromtxt('data/ki39.csv', delimiter=',')
data_kd = np.genfromtxt('data/kd39.csv', delimiter=',')


x = np.arange(len(data_temperature))

fig = plt.figure()
ax = fig.add_subplot(111)

X = [val/120.0 for val in x]
ax.plot(X, data_temperature, c='b', label='Temperature')
#ax.plot(x, data_control_value, c='g', label='Control Value')
#ax.plot(x, data_kp, c='k', label='Kp')
#ax.plot(x, data_ki, c='r', label='Ki')
#ax.plot(x, data_kd, c='m', label='Kd')
ax.plot(X,[38.7]*len(data_temperature), c='k', label='Target Temperature')
ax.set_xlabel('Time [min]')
ax.set_ylabel('Temperature [°C]')
ax.set_title("PID Controller Target Temperature: 38.7°C")

plt.legend()
plt.show()


