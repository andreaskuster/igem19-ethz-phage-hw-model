import time
from enum import Enum

import busio
from adafruit_tsl2591 import TSL2591 as library
from board import SCL, SDA


class TSL2591(Enum):
    _OVERSAMPLING = 8

    lib = library(busio.I2C(SCL, SDA))

    @staticmethod
    def init():
        TSL2591.lib.GAIN_HIGH
        TSL2591.lib.INTEGRATIONTIME_200MS

    @staticmethod
    def read_light_intensity():
        """
        Read full spectrum light intensity value.
        :return: raw light intensity value (0..2.4e9)
        """
        sum = 0.0
        for i in range(TSL2591._OVERSAMPLING):
            sum += TSL2591.lib.full_spectrum
        return sum / TSL2591._OVERSAMPLING


if __name__ == "__main__":
    while True:
        print('Full spectrum light intensity: {}'.format(TSL2591.lib.full_spectrum))
        time.sleep(1.0)
