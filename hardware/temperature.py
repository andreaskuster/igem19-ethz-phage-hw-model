import smbus
import numpy as np

from simple_pid import PID

from i2c.ESC import set_value, stop_esc, full_forward, full_reverse
from one_wire.DS18B20 import get_temperature

if __name__ == "__main__":

    _BUS_NO = 1
    bus = smbus.SMBus(_BUS_NO)


    # define target value and reactor id
    _TARGET_SETPOINT = 39.7
    _TARGET_REACTOR = 2

    _Kp = 80.0
    _Ki = 0.2
    _Kd = 10.0

    # instantiate PID controller
    pid = PID(Kp=_Kp, #150.0,
              Ki=_Ki,
              Kd=_Kd,
              setpoint=_TARGET_SETPOINT,
              sample_time=1.0,  # 1.0 s
              output_limits=(-100, 100),
              auto_mode=True,
              proportional_on_measurement=False)

    # initialize log arrays
    temp_log = list()
    kp_log = list()
    ki_log = list()
    kd_log = list()
    control_val_log = list()

    try:
        # run control loop till keyboard interrupt (Ctrl + C)
        while True:
            # get current temperature
            actual_temperature = get_temperature(_TARGET_REACTOR)

            print("current temperature: {}".format(actual_temperature))

            # anti wind-up procedure
            (kp, ki, kd) = pid.components
            if (kp + ki + kd) > 100 or (kp + ki + kd) < -100:
                pid.Ki = 0.0
            else:
                pid.Ki = _Ki

            # compute new ouput from the PID according to the systems current value
            control_value = int(pid(actual_temperature))

            # do custom control_value heuristics: peltier elements should not change polarity too often
            # control_value = control_value if abs(control_value) > 10 else 0.0

            print("control value: {}".format(control_value))
            print("pid components: {}".format(pid.components))

            # feed the PID output to the system
            set_value(bus, _TARGET_REACTOR, control_value)

            # append log
            temp_log.append(actual_temperature)
            control_val_log.append(control_value)
            (kp, ki, kd) = pid.components
            kp_log.append(kp)
            ki_log.append(ki)
            kd_log.append(kd)

    except KeyboardInterrupt:
        # save log files
        np.savetxt(fname="temperature.csv", delimiter=",", X=temp_log)
        np.savetxt(fname="control_value.csv", delimiter=",", X=control_val_log)
        np.savetxt(fname="kp.csv", delimiter=",", X=kp_log)
        np.savetxt(fname="ki.csv", delimiter=",", X=ki_log)
        np.savetxt(fname="kd.csv", delimiter=",", X=kd_log)


# integrate anti-windup and increase integral value to reach the target value:
# https://info.erdosmiller.com/blog/pid-anti-windup-techniques
# http://brettbeauregard.com/blog/2011/04/improving-the-beginner%E2%80%99s-pid-reset-windup/
# https://ch.mathworks.com/help/simulink/slref/anti-windup-control-using-a-pid-controller.html;jsessionid=d9bbc6f16c16b3adb8c425a92d74

# we do anti-windup by setting Ki to 0 if the control output is higher than the maximum value  (100)
