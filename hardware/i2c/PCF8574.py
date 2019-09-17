import smbus

_BUS_NO = 1
_DEVICE_ADDRESS = 0x38

bus = smbus.SMBus(_BUS_NO)


def clear_all():
    bus.write_byte(_DEVICE_ADDRESS, 0x00)


def set_all():
    bus.write_byte(_DEVICE_ADDRESS, 0xff)



# note: PCF8574 uses 'sinking': 0 -> on, 1 -> off


bus.write_byte(_DEVICE_ADDRESS, 0xff)

print(bus.read_byte(_DEVICE_ADDRESS))

#bus.write_byte(0x38, 0x01 << port)
