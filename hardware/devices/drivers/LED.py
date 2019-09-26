from __future__ import annotations

import threading
import time
import warnings
from enum import Enum

from hw.i2c import PCF8574


class LED(Enum):
    REACTOR0 = 0  # TODO: check if the values are correct
    REACTOR1 = 1
    REACTOR2 = 2

    def __init__(self,
                 id: LED,
                 i2c_lock: threading.Lock):
        self.id = id
        self.thread_safe = False if i2c_lock is None else True
        if self.thread_safe:
            self.lock = i2c_lock
            with self.lock:
                PCF8574.init()
        else:
            warnings.warn("Class functionality is not thread-safe.")
            PCF8574.init()

    def set_led(self):
        if self.thread_safe:
            with self.lock:
                return PCF8574.clear(self.id)  # 'sinking configuration' clear is actually setting
        else:
            return PCF8574.clear(self.id)

    def clear_led(self):
        if self.thread_safe:
            with self.lock:
                return PCF8574.set(self.id)  # 'sinking configuration' set is actually clearing
        else:
            return PCF8574.set(self.id)


if __name__ == "__main__":
    leds = [LED(LED.REACTOR0),
            LED(LED.REACTOR1),
            LED(LED.REACTOR2)]
    while True:
        print("Set all leds.")
        for led in leds:
            led.set_led()
        time.sleep(10)
        print("Reset all leds")
        for led in leds:
            led.set_speed(50)
        time.sleep(10)
