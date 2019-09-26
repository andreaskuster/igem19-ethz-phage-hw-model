from __future__ import annotations

import threading
import time
import warnings
from enum import Enum

from hw.i2c import PCA9685


class WaterPump(Enum):
    REACTOR0 = 6
    REACTOR1 = 7
    REACTOR2 = 11

    def __init__(self,
                 id: WaterPump,
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
    pumps = [WaterPump(WaterPump.REACTOR0),
             WaterPump(WaterPump.REACTOR1),
             WaterPump(WaterPump.REACTOR2)]
    print("Set speed of all pumps to 100%")
    for pump in pumps:
        pump.set_speed(100)
    time.sleep(10)
    print("Set speed of all pumps to 50%")
    for pump in pumps:
        pump.set_speed(50)
    time.sleep(10)
    print("Set speed of all pumps to 0%")
    for pump in pumps:
        pump.set_speed(0)
    time.sleep(10)
