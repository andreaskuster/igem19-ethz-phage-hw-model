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

import time

import smbus


class PCF8574:
    _BUS_NO = 1
    _DEVICE_ADDRESS = 0x38

    bus = smbus.SMBus(_BUS_NO)

    def __init__(self):
        pass

    @staticmethod
    def init():
        """
        Initialize board.
        """
        pass

    @staticmethod
    def clear_all():
        """
        Resets all eight I/Os to zero.
        """
        PCF8574.bus.write_byte(PCF8574._DEVICE_ADDRESS, 0x00)

    @staticmethod
    def set_all():
        """
        Sets all eight I/Os to one.
        """
        PCF8574.bus.write_byte(PCF8574._DEVICE_ADDRESS, 0xff)

    @staticmethod
    def set(port: int):
        """
        Sets an individual I/O to one.
        :param port: I/O port (0,..,7)
        """
        # read register
        state = PCF8574.bus.read_byte(PCF8574._DEVICE_ADDRESS)
        # set port
        PCF8574.bus.write_byte(PCF8574._DEVICE_ADDRESS, state | (0x1 << port))

    @staticmethod
    def clear(port: int):
        """
        Clears an individual I/O to zero.
        :param port: I/O port (0,..,7)
        """
        # read register
        state = PCF8574.bus.read_byte(PCF8574._DEVICE_ADDRESS)
        # clear port
        PCF8574.bus.write_byte(PCF8574._DEVICE_ADDRESS, state & (0xff ^ (0x1 << port)))

    @staticmethod
    def toggle(port: int):
        """
        Toggles an individual I/O port.
        :param port: I/O port (0,..,7)
        """
        # read register
        state = PCF8574.bus.read_byte(PCF8574._DEVICE_ADDRESS)
        # clear port
        PCF8574.bus.write_byte(PCF8574._DEVICE_ADDRESS, state ^ (0x1 << port))


if __name__ == "__main__":

    _CASE = 1

    if _CASE == 1:
        # run all on / all off interval
        while True:
            print("set all outputs")
            PCF8574.set_all()
            time.sleep(10)
            print("reset all outputs")
            PCF8574.clear_all()
            time.sleep(10)
    elif _CASE == 2:
        PCF8574.clear_all()

# note: PCF8574 uses 'sinking': 0 -> on, 1 -> off