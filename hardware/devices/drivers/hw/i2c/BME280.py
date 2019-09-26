import time

import adafruit_bmp280
import board
import busio


def get_temperature(bus):
    """

    :param bus: busio instance
    :return: temperature in degree celcius
    """
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    return bmp280.temperature


def get_pressure(bus):
    """

    :param bus: busio instance
    :return: pressure in hPa
    """
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    return bmp280.pressure


if __name__ == "__main__":

    # Create library object using our Bus I2C port
    i2c = busio.I2C(board.SCL, board.SDA)
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)

    while True:
        print("\nTemperature: {} °C".format(bmp280.temperature))
        print("Pressure: {} hPa".format(bmp280.pressure))
        time.sleep(1.0)
