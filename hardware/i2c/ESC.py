import smbus

bus = smbus.SMBus(1)

#bus.write_byte_data(0x07, 0x0, 0x00)
#bus.write_byte_data(0x07, 0x0, 0x96)

val = 100
bus.write_i2c_block_data(0x07, 0x00, [val])
bus.write_i2c_block_data(0x07, 0x01, [val])
bus.write_i2c_block_data(0x07, 0x02, [val])
