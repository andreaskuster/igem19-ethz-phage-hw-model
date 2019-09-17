import time
import smbus

_DEVICE_ADDRESS = 0x38


def clear_all(bus: smbus):
    """
    Resets all eight I/Os to zero.
    :param bus: smbus instance
    """
    bus.write_byte(_DEVICE_ADDRESS, 0x00)


def set_all(bus: smbus):
    """
    Sets all eight I/Os to one.
    :param bus:
    """

    bus.write_byte(_DEVICE_ADDRESS, 0xff)


def set(bus: smbus,
        port: int):
    """
    Sets an individual I/O to one.
    :param bus: smbus instance
    :param port: I/O port (0,..,7)
    """
    # read register
    state = bus.read_byte(_DEVICE_ADDRESS)
    # set port
    bus.write_byte(_DEVICE_ADDRESS, state | (0x1 << port))


def clear(bus: smbus,
          port: int):
    """
    Clears an individual I/O to zero.
    :param bus: smbus instance
    :param port: I/O port (0,..,7)
    """
    # read register
    state = bus.read_byte(_DEVICE_ADDRESS)
    # clear port
    bus.write_byte(_DEVICE_ADDRESS, state & (0xff ^ (0x1 << port)))


def toggle(bus: smbus,
          port: int):
    """
    Toggles an individual I/O port.
    :param bus: smbus instance
    :param port: I/O port (0,..,7)
    """
    # read register
    state = bus.read_byte(_DEVICE_ADDRESS)
    # clear port
    bus.write_byte(_DEVICE_ADDRESS, state ^ (0x1 << port))


if __name__ == "__main__":

    # instantiate i2c smbus
    _BUS_NO = 1
    bus = smbus.SMBus(_BUS_NO)

    # run all on / all off interval
    while True:
        print("set all outputs")
        set_all(bus)
        time.sleep(10)
        print("reset all outputs")
        clear_all(bus)
        time.sleep(10)

# note: PCF8574 uses 'sinking': 0 -> on, 1 -> off
