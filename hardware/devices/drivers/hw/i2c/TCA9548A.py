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

import smbus


class TCA9548A:
    _BUS_NO = 1
    _DEVICE_ADDRESS = 0x70

    bus = smbus.SMBus(_BUS_NO)

    def __init__(self):
        pass

    @staticmethod
    def init():
        pass

    @staticmethod
    def switch(port: int):
        """
        Sets an individual I/O to one.
        :param port: I2C channel (0,..,7)
        """
        # set port
        TCA9548A.bus.write_byte(TCA9548A._DEVICE_ADDRESS, 0x1 << port)


if __name__ == "__main__":
    _CHANNEL = 2  # od light sensor @reactor 2
    TCA9548A.init()
    TCA9548A.switch(_CHANNEL)