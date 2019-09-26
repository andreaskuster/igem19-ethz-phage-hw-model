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
