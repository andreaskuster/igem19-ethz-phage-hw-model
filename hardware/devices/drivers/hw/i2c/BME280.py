import time

import adafruit_bme280
import board
import busio


def get_temperature(bus):
    """

    :param bus: busio instance
    :return: temperature in degree celcius
    """
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
    return bmp280.temperature


def get_pressure(bus):
    """

    :param bus: busio instance
    :return: pressure in hPa
    """
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
    return bme280.pressure


if __name__ == "__main__":

    # Create library object using our Bus I2C port
    i2c = busio.I2C(board.SCL, board.SDA)

    adafruit_bme280._BME280_ADDRESS = 0x76
    bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
    bme280._BME280_ADDRESS = 0x76

    while True:
        print("\nTemperature: {} °C".format(bme280.temperature))
        print("Pressure: {} hPa".format(bme280.pressure))
        time.sleep(1.0)
