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

from collections import deque

import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
from ddeint import ddeint
from pylab import array

from host import Host
from phage import Phage


class reaB():

    def __init__(self):
        # simulation time and resolution of samples
        self.dt = 0.1
        self.xs = np.linspace(0, 120, 120 / self.dt)
        self.fluxA = 0.0
        self.fluxB = 0.0

        self.new_host = Host(
            c0=10 ** 5,
            g_max=0.036,  # lit: 0.012
            yield_coeff=0.000000000001,
            half_sat=0.00000125,
            death_rate=0.001,
            t_dep=self.temperature_dependency_new_host,
        )
        self.original_phage = Phage(
            c0=10 ** 9,
            adsorption_rate=0.000000000001,
            burst_size=100,
            death_rate=0.00272,
        )
        self.new_phage = Phage(
            c0=10 ** 6,
            adsorption_rate=0.0000000001,
            burst_size=100,
            death_rate=0.00272,
        )

        self.s0 = 0.0000025  # stock concentration of nutrient (g/mL) #0.0000025
        self.R_pnn = 1 / 1000  # fraction of new phage in library

        self.myinterpolator = scipy.interpolate.interp1d(
            np.array([0 - 1, 0]),  # X
            np.array([0, 1]).T,  # Y
            kind="linear",
            bounds_error=False,
            fill_value=0
        )

        self.d = 13.3  # lysis time delay
        self.dd = 13
        # dt *=10
        self.q_h_inf_poo = deque([0])
        self.q_h_inf_pnn = deque([0])
        for i in range(100):
            self.q_h_inf_poo.append(0)
            self.q_h_inf_pnn.append(0)

        data = ddeint(self.model, self.initial_conditions, self.xs, fargs=(self.d,))

        plt.figure(figsize=(16, 16))

        plt.subplot(3, 3, 1)
        plt.plot(self.xs, [data[t][0] for t in range(len(self.xs))], label="reactor A")
        plt.xlabel('time [min]')
        plt.ylabel('concentration [#bacteria/mL]')
        plt.title('Host Concentration A over Time')
        plt.legend()

        plt.subplot(3, 3, 2)
        plt.plot(self.xs, [data[t][1] for t in range(len(self.xs))], label="reactor A")
        plt.xlabel('time [min]')
        plt.ylabel('concentration [g/mL]')
        plt.title('Nutrient A over Time')
        plt.legend()

        plt.subplot(3, 3, 3)
        plt.plot(self.xs, [data[t][2] for t in range(len(self.xs))])
        plt.xlabel('time [min]')
        plt.ylabel('concentration [#bacteria/mL]')
        plt.title('Host Concentration B over Time')

        plt.subplot(3, 3, 4)
        plt.plot(self.xs, [data[t][3] for t in range(len(self.xs))])
        plt.xlabel('time [min]')
        plt.ylabel('concentration [g/mL]')
        plt.title('Nutrient B over Time')

        plt.subplot(3, 3, 5)
        plt.plot(self.xs, [data[t][4] for t in range(len(self.xs))])
        plt.xlabel('time [min]')
        plt.ylabel('concentration [#bacteria/mL]')
        plt.title('Host infected OO over Time')

        plt.subplot(3, 3, 6)
        plt.plot(self.xs, [data[t][5] for t in range(len(self.xs))])
        plt.xlabel('time [min]')
        plt.ylabel('concentration [#bacteria/mL]')
        plt.title('Host infected NN over Time')

        plt.subplot(3, 3, 8)
        plt.plot(self.xs, [data[t][6] for t in range(len(self.xs))])
        plt.xlabel('time [min]')
        plt.ylabel('concentration [#phage/mL]')
        plt.title('Phage OO over Time')

        plt.subplot(3, 3, 9)
        plt.plot(self.xs, [data[t][7] for t in range(len(self.xs))])
        plt.xlabel('time [min]')
        plt.ylabel('concentration [#phage/mL]')
        plt.title('Phage NN over Time')

        plt.subplot(3, 3, 7)
        plt.plot(self.xs, [data[t][6] for t in range(len(self.xs))], label="original")
        plt.plot(self.xs, [data[t][7] for t in range(len(self.xs))], label="new")
        plt.xlabel('time [min]')
        plt.ylabel('concentration [#phage/mL]')
        plt.title('Phage over Time')
        plt.legend()

        plt.subplots_adjust(wspace=0.4, hspace=0.4)
        plt.show()

    # Reactor A
    # lb influx profile of reactor A
    def in_a_lb(self, t):
        """
        :param t: time t
        :return: lb influx to reactor a at time t
        """
        return self.fluxA

    # biomass outflux profile of reactor A
    def out_a(self, t):
        """
        :param t: time t
        :return: biomass outflux of reactor a at time t
        """
        return self.fluxA

    # temperature profile of reactor A
    def temperature_a(self, t):
        """
        :param t: time t
        :return: temperature at time t
        """
        return 39.7

    # Reactor B
    # lb influx profile of reactor B
    def in_b_lb(self, t):
        """
        :param t: time t
        :return: lb influx to reactor b at time t
        """
        return self.fluxB / 3

    # lb influx profile of reactor B
    def in_nh(self, t):
        """
        :param t: time t
        :return: new_host influx from reactor a to reactor b at time t
        """
        return self.fluxB / 3

    # phage library influx in reactor B
    def in_lib(self, t):
        """
        param t: time t
        :return: library influx in reator b at time t
        """
        return self.fluxB / 3

    # biomass outflux profile of reactor B
    def out_b(self, t):
        """
        :param t: time t
        :return: biomass outflux of reactor b at time t
        """
        return self.fluxB

    # temperature profile of reactor B
    def temperature_b(self, t):
        """
        :param t: time t
        :return: temperature at time t
        """
        return 39.7

    def temperature_dependency_new_host(self, x):
        """
        :param x: temperature
        :return: growth rate factor
        """
        mu = 39.7
        sigma_l = 120.0
        sigma_r = 10.0
        if x < mu:
            return np.exp(-0.5 * (np.square(x - mu) / sigma_l))  # gaussian l: ~(39.7, 120)
        else:
            return np.exp(-0.5 * (np.square(x - mu) / sigma_r))  # gaussian r: ~(39.7, 10)

    def update(self, myinterpolator, t, Y):
        """ Add one new (ti,yi) to the interpolator """
        Y2 = Y if (Y.size == 1) else np.array([Y]).T
        myinterpolator = scipy.interpolate.interp1d(
            np.hstack([myinterpolator.x, [t]]),  # X
            np.hstack([myinterpolator.y, Y2]),  # Y
            kind="linear",
            bounds_error=False,
            fill_value=Y
        )
        return myinterpolator

    # define system of differential equations
    def model(self, Y, t, d):
        c_host_a, c_nutr_a, c_host_b, c_nutr_b, c_inf_poo, c_inf_pnn, c_poo, c_pnn = Y(t)
        c_host_a_d, c_nutr_a_d, c_host_b_d, c_nutr_b_d, c_inf_poo_d, c_inf_pnn_d, c_poo_d, c_pnn_d = Y(t - d)
        y = self.myinterpolator(t)
        self.myinterpolator = self.update(self.myinterpolator, t,
                                          self.original_phage.infection_rate(c_host_b, c_poo) - y - self.out_b(
                                              t) * c_inf_poo)
        if y != 0:
            pass
            #print(y)

        return np.array([0 if c_host_a < 0 else self.new_host.per_cell_growth_rate(c_nutr_a, self.temperature_a(
            t)) * c_host_a - self.out_a(t) * c_host_a - self.new_host.death_rate * c_host_a,
                         self.s0 * self.in_a_lb(
                             t) if c_nutr_a < 0 else - self.new_host.yield_coeff * self.new_host.per_cell_growth_rate(
                             c_nutr_a, self.temperature_a(t)) * c_host_a
                                                     + self.s0 * self.in_a_lb(t) - c_nutr_a * self.out_a(t),
                         0 if c_host_b < 0 else self.new_host.per_cell_growth_rate(c_nutr_b, self.temperature_b(
                             t)) * c_host_b + self.in_nh(t) * c_host_a
                                                - self.new_phage.infection_rate(c_host_b,
                                                                                c_pnn) - self.original_phage.infection_rate(
                             c_host_b, c_poo)
                                                - self.new_host.death_rate * c_host_b - self.out_b(t) * c_host_b,
                         self.s0 * self.in_b_lb(t) + c_nutr_a * self.in_nh(
                             t) if c_nutr_b < 0 else - self.new_host.yield_coeff * self.new_host.per_cell_growth_rate(
                             c_nutr_b, self.temperature_b(t)) * (c_host_b + c_inf_poo + c_inf_pnn)
                                                     + self.s0 * self.in_b_lb(t) + c_nutr_a * self.in_nh(
                             t) - c_nutr_b * self.out_b(t),
                         self.original_phage.infection_rate(c_host_b,
                                                            c_poo) if c_inf_poo < 0 else self.original_phage.infection_rate(
                             c_host_b, c_poo) - y - self.out_b(t) * c_inf_poo,
                         self.new_phage.infection_rate(c_host_b,
                                                       c_pnn) if c_inf_pnn < 0 else self.new_phage.infection_rate(
                             c_host_b, c_pnn) - y - self.out_b(t) * c_inf_pnn,
                         0 if c_poo < 0 else self.original_phage.burst_size * y - self.original_phage.infection_rate(
                             c_host_b, c_poo)
                                             - self.out_b(
                             t) * c_poo - self.original_phage.death_rate * c_poo + self.in_lib(t) * (1 - self.R_pnn),
                         0 if c_pnn < 0 else self.new_phage.burst_size * y - self.new_phage.infection_rate(c_host_b,
                                                                                                           c_pnn)
                                             - self.out_b(t) * c_pnn - self.new_phage.death_rate * c_pnn + self.in_lib(
                             t) * self.R_pnn])

    def initial_conditions(self, t):
        return array([self.new_host.c0, self.s0, 10 ** 9, self.s0 * 5 * 10 ** 3, 0.0, 0.0, self.original_phage.c0,
                      self.new_phage.c0])
    # for elem in q_h_inf_poo:
    #    print(elem)


if __name__ == "__main__":
    reaB()
