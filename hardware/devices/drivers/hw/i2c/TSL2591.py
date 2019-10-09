import time

import busio
from adafruit_tsl2591 import GAIN_HIGH, INTEGRATIONTIME_200MS, TSL2591 as library
from board import SCL, SDA
from TCA9548A import TCA9548A


class TSL2591:
    _OVERSAMPLING = 8

    lib = library(busio.I2C(SCL, SDA))

    def __init__(self):
        TCA9548A.switch(2) # initialize i2c mux to have at valid sensor

    @staticmethod
    def init():
        for dev in [2, 3, 4]:
            TCA9548A.switch(dev)
            time.sleep(0.1)
            TSL2591.lib.gain = GAIN_HIGH
            TSL2591.lib.integration_time = INTEGRATIONTIME_200MS
            # do a few test runs
            for i in range(5):
                TSL2591.read_light_intensity()
                time.sleep(0.1)

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

    TSL2591.init()


    _CASE = 2

    if _CASE == 1:
        while True:
            TCA9548A.switch(3)
            print('Light intensity: {}'.format(TSL2591.read_light_intensity()))
            time.sleep(1.0)
    elif _CASE == 2:
        for i in range(4):
            TCA9548A.switch(2)
            time.sleep(0.1)
            print('Light intensity: {}'.format(TSL2591.read_light_intensity()))
            TCA9548A.switch(3)
            time.sleep(0.1)
            print('Light intensity: {}'.format(TSL2591.read_light_intensity()))
            TCA9548A.switch(4)
            time.sleep(0.1)
            print('Light intensity: {}'.format(TSL2591.read_light_intensity()))
            time.sleep(1.0)
