import numpy as np
from simple_pid import PID

import hardware.i2c.ESC

if __name__ == "__main__":

    # define target value and reactor id
    _TARGET_SETPOINT = 39.7
    _TARGET_REACTOR = 0

    # instantiate PID controller
    pid = PID(Kp=1.0,
              Ki=0.0,
              Kd=0.0,
              setpoint=_TARGET_SETPOINT,
              sample_time=10.0,  # 10.0 s
              output_limits=(None, None),
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
            actual_temperature = hardware.one_wire.DS18B20.get_temperature(_TARGET_REACTOR)

            # compute new ouput from the PID according to the systems current value
            control_value = pid(actual_temperature)

            # do custom control_value heuristics: peltier elements should not change polarity too often
            control_value = control_value if abs(control_value) > 10 else 0.0

            # feed the PID output to the system
            hardware.i2c.ESC.set_value(control_value)

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
