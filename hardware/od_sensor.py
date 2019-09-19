import time
import smbus
from board import SCL, SDA
import busio
import numpy as np
from simple_pid import PID

from i2c.PCF8574 import clear_all, set_all, set, clear
from i2c.PCA9685 import set_pwm

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
            set_pwm(busio_bus, 13, 0xffff)
            
            print("run peristaltic pump")
            time.sleep(10)
        
            # let the biomass settle down for 3s
            set_pwm(busio_bus, 13, 0x0000)

            print("stop peristaltic pump")
            time.sleep(3)
    

            print("measure")
            # measure dark value
            set(smbus, 0)
            time.sleep(1.0)
            #dark =
            # measure light value
            clear(smbus, 0)
            time.sleep(1.0)
            #light =

            od = 0.0 #light - dark

            # append log
            od_log.append(od)

            time.sleep(60.0 - ((time.time() - starttime) % 60.0))

    except KeyboardInterrupt:
        # save log files
        np.savetxt(fname="od.csv", delimiter=",", X=od_log)
        set_pwm(busio_bus, 13, 0x0000)

