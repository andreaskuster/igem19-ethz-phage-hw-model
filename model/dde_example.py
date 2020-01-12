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
from ddeint import ddeint
from pylab import array, sin, linspace, subplots

tau = 30.0


def foo(t):
    if t < 10.0:
        return 0.0
    elif 10.0 <= t < 10.0 * np.pi:
        return 1.0
    else:
        return 10.0 * sin(t * 0.5)


def values_before_zero(t):
    return array([0.0, 0.0])


def model(Y, t):
    x, y = Y(t)
    x_tau, y_tau = Y(t - tau)
    return array([foo(t), x_tau])


tt = linspace(0, 100, 1000)
yy = ddeint(model, values_before_zero, tt)

fig, ax = subplots(1, figsize=(8, 4))

ax.plot(tt, [x[0] for x in yy], label="trace1")
ax.plot(tt, [x[1] for x in yy], label="trace2")
fig.legend(loc='upper center', borderaxespad=2.0)
fig.show()
