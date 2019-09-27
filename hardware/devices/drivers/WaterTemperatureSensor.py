from __future__ import annotations
import threading
import time
import warnings
from enum import Enum

from hw.one_wire import DS18B20


class WaterTemperatureSensor(Enum):

    _DEVICE_ID_MAP = {
        "REACTOR0": "28-0114536b03aa",
        "REACTOR1": "28-80000026f3d8",
        "REACTOR2": "28-0114534081aa"
    }

    def __init__(self,
                 id: WaterTemperatureSensor,
                 one_wire_lock: threading.Lock = None):
        """

        :param id: id of the water temperature sensor
        :param one_wire_lock: lock for the one wire bus access
        """
        self.id = id  # sets name from {REACTOR0, REACTOR1, REACTOR2} and value from {28-xxxxxxxxxxxx, ..}
        self.thread_safe = False if one_wire_lock is None else True
        if self.thread_safe:
            self.lock = one_wire_lock
            with self.lock:
                DS18B20.init()
        else:
            warnings.warn("Class functionality is not thread-safe.")
            DS18B20.init()

    def get_temperature(self):
        if self.thread_safe:
            with self.lock:
                return DS18B20.get_temperature(self.value)
        else:
            return DS18B20.get_temperature(self.value)


if __name__ == "__main__":
    reactors = [WaterTemperatureSensor(WaterTemperatureSensor.REACTOR0),
                WaterTemperatureSensor(WaterTemperatureSensor.REACTOR1),
                WaterTemperatureSensor(WaterTemperatureSensor.REACTOR2)]
    while True:
        for reactor in reactors:
            print("Water temperature of {}: {}°C".format(reactor.name, reactor.get_temperature()))
        time.sleep(10.0)
