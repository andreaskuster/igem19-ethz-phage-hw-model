import time

import busio
from adafruit_bme280 import Adafruit_BME280_I2C
from board import SCL, SDA


class BME280:
    lib = Adafruit_BME280_I2C(busio.I2C(SCL, SDA))

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
        print("\nTemperature: {} °C".format(BME280.get_temperature()))
        print("Pressure: {} hPa".format(BME280.get_pressure()))
        time.sleep(1.0)
