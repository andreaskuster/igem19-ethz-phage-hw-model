from __future__ import annotations

import threading
import time
import warnings
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from hw.i2c import PCA9685


class PCFan:

    _DEVICE_ID_MAP = {
        0: 8,
        1: 9,
        2: 10
    }

    def __init__(self,
                 id: PCFan,
                 i2c_lock: threading.Lock):
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
        scaled_value = (float(value) / 100.0) * 0xffff
        if self.thread_safe:
            with self.lock:
                PCA9685.set_pwm(self.lib, self.value, scaled_value)
        else:
            PCA9685.set_pwm(self.lib, self.value, scaled_value)

    def start(self):
        self.set_speed(100)

    def stop(self):
        self.set_speed(0)


if __name__ == "__main__":

    fans = [PCFan(PCFan._DEVICE_ID_MAP[0]),
            PCFan(PCFan._DEVICE_ID_MAP[1]),
            PCFan(PCFan._DEVICE_ID_MAP[2])]

    print("Set speed of all pc fans to 100%")
    for fan in fans:
        fan.set_speed(100)
    time.sleep(10)
    print("Set speed of all pc fans to 50%")
    for fan in fans:
        fan.set_speed(50)
    time.sleep(10)
    print("Set speed of all pc fans to 0%")
    for fan in fans:
        fan.set_speed(0)
    time.sleep(10)
