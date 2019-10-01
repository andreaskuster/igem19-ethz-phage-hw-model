from __future__ import annotations

import threading
import time
import warnings
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from hw.i2c.TSL2591 import TSL2591
from hw.i2c.TCA9548A import TCA9548A

class LightSensor:

    _DEVICE_ID_MAP = {
        0: 4,
        1: 3,
        2: 2
    }

    def __init__(self,
                 id: int,
                 i2c_lock: threading.Lock = None):
        """
        Initialize the class structure.
        :param id:
        :param i2c_lock:
        """
        self.id = id
        self.thread_safe = False if i2c_lock is None else True
        if self.thread_safe:
            self.lock = i2c_lock
            with self.lock:
                TCA9548A.init()
                TSL2591.init()
        else:
            warnings.warn("Class functionality is not thread-safe.")
            TCA9548A.init()
            TSL2591.init()

    def get_light_intensity(self):
        if self.thread_safe:
            with self.lock:
                TCA9548A.switch(self._DEVICE_ID_MAP[self.id])  # set i2c multiplexer to correct sensor
                time.sleep(0.1)
                return TSL2591.read_light_intensity()
        else:
            TCA9548A.switch(self._DEVICE_ID_MAP[self.id])
            time.sleep(0.1)
            return TSL2591.read_light_intensity()


if __name__ == "__main__":
    sensors = [LightSensor(0),
               LightSensor(1),
               LightSensor(2)]
    while True:
        for sensor in sensors:
            print("Light intensity of sensor {}: {} units.".format(sensor.id, sensor.get_light_intensity()))
        time.sleep(10.0)