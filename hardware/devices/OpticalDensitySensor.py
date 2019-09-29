import threading
import time

import numpy as np
from pykalman import KalmanFilter
from sklearn.svm import SVR

from hardware.devices.drivers.LED import LED
from hardware.devices.drivers.LightSensor import LightSensor
from hardware.devices.drivers.PeristalticPump import PeristalticPump


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
        self.raw_log = list()
        self.od_log = list()
        self.svr: SVR = None
        self.calibrate()

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
        raw_value = light - dark
        if self.verbose:
            print("raw sensor value: {}".format(raw_value))

        # switch led off
        self.led.clear_led()

        # map raw value to actual od value
        od = self.svr.predict(raw_value.reshape(-1, 1))

        if self.verbose:
            print("od sensor value: {}".format(od))

        # append log
        if self.verbose:
            print("log data")
        self.raw_log(raw_value)
        self.od_log.append(od)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def finalize(self):
        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
        np.savetxt(fname="log/{}_od{}.csv".format(timestamp, self.id), delimiter=",", X=self.od_log)

    def calibrate(self, ):
        self.svr = SVR(gamma='scale', C=10000.0, epsilon=0.01)
        calibration_data_sensor = np.genfromtxt('calibration_sensor_data.csv', delimiter=',')  # od.csv
        calibration_data_od_device = np.genfromtxt('calibration_od_data.csv', delimiter=',')  # od_measurements.csv

        X = np.array([calibration_data_sensor[int(x) * 2] for x in calibration_data_od_device[0]])

        kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
        (mean, covariance) = kf.filter([x[1] for x in calibration_data_od_device])

        self.svr.fit(X.reshape(-1, 1), mean)


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
