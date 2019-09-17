import smbus

_BUS_NO = 1
_DEVICE_ADDRESS = 0x38

bus = smbus.SMBus(_BUS_NO)


def clear_all():
    bus.write_byte(_DEVICE_ADDRESS, 0x00)


def set_all():
    bus.write_byte(_DEVICE_ADDRESS, 0xff)


def set(port: int):
    # read register
    state = bus.read_byte(_DEVICE_ADDRESS)
    # set port
    bus.write_byte(_DEVICE_ADDRESS, state | (0x1 << port))


def clear(port: int):
    # read register
    state = bus.read_byte(_DEVICE_ADDRESS)
    # clear port
    bus.write_byte(_DEVICE_ADDRESS, state & (0xff ^ (0x1 << port)))


# note: PCF8574 uses 'sinking': 0 -> on, 1 -> off

set_all()
clear(1)

