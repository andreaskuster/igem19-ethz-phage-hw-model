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

import busio
from adafruit_bme280 import Adafruit_BME280_I2C as library
from board import SCL, SDA


class BME280:
    lib = library(busio.I2C(SCL, SDA))

    def __init__(self):
        pass

    @staticmethod
    def init():
        pass

    @staticmethod
    def get_temperature() -> float:
        """

        :return:
        """
        return BME280.lib.temperature

    @staticmethod
    def get_pressure() -> float:
        """

        :return:
        """
        return BME280.lib.pressure


if __name__ == "__main__":
    while True:
        print("Temperature: {} °C".format(BME280.get_temperature()))
        print("Pressure: {} hPa".format(BME280.get_pressure()))
        time.sleep(1.0)
