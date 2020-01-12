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

from ddeint import ddeint
from pylab import array, linspace, subplots, subplot


def values_before_zero(t):
    return array([10000.0, 1.0])


def model(Y, t):
    x, y = Y(t)
    tot = x + y
    return array([
        0.04*x - 0.01*x/tot,
        0.06*y - 0.01*y/tot
    ])


tt0 = linspace(0, 6*1e1, 1000)
tt1 = linspace(0, 6*1e2, 1000)

yy0 = ddeint(model, values_before_zero, tt0)
yy1 = ddeint(model, values_before_zero, tt1)


fig, (ax0, ax1) = subplots(2, figsize=(8, 6))

ax0.plot(tt0, [x[0] for x in yy0], label="slower growing, quantitatively more")
ax0.ticklabel_format(axis='y', style='sci', scilimits=(2,3))
ax0.plot(tt0, [x[1] for x in yy0], label="faster growing, quantitatively less")
ax0.set_xlabel('Time [min]')
ax0.set_ylabel('Number of Phages')
ax0.legend(loc='upper left', borderaxespad=2.0)


ax1.plot(tt1, [x[0] for x in yy1], label="slower growing, quantitatively more")
ax1.plot(tt1, [x[1] for x in yy1], label="faster growing, quantitatively less")
ax1.set_xlabel('Time [min]')
ax1.set_ylabel('Number of Phages')
ax1.legend(loc='upper left', borderaxespad=2.0)
fig.show()
