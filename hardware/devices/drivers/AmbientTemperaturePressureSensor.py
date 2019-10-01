from __future__ import annotations

import threading
import time
import warnings
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hw.i2c.BME280 import BME280


class AmbientTemperaturePressureSensor():

    def __init__(self,
                 i2c_lock: threading.Lock = None):
        """
        :param i2c_lock:
        """
        self.thread_safe = False if i2c_lock is None else True
        if self.thread_safe:
            self.lock = i2c_lock
            with self.lock:
                BME280.init()
        else:
            warnings.warn("Class functionality is not thread-safe.")
            BME280.init()

    def get_temperature(self):
        if self.thread_safe:
            with self.lock:
                return BME280.get_temperature()
        else:
            return BME280.get_temperature()

    def get_pressure(self):
        if self.thread_safe:
            with self.lock:
                return BME280.get_pressure()
        else:
            return BME280.get_pressure()


if __name__ == "__main__":
    sensor = AmbientTemperaturePressureSensor()

    while True:
        print("Ambient temperature: {}°C".format(sensor.get_temperature()))
        print("Ambient pressure: {}hPa".format(sensor.get_pressure()))
        time.sleep(10.0)