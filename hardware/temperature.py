from simple_pid import PID

import hardware.i2c.ESC


if __name__ == "__main__":
    _TARGET_SETPOINT = 39.7
    _TARGET_REACTOR = 0

    # instantiate PID controller
    pid = PID(Kp=1.0,
              Ki=0.0,
              Kd=0.0,
              setpoint=_TARGET_SETPOINT,
              sample_time=10.0, # 10.0 s
              output_limits=(None, None),
              auto_mode=True,
              proportional_on_measurement=False)

    while True:
        # get current temperature
        actual_temperature = hardware.one_wire.DS18B20.get_temperature(_TARGET_REACTOR)

        # compute new ouput from the PID according to the systems current value
        control_value = pid(actual_temperature)

        # do custom control_value heuristics: peltier elements should not change polarity too often
        control_value = control_value if abs(control_value) > 10 else 0.0

        # feed the PID output to the system
        hardware.i2c.ESC.set_value(control_value)
