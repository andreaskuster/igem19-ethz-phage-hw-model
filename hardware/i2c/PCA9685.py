from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685


def set_pwm(bus,
            channel,
            value):
    """

    :param bus: busio instance
    :param channel: channel
    :param value: pwm value (0x0000 - 0xffff)
    """
    pca = PCA9685(bus)
    pca.frequency = 60
    pca.channels[channel].duty_cycle = value


if __name__ == "__main__":

    # Create the I2C bus interface.
    i2c_bus = busio.I2C(SCL, SDA)

    # Create a simple PCA9685 class instance.
    pca = PCA9685(i2c_bus)

    # Set the PWM frequency to 60hz.
    pca.frequency = 60



    # peristaltic pumps
    value = 0xffff
    pca.channels[0].duty_cycle = 0
    pca.channels[1].duty_cycle = 0
    pca.channels[2].duty_cycle = 0
    pca.channels[3].duty_cycle = 0
    pca.channels[4].duty_cycle = 0
    pca.channels[5].duty_cycle = 0
    pca.channels[12].duty_cycle = 0
    pca.channels[13].duty_cycle = 0xffff
    pca.channels[14].duty_cycle = 0


    # pc fan
    pca.channels[8].duty_cycle = 0xffff
    pca.channels[9].duty_cycle = 0xffff
    pca.channels[10].duty_cycle = 0x0000


    # water pump
    pca.channels[6].duty_cycle = 0
    pca.channels[7].duty_cycle = 0
    pca.channels[11].duty_cycle = 0

