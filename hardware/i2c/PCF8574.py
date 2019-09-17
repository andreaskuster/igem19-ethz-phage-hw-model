import smbus

bus = smbus.SMBus(1)

def clear():
    bus.write_byte(0x38, 0x00)


#port = 4  # 0..7


# note: PCF8574 uses 'sinking': 0 -> on, 1 -> off


bus.write_byte(0x38, 0xff)
#bus.write_byte(0x38, 0x01 << port)
