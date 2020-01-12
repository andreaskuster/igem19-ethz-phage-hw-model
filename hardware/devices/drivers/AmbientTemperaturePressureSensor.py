from __future__ import annotations

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

import threading
import time
import warnings
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hw.i2c.BME280 import BME280


class AmbientTemperaturePressureSensor():

    def __init__(self,
                 i2c_lock: threading.Lock = None):
        """
        :param i2c_lock:
        """
        self.thread_safe = False if i2c_lock is None else True
        if self.thread_safe:
            self.lock = i2c_lock
            with self.lock:
                BME280.init()
        else:
            warnings.warn("Class functionality is not thread-safe.")
            BME280.init()

    def get_temperature(self):
        if self.thread_safe:
            with self.lock:
                return BME280.get_temperature()
        else:
            return BME280.get_temperature()

    def get_pressure(self):
        if self.thread_safe:
            with self.lock:
                return BME280.get_pressure()
        else:
            return BME280.get_pressure()


if __name__ == "__main__":
    sensor = AmbientTemperaturePressureSensor()

    while True:
        print("Ambient temperature: {}°C".format(sensor.get_temperature()))
        print("Ambient pressure: {}hPa".format(sensor.get_pressure()))
        time.sleep(10.0)