#!/usr/bin/env python3
# encoding: utf-8
from __future__ import annotations

"""
    Copyright (C) 2019-2020 Andreas Kuster

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
import sys
import threading
import time
import warnings

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from drivers.hw.one_wire.DS18B20 import DS18B20


class WaterTemperatureSensor:
    _DEVICE_ID_MAP = {
        2: "28-0114536b03aa",
        1: "28-80000026f3d8",
        0: "28-0114534081aa"
    }

    def __init__(self,
                 id: int,
                 one_wire_lock: threading.Lock = None):
        """

        :param id: id of the water temperature sensor
        :param one_wire_lock: lock for the one wire bus access
        """
        self.id = id  # sets name from {REACTOR0, REACTOR1, REACTOR2} and value from {28-xxxxxxxxxxxx, ..}
        self.thread_safe = False if one_wire_lock is None else True
        if self.thread_safe:
            self.lock = one_wire_lock
            with self.lock:
                DS18B20.init()
        else:
            warnings.warn("Class functionality is not thread-safe.")
            DS18B20.init()

    def get_temperature(self):
        if self.thread_safe:
            with self.lock:
                return DS18B20.get_temperature(self._DEVICE_ID_MAP[self.id])
        else:
            return DS18B20.get_temperature(self._DEVICE_ID_MAP[self.id])


if __name__ == "__main__":

    reactors = [WaterTemperatureSensor(0),
                WaterTemperatureSensor(1),
                WaterTemperatureSensor(2)]
    while True:
        for reactor in reactors:
            print("Water temperature of recator {}: {}°C".format(reactor.id, reactor.get_temperature()))
        time.sleep(10.0)