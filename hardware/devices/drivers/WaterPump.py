from __future__ import annotations

import time
from enum import Enum

from hardware.devices.drivers.hw.i2c import PCA9685


class WaterPump(Enum):
    REACTOR0 = 6
    REACTOR1 = 7
    REACTOR2 = 11

    def __init__(self,
                 id: WaterPump,
                 lib):
        self.id = id
        self.lib = lib

    def set_speed(self, value: int):
        """

        :param value: speed value in percent
        """
        PCA9685.set_pwm(self.lib, self.value, (float(value) / 100) * 0xffff)

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
