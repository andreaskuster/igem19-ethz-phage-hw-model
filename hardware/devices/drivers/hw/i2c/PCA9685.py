import busio
from adafruit_pca9685 import PCA9685 as library
from board import SCL, SDA


class PCA9685:
    lib = library(busio.I2C(SCL, SDA))

    def __init__(self):
        PCA9685.init()

    @staticmethod
    def init():
        """
        Initialize board.
        """
        PCA9685.lib.frequency = 60

    @staticmethod
    def set_pwm(channel: int,
                value: int) -> None:
        """
        Set the PWM (pulse width modulation) value of a channel.
        :param channel: channel
        :param value: pwm value (0x0000 - 0xffff)
        """
        # check input value
        if value > 0xffff or value < 0x0000:
            raise ValueError("Value out of bounds.")
        if channel > 15 or channel < 0:
            raise ValueError("Channel number out of bounds.")
        # check lib initialized
        if PCA9685.lib is None:
            raise RuntimeError("Module has not been initialized.")
        # set pwm value
        PCA9685.lib.channels[channel].duty_cycle = value

    @staticmethod
    def set_all(value: int) -> None:
        """
        Set the PWM value of all channels.
        :param value: pwm value (0x0000 - 0xffff)
        """
        for i in range(16):
            PCA9685.set_pwm(i, value)


if __name__ == "__main__":
    # initialize the PCA9685 board
    PCA9685.init()

    # set all outputs to their default value

    # peristaltic pumps
    PCA9685.set_pwm(0, 0x0000)
    PCA9685.set_pwm(1, 0x0000)
    PCA9685.set_pwm(2, 0x0000)
    PCA9685.set_pwm(3, 0x0000)
    PCA9685.set_pwm(4, 0x0000)
    PCA9685.set_pwm(5, 0x0000)
    PCA9685.set_pwm(12, 0x0000)
    PCA9685.set_pwm(13, 0x0000)
    PCA9685.set_pwm(14, 0x0000)

    # pc fan
    PCA9685.set_pwm(8, 0xffff)
    PCA9685.set_pwm(9, 0xffff)
    PCA9685.set_pwm(10, 0xffff)

    # water pump
    PCA9685.set_pwm(6, 0x0000)
    PCA9685.set_pwm(7, 0x0000)
    PCA9685.set_pwm(11, 0x0000)
