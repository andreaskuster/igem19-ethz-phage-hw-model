from __future__ import annotations

import threading
import time
import warnings

import numpy as np
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "drivers"))


from drivers.ESC import ESC
from drivers.WaterPump import WaterPump
from drivers.PCFan import PCFan
from drivers.WaterTemperatureSensor import WaterTemperatureSensor
from simple_pid import PID


class ReactorTemperatureControl:

    _DEVICE_ID_MAP = {
            0: 2,
            1: 1,
            2: 0
            }

    def __init__(self,
                 id: int,
                 i2c_lock: threading.Lock = None,
                 one_wire_lock: threading.Lock = None,
                 target_temperature: float = 25.0,
                 enabled: bool = False,
                 verbose: bool = True):
        self.id = id
        self.water_pump = WaterPump(id=id,
                                    i2c_lock=i2c_lock)
        self.pc_fan = PCFan(id=id,
                            i2c_lock=i2c_lock)
        self.temperature_sensor = WaterTemperatureSensor(id=id,
                                                         one_wire_lock=one_wire_lock)
        self.output = ESC(id=self._DEVICE_ID_MAP[id],
                          i2c_lock=i2c_lock)
        self.target_setpoint = target_temperature

        self.Kp = 80.0
        self.Ki = 0.2
        self.Kd = 10.0
        self.reset = 10
        # instantiate PID controller
        self.pid = PID(Kp=self.Kp,
                       Ki=self.Ki,
                       Kd=self.Kd,
                       setpoint=target_temperature,
                       sample_time=1.0,  # 1.0 s
                       output_limits=(-100, 100),
                       auto_mode=True,
                       proportional_on_measurement=False)

        # initialize log arrays
        self.temp_log = list()
        self.kp_log = list()
        self.ki_log = list()
        self.kd_log = list()
        self.control_val_log = list()
        self.actual_temperature = -100
        self.control_value  = 0
        self.enabled = enabled
        if not self.enabled:
            self.output.stop()
        self.verbose = verbose

    def info(self):
        print("Temperature Control Reactor {}: Target Temperature: {}, Actual Temperature: {}, Coefficients: {}".format(self.id, self.target_setpoint, self.actual_temperature, self.pid.components))

    def set_target_temperature(self,
                               temperature: float):
        self.target_setpoint = temperature
        self.pid.setpoint = self.target_setpoint

    def enable(self):
        self.enabled = True
        self.water_pump.start()
        self.pc_fan.set_speed(100)

    def disable(self):
        self.enabled = False
        self.water_pump.stop()
        self.pc_fan.set_speed(0)
        self.output.stop()

    def finalize(self):
        self.disable()


    def control_loop(self):

        if self.enabled:

            if self.reset < 0:
                self.output.stop()
                time.sleep(1.0)
                self.reset = 10
                self.output.set_value(int(self.pid(self.actual_temperature)))
            else:
                self.reset -= 1
                
            # get current temperature
            actual_temperature = self.temperature_sensor.get_temperature()
            self.actual_temperature = actual_temperature

            if self.verbose:
                print("current temperature: {}".format(actual_temperature))
                print("target temperature: {}".format(self.target_setpoint))
            # anti wind-up procedure
            (kp, ki, kd) = self.pid.components
            if (kp + ki + kd) > 100 or (kp + ki + kd) < -100:
                self.pid.Ki = 0.0
            else:
                self.pid.Ki = self.Ki

            # compute new ouput from the PID according to the systems current value
            self.control_value = int(self.pid(actual_temperature))

            # do custom control_value heuristics: peltier elements should not change polarity too often
            # control_value = control_value if abs(control_value) > 10 else 0.0

            if self.verbose:
                print("control value: {}".format(self.control_value))
                print("pid components: {}".format(self.pid.components))

            # feed the PID output to the system
            self.output.set_value(self.control_value)

            # append log
            self.temp_log.append(actual_temperature)
            self.control_val_log.append(self.control_value)
            (kp, ki, kd) = self.pid.components
            self.kp_log.append(kp)
            self.ki_log.append(ki)
            self.kd_log.append(kd)


if __name__ == "__main__":

    reactor0 = ReactorTemperatureControl(1, threading.Lock(), threading.Lock(), 27.0)
    reactor0.enable()

    # run control loop till keyboard interrupt (Ctrl + C)
    try:
        while True:
            reactor0.control_loop()
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("Exiting...but first put device into a safe state...")
    finally:
        reactor0.finalize()
        # save log files
        timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")
        np.savetxt(fname="log/{}_temperature.csv".format(timestamp), delimiter=",", X=reactor0.temp_log)
        np.savetxt(fname="log/{}_control_value.csv".format(timestamp), delimiter=",", X=reactor0.control_val_log)
        np.savetxt(fname="log/{}_kp.csv".format(timestamp), delimiter=",", X=reactor0.kp_log)
        np.savetxt(fname="log/{}_ki.csv".format(timestamp), delimiter=",", X=reactor0.ki_log)
        np.savetxt(fname="log/{}_kd.csv".format(timestamp), delimiter=",", X=reactor0.kd_log)