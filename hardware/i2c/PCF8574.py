import smbus

bus = smbus.SMBus(1)

def clear():
    bus.write_byte(0x38, 0x00)


port = 4  # 0..7


bus.write_byte(0x38, 0x01 << port)
