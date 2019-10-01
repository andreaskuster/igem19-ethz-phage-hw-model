import threading
import time
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "drivers"))


from drivers.PeristalticPump import PeristalticPump as Pump


class PeristalticPump:

    def __init__(self,
                 id: int,
                 i2c_lock: threading.Lock,
                 enabled: bool = False,
                 verbose: bool = True):
        self.id = id
        self.pump = Pump(id, i2c_lock)
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

    def finalize(self):
        self.stop()


if __name__ == "__main__":

    pump = PeristalticPump(id=0,
                           i2c_lock=None,
                           enabled=False,
                           verbose=False)
    try:
        while True:
            print("Run pump 0 at full speed.")
            pump.start()
            time.sleep(4.0)
            print("Stop pump 0.")
            pump.stop()
            time.sleep(4.0)
            print("Run pump 0 at 50% speed.")
            pump.set_speed(50)
            time.sleep(4.0)
            print("Stop pump 0.")
            pump.stop()
            time.sleep(10.0)
    except KeyboardInterrupt:
        print("Exiting...but first put device into a safe state...")
    finally:
        pump.finalize()
        print("Goodbye.")