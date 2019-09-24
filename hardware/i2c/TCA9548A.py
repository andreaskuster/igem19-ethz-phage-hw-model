import time
import smbus

_DEVICE_ADDRESS = 0x70


def switch(bus: smbus,
        port: int):
    """
    Sets an individual I/O to one.
    :param bus: smbus instance
    :param port: I2C channel (0,..,7)
    """
    # set port
    bus.write_byte(_DEVICE_ADDRESS, 0x1 << port)



if __name__ == "__main__":

    # instantiate i2c smbus
    _BUS_NO = 1
    bus = smbus.SMBus(_BUS_NO)

    _CHANNEL = 2

    switch(bus, _CHANNEL)