#!/usr/bin/env python3
# encoding: utf-8
from __future__ import annotations

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

from hw.i2c.PCF8574 import PCF8574


class LED:

    _DEVICE_ID_MAP  = {
        0: 0,
        1: 1,
        2: 2
    }

    def __init__(self,
                 id: int,
                 i2c_lock: threading.Lock = None):
        self.id = id
        self.thread_safe = False if i2c_lock is None else True
        if self.thread_safe:
            self.lock = i2c_lock
            with self.lock:
                PCF8574.init()
        else:
            warnings.warn("Class functionality is not thread-safe.")
            PCF8574.init()

    def set_led(self):
        if self.thread_safe:
            with self.lock:
                return PCF8574.clear(self._DEVICE_ID_MAP[self.id])  # 'sinking configuration' clear is actually setting
        else:
            return PCF8574.clear(self._DEVICE_ID_MAP[self.id])

    def clear_led(self):
        if self.thread_safe:
            with self.lock:
                return PCF8574.set(self._DEVICE_ID_MAP[self.id])  # 'sinking configuration' set is actually clearing
        else:
            return PCF8574.set(self._DEVICE_ID_MAP[self.id])


if __name__ == "__main__":
    leds = [LED(0),
            LED(1),
            LED(2)]
    while True:
        print("Set all leds.")
        for led in leds:
            led.set_led()
        time.sleep(10)
        print("Reset all leds")
        for led in leds:
            led.clear_led()
        time.sleep(10)