import threading
import time
import numpy as np

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
        self.od_log = list()

    def event_loop(self):
        # run peristaltic pump for 10s
        if self.verbose:
            print("run peristaltic pump")
        self.pump.start()
        time.sleep(10)

        # let the biomass settle down for 3s
        if self.verbose:
            print("stop peristaltic pump")
        self.pump.stop()
        time.sleep(3)

        # start measuring
        if self.verbose:
            print("measure")

        # measure dark value
        self.led.set_led()
        time.sleep(1.0)
        dark = self.sensor.get_light_intensity()
        # measure light value
        self.led.clear_led()
        time.sleep(1.0)
        light = self.sensor.get_light_intensity()
        od = light - dark
        if self.verbose:
            print("od value: {}".format(od))

        # switch led off
        self.led.clear_led()

        # append log
        if self.verbose:
            print("log data")
        self.od_log.append(od)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def finalize(self):
        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
        np.savetxt(fname="log/{}_od{}.csv".format(timestamp, self.id), delimiter=",", X=self.od_log)


if __name__ == "__main__":

    interval = 30.0
    sensor = OpticalDensitySensor(id=0,
                                  i2c_lock=None,
                                  enabled=False,
                                  verbose=False)
    sensor.enable()

    try:
        # run control loop till keyboard interrupt (Ctrl + C)
        starttime = time.time()

        while True:

            sensor.event_loop()

            # wait for the next measurement cycle
            print("sleep till next cycle")
            time.sleep(interval - ((time.time() - starttime) % interval))

    except KeyboardInterrupt:
        print("Exiting...but first put device into a safe state...")
    finally:
        sensor.finalize()
        print("Goodbye.")