import time
import smbus
from board import SCL, SDA
import busio
import numpy as np
from simple_pid import PID

from i2c.PCF8574 import clear_all, set_all, set, clear
from i2c.PCA9685 import set_pwm
from i2c.TSL2591 import read_light_intensity

if __name__ == "__main__":

    _BUS_NO = 1
    smbus = smbus.SMBus(_BUS_NO)
    # Create the I2C bus interface.

    busio_bus = busio.I2C(SCL, SDA)

    # define target value and reactor id
    _TARGET_REACTOR = 0

    # initialize log arrays
    od_log = list()


    try:
        # run control loop till keyboard interrupt (Ctrl + C)
        starttime = time.time()

        while True:

            # run peristaltic pump for 10s
            print("run peristaltic pump")
            set_pwm(busio_bus, 13, 0xffff)
            time.sleep(10)
        
            # let the biomass settle down for 3s
            print("stop peristaltic pump")
            set_pwm(busio_bus, 13, 0x0)
            time.sleep(3)

            # start measuring
            print("measure")

            # measure dark value
            set(smbus, 0)
            time.sleep(1.0)
            dark = read_light_intensity(busio_bus, 0)
            # measure light value
            clear(smbus, 0)
            time.sleep(1.0)
            light = read_light_intensity(busio_bus, 0)
            od = light - dark
            print("od value: {}".format(od))

            # switch led off
            set(smbus, 0)

            # append log
            print("log data")
            od_log.append(od)

            # wait for the next measurement cycle
            print("sleep till next cycle")
            interval = 30.0
            time.sleep(interval - ((time.time() - starttime) % interval))

    except KeyboardInterrupt:
        # save log files
        np.savetxt(fname="od.csv", delimiter=",", X=od_log)
        set_pwm(busio_bus, 13, 0x0000)



#  calibration and conversion: do ridge regression: https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression