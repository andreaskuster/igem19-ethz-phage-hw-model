import threading
import time

from hardware.devices.drivers.PeristalticPump import PeristalticPump


class PeristalticPump:

    def __init__(self,
                 id: int,
                 i2c_lock: threading.Lock,
                 enabled: bool = False,
                 verbose: bool = True):
        self.id = id
        self.pump = PeristalticPump(id, i2c_lock)
        self.enabled = enabled
        self.verbose = verbose
        self.od_log = list()

    def enable(self):
        self.enabled = True
        self.pump.start()

    def disable(self):
        self.enabled = False
        self.pump.stop()

    def set_speed(self,
                  value: int):
        self.pump.set_speed(value)

    def start(self):
        self.pump.start()

    def stop(self):
        self.pump.stop()

    def set_volume(self,
                   value: int):
        raise NotImplementedError()  # TODO: calibrate water flow first


if __name__ == "__main__":

    pump = PeristalticPump(id=0,
                           i2c_lock=None,
                           enabled=False,
                           verbose=False)

    while True:
        pump.start()
        time.sleep(4.0)
        pump.stop()
        time.sleep(4.0)
        pump.set_speed(50)
        time.sleep(4.0)
        pump.stop()
        time.sleep(10.0)
