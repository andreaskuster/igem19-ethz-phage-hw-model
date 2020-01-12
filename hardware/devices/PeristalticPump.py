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
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "drivers"))


from drivers.PeristalticPump import PeristalticPump as Pump


class PeristalticPump:

    def __init__(self,
                 id: int,
                 i2c_lock: threading.Lock,
                 enabled: bool = False,
                 verbose: bool = True):
        self.id = id
        self.pump = Pump(id, i2c_lock)
        self.enabled = enabled
        self.verbose = verbose
        self.od_log = list()
        self.speed = 0

    def info(self):
        print("Peristaltic Pump {}: Speed: {}".format(self.id, self.speed))

    def enable(self):
        self.enabled = True
        self.speed = 100
        self.pump.start()

    def disable(self):
        self.enabled = False
        self.speed = 0
        self.pump.stop()

    def set_speed(self,
                  value: int):
        self.speed = value
        self.pump.set_speed(value)

    def start(self):
        self.pump.start()
        self.speed = 100

    def stop(self):
        self.pump.stop()
        self.speed = 0

    def set_volume(self,
                   value: int):
        raise NotImplementedError()  # TODO: calibrate water flow first

    def finalize(self):
        self.stop()


if __name__ == "__main__":

    pump = PeristalticPump(id=0,
                           i2c_lock=None,
                           enabled=False,
                           verbose=False)
    try:
        while True:
            print("Run pump 0 at full speed.")
            pump.start()
            time.sleep(4.0)
            print("Stop pump 0.")
            pump.stop()
            time.sleep(4.0)
            print("Run pump 0 at 50% speed.")
            pump.set_speed(50)
            time.sleep(4.0)
            print("Stop pump 0.")
            pump.stop()
            time.sleep(10.0)
    except KeyboardInterrupt:
        print("Exiting...but first put device into a safe state...")
    finally:
        pump.finalize()
        print("Goodbye.")