from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685


def init(bus: busio) -> PCA9685:
    pwm_driver = PCA9685(bus)
    pwm_driver.frequency = 60
    return pwm_driver


def set_pwm(lib: PCA9685,
            channel: int,
            value: int):
    """

    :param lib: PCA9685 pwd driver library instance
    :param channel: channel
    :param value: pwm value (0x0000 - 0xffff)
    """
    # check input value
    if value > 0xffff or value < 0x0000:
        raise ValueError("Value out of bounds.")
    if channel > 15 or channel < 0:
        raise ValueError("Channel number out of bounds.")

    lib.channels[channel].duty_cycle = value


if __name__ == "__main__":

    # Create the I2C bus interface.
    i2c_bus = busio.I2C(SCL, SDA)

    # Create a simple PCA9685 class instance.
    pca = init(i2c_bus)

    # set all outputs to their default value

    # peristaltic pumps
    value = 0xffff
    set_pwm(pca, 0, 0x0000)
    set_pwm(pca, 1, 0x0000)
    set_pwm(pca, 2, 0x0000)
    set_pwm(pca, 3, 0x0000)
    set_pwm(pca, 4, 0x0000)
    set_pwm(pca, 5, 0x0000)
    set_pwm(pca, 12, 0x0000)
    set_pwm(pca, 13, 0x0000)
    set_pwm(pca, 14, 0x0000)

    # pc fan
    set_pwm(pca, 8, 0xffff)
    set_pwm(pca, 9, 0xffff)
    set_pwm(pca, 10, 0xffff)

    # water pump
    set_pwm(pca, 6, 0xffff)
    set_pwm(pca, 7, 0x0000)
    set_pwm(pca, 11, 0x0000)
