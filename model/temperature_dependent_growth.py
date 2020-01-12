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


def concentration_to_od(concentration: float) -> float:
    # concentration in cells/ml
    return concentration / 8.0e8


def od_to_concentration(od: float) -> float:
    # concentration in cells/ml
    return 8.0e8 * od  # assumption: od is linear, approximately valid in the interval [0.0, 1.0]


def values_before_zero(t):
    return array([0.2, 0.2, 0.2])


def model(Y, t):
    x0, x1, x2 = Y(t)
    return array([
        0.01*x0,
        0.02*x1,
        0.03*x2
    ])


tt0 = linspace(0, 100, 1000)

yy0 = ddeint(model, values_before_zero, tt0)

fig, ax0 = subplots(1, figsize=(8, 6))

ax0.plot(tt0, [concentration_to_od(x[0]) for x in yy0], label="T=21.0")
ax0.ticklabel_format(axis='y', style='sci', scilimits=(2, 3))
ax0.plot(tt0, [concentration_to_od(x[1]) for x in yy0], label="T=30.0")
ax0.plot(tt0, [concentration_to_od(x[2]) for x in yy0], label="T=39.0")

ax0.set_xlabel('Time [min]')
ax0.set_ylabel('Host Concentration')
ax0.legend(loc='upper left', borderaxespad=2.0)
ax0.set_xlim(xmin=0)


fig.show()
