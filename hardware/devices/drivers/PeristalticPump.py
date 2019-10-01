from __future__ import annotations

import threading
import time
import warnings
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from hw.i2c.PCA9685 import PCA9685


class PeristalticPump:

    _DEVICE_ID_MAP = {
        0: 14,
        1: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 12,
        8: 13
    }

    def __init__(self,
                 id: int,
                 i2c_lock: threading.Lock = None):
        self.id = id
        self.thread_safe = False if i2c_lock is None else True
        if self.thread_safe:
            self.lock = i2c_lock
            with self.lock:
                PCA9685.init()
        else:
            warnings.warn("Class functionality is not thread-safe.")
            PCA9685.init()

    def set_speed(self, value: int):
        """

        :param value: speed value in percent
        """
        scaled_value = int((float(value) / 100.0) * 0xffff)
        if self.thread_safe:
            with self.lock:
                PCA9685.set_pwm(self._DEVICE_ID_MAP[self.id], scaled_value)
        else:
            PCA9685.set_pwm(self._DEVICE_ID_MAP[self.id], scaled_value)

    def start(self):
        self.set_speed(100)

    def stop(self):
        self.set_speed(0)


if __name__ == "__main__":
    pumps = [PeristalticPump(0),
             PeristalticPump(1),
             PeristalticPump(2),
             PeristalticPump(3),
             PeristalticPump(4),
             PeristalticPump(5),
             PeristalticPump(6),
             PeristalticPump(7),
             PeristalticPump(8)]
    print("Set speed of all pumps to 100%")
    for pump in pumps:
        pump.set_speed(100)
    time.sleep(1)
    print("Set speed of all pumps to 50%")
    for pump in pumps:
        pump.set_speed(50)
    time.sleep(1)
    print("Set speed of all pumps to 0%")
    for pump in pumps:
        pump.set_speed(0)
    time.sleep(1)