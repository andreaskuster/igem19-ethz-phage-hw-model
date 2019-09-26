from __future__ import annotations
import threading
import time
from enum import Enum

from hardware.hw.one_wire import DS18B20


class WaterTemperatureSensor(Enum):
    REACTOR0 = "28-0114536b03aa"
    REACTOR1 = "28-80000026f3d8"
    REACTOR2 = "28-0114534081aa"

    def __init__(self,
                 id: WaterTemperatureSensor,
                 lock: threading.Lock):
        """

        :param id: id of the water temperature sensor
        :param lock: lock for the one wire bus access
        """
        self.id = id  # sets name from {REACTOR0, REACTOR1, REACTOR2} and value from {28-xxxxxxxxxxxx, ..}
        self.thread_safe = False if lock is None else True
        if self.thread_safe:
            self._lock = lock
            with self._lock:
                DS18B20.init()
        else:
            raise RuntimeWarning("Class functionality is not thread-safe.")

    def get_temperature(self):
        with self._lock:
            return DS18B20.get_temperature(self.value)


if __name__ == "__main__":
    reactors = [WaterTemperatureSensor(WaterTemperatureSensor.REACTOR0),
                WaterTemperatureSensor(WaterTemperatureSensor.REACTOR1),
                WaterTemperatureSensor(WaterTemperatureSensor.REACTOR2)]
    for reactor in reactors:
        print("Water temperature of {}: {}°C".format(reactor.name, reactor.get_temperature()))
    time.sleep(10)
