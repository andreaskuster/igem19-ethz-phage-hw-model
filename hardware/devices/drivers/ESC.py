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

import os
import sys
import threading
import time
import warnings

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hw.i2c.ESC import ESC as ESC_HW


class ESC:

    _DEVICE_ID_MAP = {
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
                pass  # ESC_HW.init()
        else:
            warnings.warn("Class functionality is not thread-safe.")
            pass  # ESC_HW.init()

    def set_value(self,
                  value: int):
        """

        :param value: intensity from [-100, 100]
        :return:
        """
        if self.thread_safe:
            with self.lock:
                ESC_HW.set_value(self._DEVICE_ID_MAP[self.id], value)
        else:
            ESC_HW.set_value(self._DEVICE_ID_MAP[self.id], value)

    def max_heating(self):
        self.set_value(100)

    def max_cooling(self):
        self.set_value(-100)

    def stop(self):
        self.set_value(0)


if __name__ == "__main__":

    escs = [ESC(0),
            ESC(1),
            ESC(2)]

    _CASE = 1

    if _CASE == 1:
        while True:
            print("Max heating for 10 seconds.")
            for esc in escs:
                esc.max_heating()
            time.sleep(10.0)
            print("Wait for 20 seconds.")
            for esc in escs:
                esc.stop()
            time.sleep(20.0)
            print("Max cooling for 10 seconds.")
            for esc in escs:
                esc.max_cooling()
            time.sleep(10.0)
            print("Wait for 20 seconds.")
            for esc in escs:
                esc.stop()
            time.sleep(20.0)
    elif _CASE == 2:
        print("Stop all devices.")
        for esc in escs:
            esc.stop()