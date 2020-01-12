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

from typing import List


class Host():

        
    def __init__(self,
                 yield_coeff: float,
                 g_max: float,
                 half_sat: float,
                 death_rate: float,
                 c0: int = 1,
                 t_dep = lambda: 1.0):
        """

        :param g_max:
        :param c0:
        :param yield_coeff:
        :param half_sat:
        :param death_rate:
        :param t_dep:
        """
        self.c0 = c0
        self.g_max = g_max       
        self.yield_coeff = yield_coeff
        self.half_sat = half_sat
        self.death_rate = death_rate
        self.t_dep = t_dep
        
    def per_cell_growth_rate(self, s, t):
        
        """
        :param s: nutrient concentration
        :return: per cell growth rate
        """
        return self.t_dep(t) * (self.g_max * s) / (self.half_sat + s)

        
