from __future__ import annotations

import threading
import time
import warnings
from enum import Enum

from drivers.hw.i2c import ESC as ESC_HW


class ESC:

    def __init__(self,
                 id: int,
                 i2c_lock: threading.Lock = None):
        self.id = id
        self.thread_safe = False if i2c_lock is None else True
        if self.thread_safe:
            self.lock = i2c_lock
            with self.lock:
                pass #ESC_HW.init()
        else:
            warnings.warn("Class functionality is not thread-safe.")
            pass  #ESC_HW.init()

    def set_value(self,
                  value: int):
        """

        :param value: intensity from [-100, 100]
        :return:
        """
        if self.thread_safe:
            with self.lock:
                ESC_HW.set_value(self.id, value)
        else:
            ESC_HW.set_value(self.id, value)

    def max_heating(self):
        self.set_value(100)

    def max_cooling(self):
        self.set_value(-100)

    def stop(self):
        self.set_value(0)


if __name__ == "__main__":

    escs = [ESC(0),
            ESC(1),
            ESC(2)]

    _CASE = 2

    while True:
        if _CASE == 1:
            print("Max heating for 10 seconds.")
            for esc in escs:
                esc.max_heating()
            time.sleep(10.0)
            print("Wait for 20 seconds.")
            for esc in escs:
                esc.stop()
            time.sleep(20.0)
            print("Max cooling for 10 seconds.")
            for esc in escs:
                esc.max_cooling()
            time.sleep(10.0)
            print("Wait for 20 seconds.")
            for esc in escs:
                esc.stop()
            time.sleep(20.0)
        elif _CASE == 2:
            print("Stop all devices.")
            for esc in escs:
                esc.stop()
