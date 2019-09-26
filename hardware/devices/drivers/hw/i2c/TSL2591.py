# Simple demo of the TSL2591 sensor.  Will print the detected light value
# every second.
import time

import board
import busio

import adafruit_tsl2591

from enum import Enum


class I2cChannel(Enum):
    REACTOR0 = 4
    REACTOR1 = 3
    REACTOR2 = 2


def read_light_intensity(bus,
                         id):
    """

    :param bus: busio instance
    :param id: od sensor id (0,1,2)
    :return: raw light intensity value
    """

    # TODO: set channel (TCA9548A) first

    _OVERSAMPLING = 4
    sensor = adafruit_tsl2591.TSL2591(bus)
    sensor.gain = adafruit_tsl2591.GAIN_HIGH
    sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS

    sum = 0.0
    for i in range(_OVERSAMPLING):
        sum += sensor.full_spectrum

    return sum/_OVERSAMPLING


if __name__ == "__main__":

    # Initialize the I2C bus.
    i2c = busio.I2C(board.SCL, board.SDA)

    # Initialize the sensor.
    sensor = adafruit_tsl2591.TSL2591(i2c)

    # You can optionally change the gain and integration time:
    #sensor.gain = adafruit_tsl2591.GAIN_LOW # (1x gain)
    #sensor.gain = adafruit_tsl2591.GAIN_MED # (25x gain, the default)
    sensor.gain = adafruit_tsl2591.GAIN_HIGH # (428x gain)
    #sensor.gain = adafruit_tsl2591.GAIN_MAX (9876x gain)
    sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS # (100ms, default)
    #sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_200MS #(200ms)
    #sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_300MS (300ms)
    #sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_400MS (400ms)
    #sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_500MS (500ms)
    #sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_600MS (600ms)

    # Read the total lux, IR, and visible light levels and print it every second.
    while True:
        # Read and calculate the light level in lux.
        #lux = sensor.lux
        #print('Total light: {0}lux'.format(lux))
        # You can also read the raw infrared and visible light levels.
        # These are unsigned, the higher the number the more light of that type.
        # There are no units like lux.
        # Infrared levels range from 0-65535 (16-bit)
        #infrared = sensor.infrared
        #print('Infrared light: {0}'.format(infrared))
        # Visible-only levels range from 0-2147483647 (32-bit)
        #visible = sensor.visible
        #print('Visible light: {0}'.format(visible))
        # Full spectrum (visible + IR) also range from 0-2147483647 (32-bit)
        full_spectrum = sensor.full_spectrum
        print('Full spectrum (IR + visible) light: {}'.format(full_spectrum))
        time.sleep(1.0)