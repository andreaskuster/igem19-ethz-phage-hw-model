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

sys.path.append(os.path.join(os.path.dirname(__file__), "hardware"))
sys.path.append(os.path.join(os.path.dirname(__file__), "hardware/devices"))
sys.path.append(os.path.join(os.path.dirname(__file__), "hardware/devices/drivers/hw/i2c"))

from devices.OpticalDensitySensor import OpticalDensitySensor
from devices.PeristalticPump import PeristalticPump
from devices.ReactorTemperatureControl import ReactorTemperatureControl


class AdvancedNaiveConstantConcentration:

    def __init__(self,
                 enabled: bool,
                 target_od: float,
                 continuous_pump_time: float,
                 reactors: List[ReactorTemperatureControl],
                 sensors: List[OpticalDensitySensor],
                 pumps: List[PeristalticPump]):
        """
        :param enabled: enable / disable control loop
        :param reactors: reactor[0] = bacteria only (control constant growth rate), reactor[2] = bacteria & phages
        :param sensors: sensor[0] = sensor for reactor[0], sensor[1]  = sensor for reactor[2]
        :param pumps: pump[0] = lb influx to reactor[0], pump[1] = pump from reactor[0] to reactor[1], pump[3] = from reactor[1] to the waste
        :param interval: control loop interval
        """
        self.enabled = enabled
        self.target_od = target_od
        self.reactors = reactors
        self.sensors = sensors
        self.pumps = pumps
        self.tol = 0.05
        self.continuous_pump_time = continuous_pump_time

    def control_loop(self):
        if self.enabled:
            diff = self.sensors[0].last_od - self.target_od
            if diff > self.tol:
                self.pumps[1].enable()
                self.pumps[3].enable()
                time.sleep(diff * 10 if diff * 10 < 5.0 else 5.0)
                self.pumps[1].disable()
                self.pumps[3].disable()
            elif diff < -self.tol:
                self.pumps[0].enable()
                self.pumps[2].enable()
                self.pumps[3].enable()
                time.sleep(abs(diff * 10) if abs(diff * 10) < 5.0 else 5.0)
                self.pumps[0].disable()
                self.pumps[2].disable()
                self.pumps[3].disable()
            self.pumps[0].enable()
            self.pumps[2].enable()
            self.pumps[3].enable()
            time.sleep(self.continuous_pump_time)
            self.pumps[0].disable()
            self.pumps[2].disable()
            self.pumps[3].disable()

    def finalize(self):
        for pump in self.pumps:
            pump.disable()
        for sensor in self.sensors:
            sensor.disable()
        for reactor in self.reactors:
            reactor.disable()