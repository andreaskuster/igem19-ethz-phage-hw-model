from __future__ import annotations

import threading
import time
import warnings
from enum import Enum

from hw.i2c import TSL2591


class LightSensor(Enum):
    REACTOR0 = 4
    REACTOR1 = 3
    REACTOR2 = 2

    def __init__(self,
                 id: TSL2591,
                 i2c_lock: threading.Lock):
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
                TSL2591.init()
        else:
            warnings.warn("Class functionality is not thread-safe.")
            TSL2591.init()

    def get_light_intensity(self):
        if self.thread_safe:
            with self.lock:
                return TSL2591.read_light_intensity(self.id)
        else:
            return TSL2591.read_light_intensity(self.id)


if __name__ == "__main__":
    sensors = [LightSensor(LightSensor.REACTOR0),
               LightSensor(LightSensor.REACTOR1),
               LightSensor(LightSensor.REACTOR2)]
    while True:
        for sensor in sensors:
            print("Light intensity of {}: {} units.".format(sensor.name, sensor.get_light_intensity()))
        time.sleep(10.0)
