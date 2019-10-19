import threading
import time

import numpy as np
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "drivers"))

from pykalman import KalmanFilter
from sklearn.svm import SVR

from drivers.LED import LED
from drivers.LightSensor import LightSensor
from drivers.PeristalticPump import PeristalticPump


class OpticalDensitySensor:
    _DEVICE_ID_MAP = {
        0: 7,
        1: 4,
        2: 1
    }

    def __init__(self,
                 id: int,
                 i2c_lock: threading.Lock,
                 enabled: bool = False,
                 verbose: bool = True):

        self.id = id
        self.pump = PeristalticPump(self._DEVICE_ID_MAP[id], i2c_lock)
        self.led = LED(id, i2c_lock)
        self.sensor = LightSensor(id, i2c_lock)
        self.enabled = enabled
        self.verbose = verbose
        self.raw_log = list()
        self.od_log = list()
        self.svr: SVR = None
        self.calibrate()
        self.last_od = -1
        self.last_raw = -1
        data = np.genfromtxt(os.path.join(os.path.dirname(__file__), 'calibration_sensor_data.csv'), delimiter=',')
        self.max_od_raw_val = max(data)

    def info(self):
        print("OD Sensor {}: OD: {}, Raw Value: {}".format(self.id, self.last_od, self.last_raw))

    def event_loop(self):

        if self.enabled:
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
            self.led.clear_led()
            time.sleep(1.0)
            # print("led off")
            dark = self.sensor.get_light_intensity()
            # print("dark value: {}".format(dark))
            # measure light value
            self.led.set_led()
            time.sleep(1.0)
            # print("led on")
            light = self.sensor.get_light_intensity()
            # print("light value: {}".format(light))
            raw_value = light - dark
            self.last_raw = raw_value
            if self.verbose:
                print("raw sensor value: {}".format(raw_value))

            # switch led off
            self.led.clear_led()
            # print("led off")
            # map raw value to actual od value
            if raw_value > self.max_od_raw_val:  # overshoot, od zero is minimum
                od = 0.0
            else:
                od = self.svr.predict(np.array(raw_value).reshape(1, -1))
            self.last_od = od
            if self.verbose:
                print("od sensor value: {}".format(od))

            # append log
            if self.verbose:
                print("log data")
            self.raw_log.append((time.strftime("%Y-%m-%d_%H:%M:%S"), raw_value))
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
        calibration_data_sensor = np.genfromtxt(os.path.join(os.path.dirname(__file__), 'calibration_sensor_data.csv'),
                                                delimiter=',')  # od.csv
        calibration_data_od_device = np.genfromtxt(os.path.join(os.path.dirname(__file__), 'calibration_od_data.csv'),
                                                   delimiter=',')  # od_measurements.csv

        X = np.array([calibration_data_sensor[int(x) * 2] for x in [x[0] for x in calibration_data_od_device]])

        kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)
        (mean, covariance) = kf.filter([x[1] for x in calibration_data_od_device])

        self.svr.fit(X.reshape(-1, 1), mean.ravel())


if __name__ == "__main__":

    interval = 30.0
    sensor = OpticalDensitySensor(id=0,
                                  i2c_lock=None,
                                  enabled=False,
                                  verbose=True)
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