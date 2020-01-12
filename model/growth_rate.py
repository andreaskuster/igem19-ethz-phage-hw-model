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

import os
import numpy as np
import functools

_CONVERSION_FACTOR = 8.0e8

# read data from the experiment
data = np.genfromtxt(os.path.join(os.path.dirname(__file__), 'growth_rate_ecor16_390.csv'), delimiter=',', dtype=(str, float, float))

# separate values
timestamps = [x[0] for x in data]
ods = [x[1] for x in data]
amounts = [x[2] for x in data]

# compute initial cell count
# initial volume: 400ml
# initial od: 0.35
initial_cell_count = 400.0 * _CONVERSION_FACTOR * 0.35

# convert pumping time to volume (1.2s pumping is equivalent to 1ml)
amounts = [x/1.2 for x in amounts]

# sum up the complete volume
total_amount = functools.reduce(lambda x, y: x + y, amounts, 0.0)

# total cell growth count
total_new_cells = total_amount * _CONVERSION_FACTOR * 0.35

# compute the time difference
delta_t = 33.0  # minutes #timestamps[-1] - timestamps[0]

# compute growth rate constant
growth_rate = (np.log(total_new_cells + initial_cell_count) - np.log(initial_cell_count)) / (np.log(2.0) * delta_t)

# print result
print("growth rate of ECOR16 at 39.0 degree celcius: {}".format(growth_rate))
