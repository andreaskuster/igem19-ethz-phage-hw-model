import threading

from hardware.devices.drivers.PeristalticPump import PeristalticPump
from hardware.devices.drivers.LED import LED
from hardware.devices.drivers.LightSensor import LightSensor


class OpticalDensitySensor:

    def __init__(self,
                 id: int,
                 i2c_lock: threading.Lock,
                 enabled: bool = False,
                 verbose: bool = True):

        self.id = id
        self.pump = PeristalticPump(id, i2c_lock)
        self.led = LED(id, i2c_lock)
        self.sensor = LightSensor(id, i2c_lock)
        self.enabled = enabled
        self.verbose = verbose


    def event_loop(self):
        pass

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False