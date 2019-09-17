import time
import smbus

_DEVICE_ADDRESS = 0x07

def set_value(bus: SMBus,
              device: int,
              value: int):
    """
    Sets the speed of the ESC.
    :param bus: smbus instance
    :param device: ESC device id {0, 1, 2}
    :param value: speed value [-100, 100]
    """
    bus.write_i2c_block_data(_DEVICE_ADDRESS, device, [value + 100])  # needs to be mapped to [0, 200]


def stop_esc(bus: SMBus,
             device: int):
    set_value(bus, device, 0)


def full_forward(bus: SMBus,
                 device: int):
    set_value(bus, device, 100)


def full_reverse(bus: SMBus,
                 device: int):
    set_value(bus, device, -100)


if __name__ == "__main__":

    # instantiate i2c smbus
    _BUS_NO = 1
    bus = smbus.SMBus(_BUS_NO)

    while True:
        stop_esc(bus, 0)
        stop_esc(bus, 1)
        stop_esc(bus, 2)
        time.sleep(10)
        full_forward(bus, 0)
        full_forward(bus, 1)
        full_forward(bus, 2)
        stop_esc(bus, 0)
        stop_esc(bus, 1)
        stop_esc(bus, 2)
        time.sleep(10)
        full_reverse(bus, 0)
        full_reverse(bus, 1)
        full_reverse(bus, 2)
