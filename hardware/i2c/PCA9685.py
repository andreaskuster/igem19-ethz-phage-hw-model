import time
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

while True:
    # Move servo on channel O between extremes.
    pwm.set_pwm(8, 0, 0)
    time.sleep(1)
    pwm.set_pwm(8, 0, 4096)
    time.sleep(1)


