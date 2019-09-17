import smbus

_BUS_NO = 1
_DEVICE_ADDRESS = 0x07

bus = smbus.SMBus(_BUS_NO)


def set_value(device: int, value: int):
    # device: {1,2,3}
    # value: input: [-100, 100] (needs to be mapped to [0, 200]
    bus.write_i2c_block_data(_DEVICE_ADDRESS, device, [value + 100])


def stop_esc(device: int):
    set_value(device, 0)


def full_forward(device: int):
    set_value(device, 100)


def full_reverse(device: int):
    set_value(device, -100)

